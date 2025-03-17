from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class Action(BaseModel):
    """Model representing an action to be executed."""
    name: str = Field(..., description="Name of the action")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the action")

class ActionResult(BaseModel):
    """Model representing the result of an action execution."""
    action: Action = Field(..., description="The action that was executed")
    success: bool = Field(..., description="Whether the action was successful")
    message: str = Field(..., description="Message describing the result")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data from the action")

class ActionDefinition(BaseModel):
    """Model representing the definition of an available action."""
    name: str = Field(..., description="Name of the action")
    description: str = Field(..., description="Description of what the action does")
    allowed_states: list[str] = Field(default_factory=list, description="States in which this action is allowed")
    required_params: list[str] = Field(default_factory=list, description="Required parameters for this action")
    optional_params: Dict[str, Any] = Field(default_factory=dict, description="Optional parameters with default values")
