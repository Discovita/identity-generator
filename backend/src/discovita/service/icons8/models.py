"""Data models for Icons8 API interactions."""

from enum import IntEnum
from typing import NewType, Optional, List
from pydantic import BaseModel, AnyHttpUrl, Field, ConfigDict

from .face_selection import BoundingBox

ImageId = NewType("ImageId", str)

class ProcessStatus(IntEnum):
    """Status of a face swap processing job."""
    QUEUE = 0
    PROCESSING = 1
    READY = 2
    ERROR = 3
    FAILED = 4

class Icons8Error(Exception):
    """Icons8 API error."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Icons8 API error: {detail}")

class BoundaryAdjustments(BaseModel):
    """Adjustments for face swapping."""
    emotion_fear: float = 0
    emotion_anger: float = 0
    emotion_disgust: float = 0
    emotion_surprise: float = 0
    emotion_contempt: float = 0
    emotion_happiness: float = 0
    age: float = 0
    gender: float = 0

class FaceTask(BaseModel):
    """Single face swap task configuration."""
    source_url: AnyHttpUrl = Field(..., description="URL of the source image")
    source_landmarks: List[float]
    target_landmarks: List[float]
    boundary_adjustments: BoundaryAdjustments = BoundaryAdjustments()

class ProcessedImage(BaseModel):
    """Details of a processed image."""
    width: int
    height: int
    type: str
    url: AnyHttpUrl = Field(..., description="URL of the processed image")

class FaceSwapResponse(BaseModel):
    """Response model for face swap operation."""
    model_config = ConfigDict(populate_by_name=True)
    
    id: ImageId
    processed: Optional[ProcessedImage] = None
    status: ProcessStatus
    status_name: str = Field(alias="statusName")

class Face(BaseModel):
    """Face detection result."""
    bbox: BoundingBox
    landmarks: List[float]

    @classmethod
    def from_icons8_response(cls, data: dict) -> "Face":
        """Create Face from Icons8 API response."""
        return cls(
            bbox=BoundingBox.from_bbox_list(data["bbox"]),
            landmarks=data["landmarks"]
        )

class RawFace(BaseModel):
    """Raw face detection result from Icons8 API."""
    bbox: List[float]
    landmarks: List[float]

class ImageFaces(BaseModel):
    """Face detection results for an image."""
    img_url: AnyHttpUrl
    faces: List[RawFace]

    def get_face_objects(self) -> List[Face]:
        """Convert raw faces to Face objects."""
        return [Face.from_icons8_response(face.model_dump()) for face in self.faces]

class GetBboxRequest(BaseModel):
    """Request model for get_bbox endpoint."""
    urls: List[AnyHttpUrl]

    def to_json(self) -> dict:
        """Convert model to JSON-serializable dict."""
        return {"urls": [str(url) for url in self.urls]}

class FaceSwapRequest(BaseModel):
    """Request model for face swap operation."""
    target_url: AnyHttpUrl = Field(..., description="URL of the target image")
    face_tasks: List[FaceTask]

    def to_json(self) -> dict:
        """Convert model to JSON-serializable dict."""
        return {
            "target_url": str(self.target_url),
            "face_tasks": [
                {
                    "source_url": str(task.source_url),
                    "source_landmarks": task.source_landmarks,
                    "target_landmarks": task.target_landmarks,
                    "boundary_adjustments": task.boundary_adjustments.model_dump()
                }
                for task in self.face_tasks
            ]
        }

class GetBboxResponse(BaseModel):
    """Response model for get_bbox endpoint."""
    images: List[ImageFaces] = Field(default_factory=list)

    @classmethod
    def model_validate(
        cls,
        obj: List[dict],
        *,
        strict: bool | None = False,
        from_attributes: bool | None = False,
        context: dict | None = None,
    ) -> "GetBboxResponse":
        """Create response from API's array response."""
        return cls(images=[ImageFaces.model_validate(item) for item in obj])
