"""Chat message models for coaching service."""

from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
