"""API-specific data models."""

from pydantic import BaseModel, HttpUrl, AnyHttpUrl
from enum import IntEnum
from typing import Optional

class DescribeImageRequest(BaseModel):
    """Request to get a clean description of an image."""
    image_url: AnyHttpUrl

class DescribeImageResponse(BaseModel):
    """Response containing clean description of an image."""
    description: str

class GenerateImageRequest(BaseModel):
    setting: str
    outfit: str
    emotion: str
    userFeedback: str | None = None
    previousAugmentedPrompt: str | None = None
    userDescription: str | None = None  # Clean description of user's headshot

class GenerateImageResponse(BaseModel):
    imageUrl: str
    augmentedPrompt: str

class SafeGenerateImageResponse(BaseModel):
    """Response for safe image generation with safety handling."""
    imageUrl: str | None = None
    augmentedPrompt: str | None = None
    success: bool
    error: str | None = None
    safety_violation: bool = False
    cleaned_prompt: str | None = None
    
class SwapFaceRequest(BaseModel):
    """Request model for face swap operation."""
    source_url: HttpUrl
    target_url: HttpUrl

class ProcessingStatus(IntEnum):
    """Status of a face swap processing job."""
    QUEUE = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    FAILED = 4

class ProcessedImageResult(BaseModel):
    """Details of a processed image."""
    width: int
    height: int
    type: str
    url: HttpUrl

class SwapFaceResult(BaseModel):
    """Response model for face swap operation."""
    job_id: str
    processed: Optional[ProcessedImageResult] = None
    status: ProcessingStatus
    status_name: str

    @classmethod
    def from_icons8_response(cls, response):
        """Convert Icons8 response to our API response model."""
        return cls(
            job_id=response.id,
            processed=ProcessedImageResult(
                width=response.processed.width,
                height=response.processed.height,
                type=response.processed.type,
                url=response.processed.url
            ) if response.processed else None,
            status=ProcessingStatus(response.status),
            status_name=response.status_name
        )
    
    def to_frontend_response(self) -> dict:
        """Convert to frontend-expected format."""
        if self.status == ProcessingStatus.READY and self.processed:
            return {"url": str(self.processed.url), "status": "complete"}
        elif self.status in (ProcessingStatus.ERROR, ProcessingStatus.FAILED):
            return {"url": "", "status": "error"}
        else:
            return {"url": "", "status": "processing"}
