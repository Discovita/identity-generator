# Step 4: Service Layer Implementation

## Overview

This step implements a simplified, stateless service layer that manages the coaching process through JSON state objects passed between frontend and backend.

## Implementation Details

### CoachService Class

```python
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Dict, Tuple

class CoachingState(Enum):
    """Represents the possible states in the coaching process."""
    INTRODUCTION = "introduction"
    IDENTITY_BRAINSTORMING = "identity_brainstorming"
    IDENTITY_REFINEMENT = "identity_refinement"

class UserProfile(BaseModel):
    """User information and goals."""
    name: str
    goals: List[str]

class Identity(BaseModel):
    """Represents a single identity with its acceptance status."""
    id: str
    description: str
    is_accepted: bool

class Message(BaseModel):
    """A single message in the conversation history."""
    role: str  # "user" or "coach"
    content: str

class CoachState(BaseModel):
    """
    Complete state of a coaching session.
    This object is passed with each request/response to maintain stateless operation.
    """
    current_state: CoachingState
    user_profile: UserProfile
    identities: List[Identity]
    current_identity_index: Optional[int]
    conversation_history: List[Message]
    metadata: Dict[str, any]

class Action(BaseModel):
    """An action to be performed on the coaching state."""
    type: str
    params: Dict[str, any]

class ProcessMessageResult(BaseModel):
    """
    Result of processing a user message.
    Contains the coach's response, updated state, and any actions taken.
    """
    message: str
    state: CoachState
    actions: List[Action]

class CoachService:
    def __init__(self, state_machine, prompt_manager):
        self.state_machine = state_machine
        self.prompt_manager = prompt_manager

    async def process_message(
        self, 
        message: str, 
        state: CoachState
    ) -> ProcessMessageResult:
        """
        Process a user message and update the coaching state.
        
        Args:
            message: The user's message
            state: Current state of the coaching session
            
        Returns:
            ProcessMessageResult containing:
            - Coach's response message
            - Updated coaching state
            - List of actions performed
            
        The function:
        1. Gets appropriate prompt for current state
        2. Gets LLM response
        3. Extracts and applies any actions
        4. Checks for state transitions
        5. Returns updated state and response
        """
        # Get prompt for current state
        prompt = self.prompt_manager.get_prompt(state)
        
        # Get LLM response
        llm_response = await self.get_llm_response(prompt, message)
        
        # Extract actions from response
        actions = self.parse_actions(llm_response)
        
        # Apply actions to state
        new_state = self.apply_actions(state, actions)
        
        # Check for state transitions
        new_state = self.state_machine.check_transitions(new_state)
        
        return ProcessMessageResult(
            message=llm_response.message,
            state=new_state,
            actions=actions
        )

    async def get_llm_response(
        self, 
        prompt: str, 
        message: str
    ) -> LLMResponse:
        """
        Get response from LLM service.
        
        Args:
            prompt: The system prompt for the current state
            message: The user's message
            
        Returns:
            LLMResponse containing:
            - Response message
            - Any structured data/actions from the response
        """
        pass  # Implementation details...

    def parse_actions(
        self, 
        llm_response: LLMResponse
    ) -> List[Action]:
        """
        Extract actions from LLM response.
        
        Args:
            llm_response: Response from the LLM containing potential actions
            
        Returns:
            List of actions to perform on the state
        """
        pass  # Implementation details...

    def apply_actions(
        self, 
        state: CoachState, 
        actions: List[Action]
    ) -> CoachState:
        """
        Apply actions to modify the coaching state.
        
        Args:
            state: Current coaching state
            actions: List of actions to apply
            
        Returns:
            New state with actions applied
        """
        pass  # Implementation details...
```

### Key Components

1. **CoachState Model**
   - Represents complete coaching session state
   - Passed with each request/response
   - Contains all necessary data for stateless operation

2. **Message Processing**
   - Takes user message and current state
   - Uses prompt manager to get appropriate prompt
   - Gets LLM response
   - Extracts and applies actions
   - Checks for state transitions
   - Returns updated state

3. **Action Handling**
   - Parses structured actions from LLM response
   - Applies actions to modify state
   - No persistence layer interaction

### Testing Strategy

1. **Unit Tests**
   - Test state updates from actions
   - Test state transition checks
   - Test prompt selection

2. **Integration Tests**
   - Test complete message processing flow
   - Test state machine integration
   - Test prompt manager integration

## Implementation Steps

1. Create CoachState model
2. Implement CoachService class
3. Implement action parsing and application
4. Add comprehensive tests
5. Document API and usage

## Dependencies

- State machine from Step 2
- Prompt manager from Step 3
- Pydantic for data validation
- OpenAI client for LLM interaction

## Next Steps

1. Implement API layer to expose service
2. Create frontend state management
3. Add error handling and validation
