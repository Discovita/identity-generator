"""Data models for coaching service."""

from typing import List
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")

class CoachRequest(BaseModel):
    """Request model for coach API."""
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="User's message")
    context: List[ChatMessage] = Field(default_factory=list, description="Previous chat context")

class CoachResponse(BaseModel):
    """Response model for coach API."""
    message: str = Field(..., description="Coach's response message")
