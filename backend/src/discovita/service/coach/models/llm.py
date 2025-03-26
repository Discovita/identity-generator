"""LLM response models for coaching service."""

from typing import List, Optional
from pydantic import BaseModel, Field
from discovita.service.openai.models.llm_response import LLMResponseModel
from .action import Action

class CoachLLMResponse(LLMResponseModel):
    """
    Response from OpenAI LLM.
    Contains only what we expect the LLM to generate - a message and optional actions.
    The coach service will handle state updates based on these actions.
    """
    message: str = Field(..., description="Coach's response message to show the user")
    actions: List[Action] = Field(
        default_factory=list,
        description="Actions to perform (e.g. create identity, transition state)"
    )
