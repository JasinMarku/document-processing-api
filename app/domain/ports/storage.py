from typing import Protocol

class StoragePort(Protocol):
# Given the document ID and original filename, return a safe path like "documents/123abc/resume.pdf
    def create_object_key(self, document_id: str, filename: str) -> str:
        ...

# Given that path and file type, return a temporary upload link (a long URL)
    def create_presigned_upload_url(self, object_key: str, content_type: str) -> str:
        ...