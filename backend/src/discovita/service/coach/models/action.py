"""Action models for coaching service."""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from discovita.service.openai.models.llm_response import LLMResponseModel

class ActionType(str, Enum):
    """Types of actions that can be performed on the coaching state."""
    CREATE_IDENTITY = "create_identity"  # Create a new identity during brainstorming
    UPDATE_IDENTITY = "update_identity"  # Update an identity during refinement
    ACCEPT_IDENTITY = "accept_identity"  # Mark an identity as accepted
    COMPLETE_INTRODUCTION = "complete_introduction"  # Mark introduction as complete
    TRANSITION_STATE = "transition_state"  # Request state transition

class Action(BaseModel):
    """An action to be performed on the coaching state."""
    type: ActionType = Field(..., description="Type of action to perform")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the action")

class ProcessMessageResult(LLMResponseModel):
    """
    Result of processing a user message.
    Contains the coach's response, updated state, and any actions taken.
    """
    message: str = Field(..., description="Coach's response message")
    state: "CoachState" = Field(..., description="Updated coaching state")  # Forward reference
    actions: List[Action] = Field(default_factory=list, description="Actions performed")

# Import at bottom to avoid circular imports
from .state import CoachState
ProcessMessageResult.model_rebuild()  # Update forward refs
