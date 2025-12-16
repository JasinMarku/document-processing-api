class InMemoryStorage:

    # Creates a safe, predictable path where the file "would" be stored
    def create_object_key(self, document_id: str, filename: str) -> str:
        # Replace / with + to prevent path issues, remove extra spaces
        safe_name = filename.replace("/","_").strip()
        return f"documents/{document_id}/{safe_name}"


    # Returns a fake upload URL (just a string that looks real)
    # In real S3 version, this will be a temporary signed link from AWS
    def create_presigned_upload_url(self, object_key: str, content_type: str) -> str:
        # Fake URL for local development. Real presigned URL comes with S3 later.
        return f"https://example.local/upload?key={object_key}&content_type={content_type}"

