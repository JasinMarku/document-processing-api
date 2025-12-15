from typing import Protocol

class QueuePort(Protocol):
    def enqueue_document_processing(self, document_id: str, object_key: str) -> str:
        ...