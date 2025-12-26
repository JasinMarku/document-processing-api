# print(">>> Loading document_service.py")

from app.domain.ports.documents_repo import DocumentsRepository
from app.domain.ports.storage import StoragePort
from app.domain.ports.queue import QueuePort
from app.domain.models.document import Document, DocumentStatus
from app.domain.errors import DocumentNotFoundError, InvalidDocumentStateError

from app.domain.errors import InvalidDocumentInputError

import uuid
from datetime import datetime, timezone
from typing import Dict, Set

ALLOWED_TRANSITIONS: dict[DocumentStatus, set[DocumentStatus]] = {
    DocumentStatus.INITIATED: {DocumentStatus.QUEUED},
    DocumentStatus.QUEUED: {DocumentStatus.PROCESSING},
    DocumentStatus.PROCESSING: {DocumentStatus.COMPLETED, DocumentStatus.FAILED},
    DocumentStatus.COMPLETED: set(), # Terminal State
    DocumentStatus.FAILED: set(), # Terminal State
}

# Types of content allowed for processing
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
}

class DocumentService:
    _repo: DocumentsRepository
    _storage: StoragePort
    _queue: QueuePort

    def __init__(self, repo: DocumentsRepository, storage: StoragePort,queue: QueuePort) -> None:
#       print(">>> DocumentService __init__ called")  # TEMPORARY DEBUG LINE
        self._repo = repo
        self._storage = storage
        self._queue = queue

# Main method for starting a new upload
    # Returns: (document_id, object_key, upload_url)
    def initiate_upload(self, filename: str, content_type: str) -> tuple[str, str, str]:
        # ---- Input Validation & Sanitization (Business Rules) ----

        # 1. Whitelist content types
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidDocumentInputError(f"Unsupported content type: {content_type}")

        # 2. Sanitize filename -- remove dangerous characters and trim
        safe_filename = filename.strip().replace("/","_").replace("\\", "_")
        if not safe_filename:
            raise InvalidDocumentInputError("Filename cannot be empty after sanitization")

        # ---- Rest of logic (using safe_filename) ----

        # 1. Create a unique ID for this document
        document_id = str(uuid.uuid4())

        # 2. Ask storage where the file should live
        object_key = self._storage.create_object_key(
            document_id = document_id,
            filename = safe_filename
        )

        # 3. Ask storage for a temporary upload link
        upload_url = self._storage.create_presigned_upload_url(
            object_key = object_key,
            content_type = content_type
        )

        # 4. Create the Document object in INITIATED state
        now = datetime.now(timezone.utc)
        doc = Document(
            id = document_id,
            filename = safe_filename,
            content_type=content_type,
            s3_key=object_key,
            status=DocumentStatus.INITIATED,
            created_at=now,
            updated_at=now,
            last_error=None,
        )

        # 5. Save it using the repository
        self._repo.create(doc)

        # 5. Return the three values the API needs to send back to the user
        return document_id, object_key, upload_url

# Retrieves a document by ID
    # Raises DocumentNotFoundError if it doesn't exist (API will turn this into 404)
    def get_document(self, document_id: str) -> Document:
        doc = self._repo.get(document_id)
        if doc is None:
            raise DocumentNotFoundError(f'Document with id {document_id} not found')
        return doc

# Enqueues a document for background processing
    # Only allowed when status is INITIATED
    # Updates status to QUEUED and returns the job_id from the queue
    def enqueue_processing(self, document_id: str) -> str:
        # 1. Get the document or raise 404
        doc = self._repo.get(document_id)
        if doc is None:
            raise DocumentNotFoundError(f'Document not found: {document_id}')

        # 2. Check if transition to QUEUED is allowed FROM CURRENT STATUS
        # This runs BEFORE we change anything
        self._ensure_transition(doc.status, DocumentStatus.QUEUED)

        # 3. Only now do we update the status (transition is confirmed valid)
        doc.status = DocumentStatus.QUEUED
        doc.updated_at = datetime.now(timezone.utc)
        self._repo.update(doc)

        # 4. Enqueue the actual job
        job_id = self._queue.enqueue_document_processing(
            document_id = document_id,
            object_key=doc.s3_key
        )

        return job_id

    def _ensure_transition(self, current: DocumentStatus, target: DocumentStatus) -> None:
        """
        Checks if moving from 'current' status to 'target' is allowed.
        Raises InvalidDocumentStateError if not.
        This keeps all transition rules in one place.
        """
        allowed = ALLOWED_TRANSITIONS.get(current, set()) # Get allowed next statuses
        if target not in allowed:
            raise InvalidDocumentStateError(
                f"Invalid status transition: {current} -> {target}"
            )
