# Custom domain-level error for when a document doesn't exist
class DocumentNotFoundError(Exception):
    pass

class InvalidDocumentStateError(Exception):
    pass

# Raised when user input violates business rules (content type, filename, etc...)
class InvalidDocumentInputError(Exception):
    pass
