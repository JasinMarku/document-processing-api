import time
from datetime import datetime, timezone

from app.domain.models.document import DocumentStatus
from app.domain.ports.documents_repo import DocumentsRepository

# Process to take job, and process it
# Updates status as it goes
def process_job(repo: DocumentsRepository, document_id: str) -> None:
    doc = repo.get(document_id)
    if doc is None:
        return

    try:
        repo.update(doc.with_status(DocumentStatus.PROCESSING))
        time.sleep(1)
        repo.update(doc.with_status(DocumentStatus.COMPLETED))
    except Exception as e:
        repo.update(doc.with_status(DocumentStatus.FAILED, error=str(e)))