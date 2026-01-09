import os

# Helper: safely get an env var or raise if missing/empty
def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


# Central config class - loaded once, used everywhere
class Settings:
    # Main toggle: "local" = in-memory fakes, "aws" = real S3/SQS
    APP_ENV: str = os.getenv("APP_ENV", "local") # Default to local for saftey

    # AWS-specific (only used if APP_ENV is "aws")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")  # Default region

    # Your S3 bucket name (required for real uploads)
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")

    # How long pre-signed URLs stay valid (in seconds)
    # 300 - 5 minutes - good balance between security and usability
    S3_PRESIGN_EXPIRES_IN: int = int(os.getenv("S3_PRESIGN_EXPIRES_IN", "300"))

# Global instance
settings = Settings()

