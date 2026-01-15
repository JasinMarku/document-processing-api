import json
from datetime import datetime, timezone

from app.core.settings import settings
from app.domain.ports.queue import QueuePort
from app.infrastructure.aws.client_factory import get_sqs_client


class SQSQueue(QueuePort):
    """Real AWS SQS implementation of QueuePort. Sends messages to AWS instead of storing in memory."""
    
    def enqueue_document_processing(self, document_id: str, object_key: str) -> str:
        """Sends a job message to SQS and returns the MessageId as job_id."""
        sqs = get_sqs_client()

        # Build message payload that the worker will receive
        body = {
            "document_id": document_id,
            "s3_key": object_key,
            "requested_at": datetime.now(timezone.utc).isoformat(),
        }

        # Send to SQS (MessageBody must be a JSON string)
        resp = sqs.send_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MessageBody=json.dumps(body),
        )

        # Return SQS MessageId as job_id (like InMemoryQueue returns UUID)
        return resp["MessageId"]
