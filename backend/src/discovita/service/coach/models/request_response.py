"""Request and response models for coaching service."""

from typing import Dict, Optional
from pydantic import BaseModel, Field

from discovita.service.openai.models.llm_response import LLMResponseModel
from .state import CoachState

class CoachRequest(BaseModel):
    """Request model for coach API."""
    message: str = Field(..., description="User's message")
    coach_state: CoachState = Field(..., description="Current state of the coaching session")

class CoachResponse(LLMResponseModel):
    """Response model for coach API."""
    message: str = Field(..., description="Coach's response message")
    coach_state: CoachState = Field(..., description="Updated state of the coaching session")
    final_prompt: str = Field("", description="The final prompt used to generate the coach's response")

class CoachStructuredResponse(LLMResponseModel):
    """Structured response from the coach."""
    message: str = Field(..., description="Main response message to show the user")
    coach_state: CoachState = Field(..., description="Updated state of the coaching session")
