from functools import lru_cache
import boto3

# Import central config (bucket, region, etc.)
from app.core.settings import settings

# Returns the same boto3 session every time (singleton per process)
@lru_cache(maxsize=1)
def get_boto3_session():
    """
    Creates a single boto3 session once per process.
    All credentials and defaults are loaded automatically from env vars.
    """
    return boto3.Session()

# Returns the same S3 client every time (singleton per process)
@lru_cache(maxsize=1)
def get_s3_client():
    """
    Gets a reusable S3 client using the cached session.
    Region comes from settings (defaults to us-east-1 if not set).
    """
    session = get_boto3_session()
    return session.client('s3', region_name=settings.AWS_REGION)

# Returns the same SQS client every time (singleton per process)
@lru_cache(maxsize=1)
def get_sqs_client():
    """
    Gets a reusable SQS client using the cached session.
    Region comes from settings (defaults to us-east-1 if not set).
    """
    session = get_boto3_session()
    return session.client('sqs', region_name=settings.AWS_REGION)