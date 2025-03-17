"""Action models for coaching service."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class ActionType(str, Enum):
    """Types of actions that can be triggered by the coach."""
    SAVE_USER_INFO = "save_user_info"
    SAVE_IDENTITY = "save_identity"
    MARK_INTRODUCTION_COMPLETE = "mark_introduction_complete"
    TRANSITION_STATE = "transition_state"
    SAVE_VISUALIZATION = "save_visualization"
    SET_FOCUS_IDENTITY = "set_focus_identity"
    CREATE_ACTION_ITEM = "create_action_item"
    MARK_ACTION_COMPLETE = "mark_action_complete"

class Action(BaseModel):
    """Model for an action triggered by the coach."""
    type: ActionType = Field(..., description="Type of action")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the action")

class ActionResult(BaseModel):
    """Result of executing an action."""
    success: bool = Field(..., description="Whether the action was successful")
    message: str = Field("", description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Any data returned by the action")
