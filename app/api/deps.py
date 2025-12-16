from functools import lru_cache # Helps keep the same instances (singleton)

# Import fake in-memory implementations
from app.infrastructure.persistence.in_memory_documents_repo import InMemoryDocumentsRepository
from app.infrastructure.storage.in_memory_storage import InMemoryStorage
from app.infrastructure.queue.in_memory_queue import InMemoryQueue

# Import service that needs them
from app.services.document_service import DocumentService

# Returns the same repository every time (so data doesn't disappear between requests)
@lru_cache(maxsize=1)
def get_documents_repo() -> InMemoryDocumentsRepository:
    return InMemoryDocumentsRepository()

# Returns the same storage instance every time
@lru_cache(maxsize=1)
def get_storage() -> InMemoryStorage:
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