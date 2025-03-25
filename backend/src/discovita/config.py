"""Application configuration."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env in project root
load_dotenv(Path(__file__).parents[3] / ".env")

@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    icons8_api_key: str
    icons8_base_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    s3_bucket: str
    openai_api_key: str
    adalo_app_id: str
    adalo_api_key: str
    database_url: str
    use_sql_database: bool
    debug: bool

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        icons8_api_key = os.getenv("FACESWAP_API_KEY")
        if not icons8_api_key:
            raise ValueError("FACESWAP_API_KEY is required")

        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if not aws_access_key_id:
            raise ValueError("AWS_ACCESS_KEY_ID is required")

        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if not aws_secret_access_key:
            raise ValueError("AWS_SECRET_ACCESS_KEY is required")

        s3_bucket = os.getenv("S3_BUCKET")
        if not s3_bucket:
            raise ValueError("S3_BUCKET is required")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")

        adalo_app_id = os.getenv("ADALO_APP_ID")
        if not adalo_app_id:
            raise ValueError("ADALO_APP_ID is required")

        adalo_api_key = os.getenv("ADALO_API_KEY")
        if not adalo_api_key:
            raise ValueError("ADALO_API_KEY is required")

        return cls(
            icons8_api_key=icons8_api_key,
            icons8_base_url="https://api-faceswapper.icons8.com/api/v1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_region="us-east-1",
            s3_bucket=s3_bucket,
            openai_api_key=openai_api_key,
            adalo_app_id=adalo_app_id,
            adalo_api_key=adalo_api_key,
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db"),
            use_sql_database=os.getenv("USE_SQL_DATABASE", "false").lower() == "true",
            debug=os.getenv("DEBUG", "false").lower() == "true"
        )

@lru_cache()
def get_settings() -> Settings:
    """Get application settings.
    
    Returns:
        Settings instance (cached)
    """
    return Settings.from_env()
