import uuid

# Fake queue that lives only in memory
# It pretends to send jobs for background processing
class InMemoryQueue:

    # Starts with an empty list of messages
    def __init__(self) -> None:
        self._messages: list[dict] = []

    # Adds a new job to the "queue" and returns a job ID
    def enqueue_document_processing(self, document_id: str, object_key: str) -> str:
        job_id = str(uuid.uuid4()) # Random unique ID for the job
        message = {
            "job_id": job_id,
            "document_id": document_id,
            "object_key": object_key,
        }
        self._messages.append(message) # Save it in the list
        return job_id # Give the ID back to the caller


    # Gives the next job message to the worker
        # Returns the oldest message or None if queue is empty
        # Using pop(0) to maintain FIFO
    def dequeue(self) -> dict | None:
        if not self._messages:
            return None
        return self._messages.pop(0)