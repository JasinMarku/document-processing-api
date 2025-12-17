from dataclasses import dataclass
from datetime import datetime

# The standard shape of a processing job message
# This is what the queue carries, and what the worker will receive
@dataclass(frozen=True)
class JobMessage:
    job_id: str            # Unique ID for the job
    document_id: str       # Document ID
    s3_key: str            # Where uploaded file lives
    requested_at: datetime # When job was enqueued