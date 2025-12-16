from pydantic import BaseModel # Helps validate and serialize data
from datetime import datetime
from app.domain.models.document import DocumentStatus

# What the client must send when asking to start an upload
class InitiateUploadRequest(BaseModel):
    filename: str
    content_type: str

# What the API returns after creating the document
class InitiateUploadResponse(BaseModel):
    document_id: str
    object_key: str
    upload_url: str

# Response model for returning full document details to the client
class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    s3_key: str
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
    last_error: str | None = None

# Response when enqueuing a document for processing
class EnqueueResponse(BaseModel):
    job_id: str # The ID of the queued job
