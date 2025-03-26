"""Models for OpenAI function definitions."""

from typing import List, Optional
from pydantic import BaseModel, Field
from ..models.action import ActionType
from ..models.state import CoachingState

class CreateIdentityParams(BaseModel):
    """Parameters for creating a new identity."""
    description: str = Field(..., description="Description of the identity")

class UpdateIdentityParams(BaseModel):
    """Parameters for updating an identity."""
    id: str = Field(..., description="ID of identity to update")
    description: str = Field(..., description="Updated description")

class AcceptIdentityParams(BaseModel):
    """Parameters for accepting an identity."""
    id: str = Field(..., description="ID of identity to accept")

class TransitionStateParams(BaseModel):
    """Parameters for transitioning state."""
    to_state: CoachingState = Field(..., description="State to transition to")

class FunctionDefinition(BaseModel):
    """OpenAI function definition."""
    type: str = Field(default="function", description="Type of the function")
    name: str = Field(..., description="Name of the function")
    description: str = Field(..., description="Description of the function")
    parameters: dict = Field(..., description="Parameters schema")
