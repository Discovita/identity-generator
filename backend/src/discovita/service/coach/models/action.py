"""Action models for coaching service."""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
class ActionType(str, Enum):
    """Types of actions that can be performed on the coaching state."""
    CREATE_IDENTITY = "create_identity"  # Create a new identity during brainstorming
    UPDATE_IDENTITY = "update_identity"  # Update an identity during refinement
    ACCEPT_IDENTITY = "accept_identity"  # Mark an identity as accepted (from PROPOSED to ACCEPTED)
    ACCEPT_IDENTITY_REFINEMENT = "accept_identity_refinement"  # Mark an identity as refinement complete (from ACCEPTED to REFINEMENT_COMPLETE)
    ADD_IDENTITY_NOTE = "add_identity_note"  # Add a note to an identity
    TRANSITION_STATE = "transition_state"  # Request state transition
    SELECT_IDENTITY_FOCUS = "select_identity_focus"  # Select an identity to focus on during refinement
    

class Action(BaseModel):
    """An action to be performed on the coaching state."""
    type: ActionType = Field(..., description="Type of action to perform")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the action")

class ProcessMessageResult(BaseModel):
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
