from fastapi import APIRouter, Depends, HTTPException # APIRouter makes a group of endpoints

# Import DI, schemas, and service
from app.api.deps import get_document_service, get_documents_repo, get_queue
from app.api.schemas.documents import InitiateUploadRequest, InitiateUploadResponse, DocumentResponse, EnqueueResponse
from app.domain.errors import DocumentNotFoundError
from app.services.document_service import DocumentService
from app.domain.errors import InvalidDocumentStateError
from app.workers.processor_stub import process_job

# Create the router for all document-related endpoints
router = APIRouter(prefix="/documents")

# Actual endpoint: POST /documents/initiate-upload
@router.post("/initiate-upload", response_model=InitiateUploadResponse)
def initiate_upload(
        request: InitiateUploadRequest,
        service: DocumentService = Depends(get_document_service),
) -> InitiateUploadResponse:
    # Call the real logic in the service
    document_id, object_key, upload_url = service.initiate_upload(
        filename=request.filename,
        content_type=request.content_type,
    )

    # Build and return the response object
    return InitiateUploadResponse(
        document_id=document_id,
        object_key=object_key,
        upload_url=upload_url
    )


# GET a single document by ID
@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
        document_id: str,
        service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    try:
        doc = service.get_document(document_id)
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse(
        id=doc.id,
        filename=doc.filename,
        content_type=doc.content_type,
        s3_key=doc.s3_key,
        status=doc.status,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        last_error=doc.last_error,
    )

# Enqueue a document for background processing
@router.post("/{document_id}/enqueue", response_model=EnqueueResponse)
def enqueue_document(
        document_id: str, # From the path
        service: DocumentService = Depends(get_document_service),
) -> EnqueueResponse:
    try:
        job_id = service.enqueue_processing(document_id)
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except InvalidDocumentStateError as e:
        raise HTTPException(status_code=400, detail=str(e)) # 409 Conflict for invalid state

    return EnqueueResponse(job_id=job_id)



# DEBUG:
# ------------------------------------------------------------------------
# @router.post("/_debug/process-next")
# def debug_process_next() -> dict:
#     repo = get_documents_repo()
#     queue = get_queue()
#
#     msg = queue.dequeue()
#     if msg is None:
#         return {"processed": False, "reason": "queue empty"}
#
#     process_job(repo=repo, document_id=msg["document_id"])
#     return {"processed": True, "document_id": msg["document_id"]}