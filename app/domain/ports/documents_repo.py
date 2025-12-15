# What actions does the system need to do with documents?
#   - Save a document (Create)
#   - Get a document by its id (Get)
#   - Save changes to an existing document (Update)

from typing import Protocol, Optional
from app.domain.models.document import Document

class DocumentsRepository(Protocol):
    def create(self, document: Document) -> Document:
        ...

    def get(self, document_id: str) -> Optional[Document]:
        ...

    def update(self, document: Document) -> Document:
        ...