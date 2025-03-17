"""State models for coaching service."""

from enum import Enum
from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class CoachingState(Enum):
    """States in the coaching process."""
    INTRODUCTION = "introduction"
    IDENTITY_BRAINSTORMING = "identity_brainstorming"
    IDENTITY_REFINEMENT = "identity_refinement"
    IDENTITY_VISUALIZATION = "identity_visualization"
    ACTION_PLANNING = "action_planning"
    ACCOUNTABILITY = "accountability"

class StateTransition(BaseModel):
    """Model for state transitions in the coaching process."""
    from_state: CoachingState = Field(..., description="Starting state")
    to_state: CoachingState = Field(..., description="Target state")
    condition_name: str = Field(..., description="Name of the condition function")
    priority: int = Field(0, description="Priority for resolving multiple valid transitions")
    
    model_config = ConfigDict(frozen=True)  # Make instances immutable
