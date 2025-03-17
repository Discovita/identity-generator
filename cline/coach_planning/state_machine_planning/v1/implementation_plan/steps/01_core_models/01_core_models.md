# Step 1: Define Core Models

This document details the implementation of the core models needed for the state machine architecture.

## Overview

The core models provide the foundation for the entire state machine architecture. They define:

1. The possible states in the coaching process
2. The structure of state transitions
3. The format of actions that can be triggered
4. The context data structure used throughout the system

## Implementation Details

### 1. CoachingState Enum

Create a new file `models/state.py` with the `CoachingState` enum:

```python
from enum import Enum

class CoachingState(Enum):
    """States in the coaching process."""
    INTRODUCTION = "introduction"
    IDENTITY_BRAINSTORMING = "identity_brainstorming"
    IDENTITY_REFINEMENT = "identity_refinement"
    IDENTITY_VISUALIZATION = "identity_visualization"
    ACTION_PLANNING = "action_planning"
    ACCOUNTABILITY = "accountability"
```

### 2. StateTransition Model

In the same file, define the `StateTransition` model:

```python
from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel, Field

class StateTransition(BaseModel):
    """Model for state transitions in the coaching process."""
    from_state: CoachingState = Field(..., description="Starting state")
    to_state: CoachingState = Field(..., description="Target state")
    condition_name: str = Field(..., description="Name of the condition function")
    priority: int = Field(0, description="Priority for resolving multiple valid transitions")
    
    class Config:
        frozen = True  # Make instances immutable
```

Note: We're using a string reference to the condition function rather than storing the function itself, as Pydantic models need to be serializable.

### 3. Action Models

Create a new file `models/action.py` with the action-related models:

```python
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
```

### 4. Context Model

Create a new file `models/context.py` with the context model:

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .chat import ChatMessage
from .user import UserProfile
from .state import CoachingState

class CoachContext(BaseModel):
    """Context for the coaching process."""
    user_id: str = Field(..., description="Unique identifier for the user")
    current_state: CoachingState = Field(
        default=CoachingState.INTRODUCTION, 
        description="Current state in the coaching process"
    )
    conversation_history: List[ChatMessage] = Field(
        default_factory=list, 
        description="Recent conversation history"
    )
    consolidated_summary: str = Field(
        "", 
        description="Summary of older conversation history"
    )
    user_profile: Optional[UserProfile] = Field(
        None, 
        description="User's profile information"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata for the coaching process"
    )
    
    def get_prompt_context(self) -> Dict[str, Any]:
        """Get context formatted for prompt templates."""
        # Format the conversation history
        recent_messages = "\n\n".join(
            f"{msg.role.capitalize()}: {msg.content}" 
            for msg in self.conversation_history
        )
        
        # Format identities if available
        identities_str = ""
        if self.user_profile and self.user_profile.identities:
            identities_str = "\n".join(
                f"- {i.category.name}: {i.name}" 
                for i in self.user_profile.identities
            )
        
        # Format current focus if available
        current_focus = "None"
        if self.user_profile and self.user_profile.current_focus:
            current_focus = self.user_profile.current_focus.name
        
        return {
            "user_summary": self.consolidated_summary,
            "recent_messages": recent_messages,
            "identities": identities_str,
            "current_focus": current_focus,
            "state": self.current_state.value,
            **self.metadata  # Include any additional metadata
        }
```

### 5. Update `__init__.py` Files

Update the `models/__init__.py` file to expose the new models:

```python
from .chat import ChatMessage
from .identity import Identity, IdentityCategory
from .request_response import CoachRequest, CoachResponse, CoachStructuredResponse
from .user import UserProfile
from .state import CoachingState, StateTransition
from .action import ActionType, Action, ActionResult
from .context import CoachContext

__all__ = [
    'ChatMessage',
    'Identity',
    'IdentityCategory',
    'CoachRequest',
    'CoachResponse',
    'CoachStructuredResponse',
    'UserProfile',
    'CoachingState',
    'StateTransition',
    'ActionType',
    'Action',
    'ActionResult',
    'CoachContext'
]
```

## Testing

Create a test file `test/service_coach/test_models.py` with tests for the new models:

```python
import pytest
from pydantic import ValidationError

from discovita.service.coach.models import (
    CoachingState,
    StateTransition,
    ActionType,
    Action,
    ActionResult,
    CoachContext,
    ChatMessage,
    UserProfile
)

def test_coaching_state_enum():
    """Test the CoachingState enum."""
    assert CoachingState.INTRODUCTION.value == "introduction"
    assert CoachingState.IDENTITY_BRAINSTORMING.value == "identity_brainstorming"
    # Test other states...

def test_state_transition_model():
    """Test the StateTransition model."""
    # Valid transition
    transition = StateTransition(
        from_state=CoachingState.INTRODUCTION,
        to_state=CoachingState.IDENTITY_BRAINSTORMING,
        condition_name="introduction_completed",
        priority=1
    )
    assert transition.from_state == CoachingState.INTRODUCTION
    assert transition.to_state == CoachingState.IDENTITY_BRAINSTORMING
    assert transition.condition_name == "introduction_completed"
    assert transition.priority == 1
    
    # Invalid transition (missing required field)
    with pytest.raises(ValidationError):
        StateTransition(
            from_state=CoachingState.INTRODUCTION,
            to_state=CoachingState.IDENTITY_BRAINSTORMING
        )

def test_action_model():
    """Test the Action model."""
    # Valid action
    action = Action(
        type=ActionType.SAVE_USER_INFO,
        params={"key": "goals", "value": "Improve work-life balance"}
    )
    assert action.type == ActionType.SAVE_USER_INFO
    assert action.params["key"] == "goals"
    
    # Action with default empty params
    action = Action(type=ActionType.MARK_INTRODUCTION_COMPLETE)
    assert action.params == {}

def test_action_result_model():
    """Test the ActionResult model."""
    # Successful result
    result = ActionResult(
        success=True,
        message="User info saved",
        data={"key": "goals"}
    )
    assert result.success is True
    assert "saved" in result.message
    assert result.data["key"] == "goals"
    
    # Failed result
    result = ActionResult(
        success=False,
        message="Failed to save user info"
    )
    assert result.success is False
    assert "Failed" in result.message
    assert result.data is None

def test_coach_context_model():
    """Test the CoachContext model."""
    # Create a basic context
    context = CoachContext(
        user_id="user123",
        current_state=CoachingState.INTRODUCTION,
        conversation_history=[
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there")
        ]
    )
    assert context.user_id == "user123"
    assert context.current_state == CoachingState.INTRODUCTION
    assert len(context.conversation_history) == 2
    
    # Test get_prompt_context method
    prompt_context = context.get_prompt_context()
    assert "User: Hello" in prompt_context["recent_messages"]
    assert "Assistant: Hi there" in prompt_context["recent_messages"]
    assert prompt_context["state"] == "introduction"
```

## Next Steps

After implementing these core models:

1. Run the tests to ensure everything works as expected
2. Proceed to implementing the state machine in Step 2
3. Update any existing code that will use these models
