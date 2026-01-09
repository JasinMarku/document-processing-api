from __future__ import annotations

from app.core.settings import settings
from app.domain.ports.storage import StoragePort # Port interface
from app.infrastructure.aws.client_factory import get_s3_client # Reused singleton client

# Real S3 implementation of the storage contract
class S3Storage(StoragePort):
    # Same key format as in-memory -- keeps everything consistent
    def create_object_key(self, document_id: str, filename: str) -> str:
        # Sanitization to prevent bad paths
        safe_filename = filename.strip().replace("/","_").replace("\\","_")
        return f"{document_id}/{safe_filename}"

    # Generates a real, time-limited pre-signed PUT URL
    def create_presigned_upload_url(self, object_key: str, content_type: str) -> str:
        s3_client = get_s3_client() # Get the shared, cached client

        return s3_client.generate_presigned_url(
            ClientMethod='put_object', # Want a PUT (upload) URL
            Params={
                "Bucket": settings.S3_BUCKET_NAME, # Real bucket
                "Key": object_key,                # Full path in bucket
                "ContentType": content_type,      # Helps S3 validate
            },
            ExpiresIn=settings.S3_PRESIGN_EXPIRES_IN,   # From settings (default 5 min)
        )