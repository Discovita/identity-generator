"""S3 service implementation."""

import uuid
from pathlib import Path
import boto3
from botocore.config import Config
from .models import FileUploadRequest
from ...config import Settings

class S3Service:
    """Service for S3 operations."""
    
    def __init__(self, settings: Settings) -> None:
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(region_name=settings.aws_region)
        )
        self.bucket = settings.s3_bucket
        self.region = settings.aws_region

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename while preserving the original extension."""
        extension = Path(original_filename).suffix
        random_name = str(uuid.uuid4())
        return f"{random_name}{extension}"

    def upload(self, request: FileUploadRequest) -> str:
        """Upload a file to S3 and return its public URL."""
        unique_filename = self._generate_unique_filename(request.filename)
        key = f"uploads/{unique_filename}"
        
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=request.content,
            ContentType=request.content_type
        )
        
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
