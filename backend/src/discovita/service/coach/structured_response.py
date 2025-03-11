"""Structured response models for coach service."""

from typing import List, Optional, Dict
from pydantic import Field
from .models import Identity
from discovita.service.openai.models.llm_response import LLMResponseModel

class CoachStructuredResponse(LLMResponseModel):
    """Structured response from the coach."""
    message: str = Field(..., description="Main response message to show the user")
    proposed_identity: Optional[Identity] = Field(
        None,
        description="A single identity being proposed for user confirmation"
    )
    confirmed_identity: Optional[Identity] = Field(
        None,
        description="A single identity that has been confirmed by the user in this response"
    )
