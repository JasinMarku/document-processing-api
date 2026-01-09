from functools import lru_cache # Helps keep the same instances (singleton)

from app.core.settings import settings                      # Central config
from app.infrastructure.storage.s3_storage import S3Storage # Real AWS adapter

# Import fake in-memory implementations
from app.infrastructure.persistence.in_memory_documents_repo import InMemoryDocumentsRepository
from app.infrastructure.storage.in_memory_storage import InMemoryStorage
from app.infrastructure.queue.in_memory_queue import InMemoryQueue

# Import service that needs them
from app.services.document_service import DocumentService
from app.domain.ports.storage import StoragePort

# Returns the same repository every time (so data doesn't disappear between requests)
@lru_cache(maxsize=1)
def get_documents_repo() -> InMemoryDocumentsRepository:
    return InMemoryDocumentsRepository()

# Returns the same storage instance every time
@lru_cache(maxsize=1)
def get_storage() -> StoragePort:
    """
    Returns the correct storage implementation based on APP_ENV.
    - local: InMemoryStorage (fake URLs)
    - aws: S3Storage (real presigned URLs)
    Validates bucket name when using AWS mode.
     """
    if settings.APP_ENV == "aws":
        if not settings.S3_BUCKET_NAME:
            raise RuntimeError("S3_BUCKET_NAME must be set when APP_ENV = AWS")
        return S3Storage()

    # Default: local dev mode
    return InMemoryStorage()

# Returns the same queue instance every time
@lru_cache(maxsize=1)
def get_queue() -> InMemoryQueue:
    return InMemoryQueue()

# Builds and returns the full service using the three pieces above
def get_document_service() -> DocumentService:
    return DocumentService(
        repo=get_documents_repo(),
        storage=get_storage(),
        queue=get_queue(),
    )