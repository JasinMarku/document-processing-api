# Defines what a "Document" is in my system, and states what it can be.

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

# This is a list of allowed "stages" a document can be in
class DocumentStatus(str, Enum):
    INITIATED = "INITIATED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# A form or record for one uploaded file
@dataclass(frozen=False)
class Document:
    id: str
    filename: str
    content_type: str
    s3_key: str
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    last_error: Optional[str] = None