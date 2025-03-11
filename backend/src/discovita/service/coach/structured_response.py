"""Structured response models for coach service."""

from typing import List, Optional, Dict
from pydantic import Field
from .models import Identity
from discovita.service.openai.models.llm_response import LLMResponseModel

class CoachStructuredResponse(LLMResponseModel):
    """Structured response from the coach."""
    message: str = Field(..., description="Main response message to show the user")
    identities: Optional[List[Identity]] = Field(
        None,
        description="List of suggested identities if any were discussed"
    )
