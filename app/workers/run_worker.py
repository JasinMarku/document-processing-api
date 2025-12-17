from datetime import datetime, timezone

# Same DI as the API to get in-memory repo and queue
from app.api.deps import get_documents_repo, get_queue

# Typed job message and processor
from app.workers.job_message import JobMessage
from app.workers.processor_stub import process_job

def main() -> None:
    # Get the same in-memory repository and queue used by the API
    # This allows the worker to see queued jobs and update document state
    repo = get_documents_repo()
    queue = get_queue()

    raw = queue.dequeue()

    # Keep processing jobs until the queue is empty
    while raw is not None:
        # Convert the raw queue message into a structured job object
        msg = JobMessage(
            job_id=raw["job_id"],
            document_id=raw["document_id"],
            s3_key=raw["object_key"],
            requested_at=datetime.now(timezone.utc),
        )

        # Process the document associated with this job
        # This simulates background work and updates document status
        process_job(repo=repo, document_id=msg.document_id)

        # Move onto the next job in the queue
        raw = queue.dequeue()

# Allow this file to be run directly as a worker script
if __name__ == "__main__":
    main()