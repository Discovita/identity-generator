# Step 4B: Enhance Context Management

This document details the implementation of the context manager component for the coaching system, which builds upon the persistence layer implemented in Step 4A.

## Overview

The context manager is responsible for:

1. Maintaining conversation history across user sessions
2. Consolidating older messages into summaries to manage token usage
3. Tracking user data including identities and progress
4. Providing formatted context for prompt templates
5. Leveraging the persistence layer to store and retrieve context data

## Implementation Details

### 1. Create Context Manager Directory Structure

First, create the directory structure for the context manager components:

```
backend/src/discovita/service/coach/context/
├── __init__.py
├── manager.py        # Context manager implementation
└── models.py         # Context-specific models and conversion utilities
```

### 2. Implement Context Manager Class

The context manager handles maintaining conversation history and user data. See [manager.py](./manager.py) for implementation details.

Key features:
- Loads and creates user context using the persistence layer
- Adds messages to conversation history
- Consolidates older messages into summaries
- Updates user profile and metadata
- Converts between domain models and persistence models

### 3. Implement Model Conversions

Create utilities to convert between domain models and persistence models. See [models.py](./models.py) for implementation details.

Key features:
- Conversion between `CoachContext` and `ContextRecord`
- Serialization and deserialization of complex types
- Type safety with Pydantic models

### 4. Service Integration

The context manager integrates with the coach service to provide stateful conversations. See [service_integration.py](./service_integration.py) for implementation details.

Key features:
- Initializes the persistence layer using the factory
- Loads user context at the start of each request
- Updates context with new messages
- Provides context for prompt formatting
- Executes actions that modify context
- Persists context at the end of each request

## API Flow with Context Manager

The context manager plays a central role in the coach API flow:

1. **Request Handling**:
   - When a request comes in, the service loads the user's context from the persistence layer
   - If no context exists, a new one is created with the initial state
   - The user's message is added to the conversation history

2. **State-Based Prompting**:
   - The current state from the context determines which prompt to use
   - The context manager formats the context for the prompt template
   - This includes recent messages, consolidated history, and user profile

3. **LLM Interaction**:
   - The formatted prompt is sent to the LLM
   - The LLM response includes structured data (identities, actions)
   - The assistant's response is added to the conversation history

4. **Action Execution**:
   - Actions extracted from the LLM response modify the context
   - For example, saving identities or marking steps as complete
   - These context changes trigger state transitions

5. **State Transitions**:
   - The state machine evaluates transitions based on context
   - If conditions are met, the state is updated in the context
   - The new state will be used for the next request

6. **Context Persistence**:
   - At the end of the request, the updated context is saved to the persistence layer
   - This ensures continuity across user sessions
   - The context includes conversation history, state, and user data

7. **Response Formation**:
   - The response includes the current state from the context
   - This allows the frontend to adapt the UI based on state

## Context Consolidation

To manage token usage in long conversations, the context manager implements a consolidation mechanism:

1. When the conversation history exceeds a threshold, older messages are summarized
2. The LLM generates a summary of key information from these messages
3. This summary is stored in the consolidated_summary field
4. The summary is included in prompts to provide long-term context
5. Only recent messages are kept in full in the conversation history

This approach balances comprehensive context with token efficiency.

## Context Data Structure

The `CoachContext` model includes:

```python
class CoachContext(BaseModel):
    user_id: str
    session_id: str  # Added to align with persistence layer
    current_state: CoachingState
    conversation_history: List[ChatMessage]
    consolidated_summary: str
    user_profile: Optional[UserProfile]
    metadata: Dict[str, Any]
```

The `metadata` field stores state-specific data that influences transitions:
- `introduction_completed`: Boolean flag for completing introduction
- `draft_identities`: List of identities being worked on
- `current_identity_refined`: Boolean flag for identity refinement
- `current_identity_visualized`: Boolean flag for visualization
- `action_items`: List of action items for the user

## Integration with Persistence Layer

The context manager uses the persistence layer (Step 4A) for storing and retrieving context data:

```python
class ContextManager:
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface,  # Database interface from persistence layer
        max_recent_messages: int = 10
    ):
        self.llm_client = llm_client
        self.db = db
        self.max_recent_messages = max_recent_messages
    
    async def load_context(self, user_id: str, session_id: str) -> CoachContext:
        """Load or create context for a user session."""
        # Try to load existing context from persistence layer
        context_record = await self.db.get_context(user_id, session_id)
        
        # If no existing context, create a new one
        if not context_record:
            return self._create_new_context(user_id, session_id)
        
        # Convert from persistence model to domain model
        return self._convert_to_coach_context(context_record)
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context to persistence layer."""
        # Convert from domain model to persistence model
        context_record = self._convert_to_context_record(context)
        
        # Save to persistence layer
        await self.db.save_context(context_record)
```

## Next Steps

After implementing the context manager:

1. Ensure it integrates well with the state machine and prompt manager
2. Implement the action system in Step 5
3. Update the API layer to use the new stateful service
