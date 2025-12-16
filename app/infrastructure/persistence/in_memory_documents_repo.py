from typing import Dict, Optional
from app.domain.models.document import Document

# This class is a simple fake database that lives only in memory
# Follows the exact same rules (contract) as DocumentsRepository
class InMemoryDocumentsRepository:

    # Runs when you create the repo: starts with an empty database
    def __init__(self) -> None:
        self._docs: Dict[str, Document] = {} # Dictionary: id -> document

    # Saves a new document and returns it
    def create(self, document: Document) -> Document:
        self._docs[document.id] = document
        return document

    # Finds and returns a document by its id, or None if found
    def get(self, document_id: str) -> Optional[Document]:
        return self._docs.get(document_id)

    # Saves changes to an existing document and returns the updated one
    def update(self, document: Document) -> Document:
        self._docs[document.id] = document
        return document