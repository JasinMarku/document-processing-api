# Custom domain-level error for when a document doesn't exist
class DocumentNotFoundError(Exception):
    pass

class InvalidDocumentStateError(Exception):
    pass
