"""Action models for coaching service."""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class ActionType(Enum):
    """Types of actions that can be performed on the coaching state."""

    CREATE_IDENTITY = "create_identity"  # Create a new identity during brainstorming
    UPDATE_IDENTITY = "update_identity"  # Update an identity during refinement
    ACCEPT_IDENTITY = (
        "accept_identity"  # Mark an identity as accepted (from PROPOSED to ACCEPTED)
    )
    ACCEPT_IDENTITY_REFINEMENT = "accept_identity_refinement"  # Mark an identity as refinement complete (from ACCEPTED to REFINEMENT_COMPLETE)
    ADD_IDENTITY_NOTE = "add_identity_note"  # Add a note to an identity
    TRANSITION_STATE = "transition_state"  # Request state transition
    SELECT_IDENTITY_FOCUS = (
        "select_identity_focus"  # Select an identity to focus on during refinement
    )


class Param(BaseModel):
    """Parameter for an action."""

    name: str = Field(description="Name of the parameter")
    value: Union[str, int, float] = Field(description="Value of the parameter")


class Action(BaseModel):
    """An action to be performed on the coaching state."""

    type: ActionType = Field(description="Type of action to perform")
    params: List[Param] = Field(description="Parameters for the action")

    model_config = {
        "use_enum_values": True,
    }


class ProcessMessageResult(BaseModel):
    """
    Result of processing a user message.
    Contains the coach's response, updated state, any actions taken, and the final prompt used.
    """

    message: str = Field(..., description="Coach's response message")
    state: "CoachState" = Field(
        description="Updated coaching state"
    )  # Forward reference
    actions: Optional[List[Action]] = Field(description="Actions performed")
    final_prompt: str = Field(
        description="The final prompt used to generate the coach's response"
    )


# Import at bottom to avoid circular imports
from .state import CoachState

ProcessMessageResult.model_rebuild()  # Update forward refs
