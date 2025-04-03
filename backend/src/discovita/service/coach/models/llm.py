"""LLM response models for coaching service."""

from typing import List, Optional

from pydantic import BaseModel, Field

from .action import Action


class CoachLLMResponse(BaseModel):
    """
    Response from OpenAI LLM.
    Contains only what we expect the LLM to generate - a message and optional actions.
    The coach service will handle state updates based on these actions.
    """

    message: str
    actions: Optional[List[Action]] = Field(
        description="List of actions to be applied to the coaching state",
    )
