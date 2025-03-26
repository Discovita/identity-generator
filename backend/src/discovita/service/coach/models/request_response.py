"""Request and response models for coaching service."""

from typing import Dict, List, Optional

from discovita.service.openai.models.llm_response import LLMResponseModel
from pydantic import BaseModel, Field

from .chat import ChatMessage
from .identity import Identity
from .user import UserProfile


class CoachRequest(BaseModel):
    """Request model for coach API."""

    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="User's message")
    context: List[ChatMessage] = Field(
        default_factory=list, description="Previous chat context"
    )
    profile: Optional[UserProfile] = Field(None, description="User's identity profile")


class CoachResponse(LLMResponseModel):
    """Response model for coach API."""

    message: str = Field(..., description="Coach's response message")
    proposed_identity: Optional[Identity] = Field(
        None, description="A single identity being proposed for user confirmation"
    )
    confirmed_identity: Optional[Identity] = Field(
        None,
        description="A single identity that has been confirmed by the user in this response",
    )
    visualization_prompt: Optional[Dict] = Field(
        None, description="Prompt for identity visualization"
    )


class CoachStructuredResponse(LLMResponseModel):
    """Structured response from the coach."""

    message: str = Field(..., description="Main response message to show the user")
    proposed_identity: Optional[Identity] = Field(
        None, description="A single identity being proposed for user confirmation"
    )
    confirmed_identity: Optional[Identity] = Field(
        None,
        description="A single identity that has been confirmed by the user in this response",
    )
