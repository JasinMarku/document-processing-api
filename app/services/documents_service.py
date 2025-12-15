from app.domain.ports.documents_repo import DocumentsRepository
from app.domain.ports.storage import StoragePort
from app.domain.ports.queue import QueuePort

class DocumentService:
    def __init__(self, repo: DocumentsRepository, storage: StoragePort,queue: QueuePort) -> None:
        self.repo = repo
        self.storage = storage
        self.queue = queue