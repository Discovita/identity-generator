"""Request and response models for coaching service."""

from pydantic import BaseModel, Field

from .state import CoachState


class CoachRequest(BaseModel):
    """Request model for coach API."""

    message: str = Field(..., description="User's message")
    coach_state: CoachState = Field(
        ..., description="Current state of the coaching session"
    )


class CoachResponse(BaseModel):
    """Response model for coach API."""

    message: str = Field(..., description="Coach's response message")
    coach_state: CoachState = Field(
        ..., description="Updated state of the coaching session"
    )
    final_prompt: str = Field(
        "", description="The final prompt used to generate the coach's response"
    )


class CoachStructuredResponse(BaseModel):
    """Structured response from the coach."""

    message: str = Field(..., description="Main response message to show the user")
    coach_state: CoachState = Field(
        ..., description="Updated state of the coaching session"
    )
