"""State models for coaching service."""

from enum import Enum, auto
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

class TransitionCondition(str, Enum):
    """Conditions for state transitions."""
    INTRODUCTION_COMPLETED = "introduction_completed"
    HAS_DRAFT_IDENTITIES = "has_draft_identities"
    HAS_MINIMUM_IDENTITIES = "has_minimum_identities"
    HAS_REFINED_IDENTITY = "has_refined_identity"
    HAS_VISUALIZATION = "has_visualization"
    HAS_ACTION_PLAN = "has_action_plan"
    ALWAYS = "always"

class ContextMetadataKey(str, Enum):
    """Keys for context metadata dictionary."""
    INTRODUCTION_COMPLETED = "introduction_completed"
    DRAFT_IDENTITIES = "draft_identities"
    CURRENT_IDENTITY_REFINED = "current_identity_refined"
    CURRENT_IDENTITY_VISUALIZED = "current_identity_visualized"
    ACTION_ITEMS = "action_items"

class StateTransition(BaseModel):
    """Model for state transitions in the coaching process."""
    from_state: CoachingState = Field(..., description="Starting state")
    to_state: CoachingState = Field(..., description="Target state")
    condition_name: TransitionCondition = Field(..., description="Condition for the transition")
    priority: int = Field(0, description="Priority for resolving multiple valid transitions")
    
    model_config = ConfigDict(frozen=True)  # Make instances immutable
