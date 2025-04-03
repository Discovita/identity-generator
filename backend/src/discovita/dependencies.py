"""FastAPI dependency functions."""

from .config import Settings


def get_settings() -> Settings:
    """Dependency for application settings."""
    return Settings.from_env()
