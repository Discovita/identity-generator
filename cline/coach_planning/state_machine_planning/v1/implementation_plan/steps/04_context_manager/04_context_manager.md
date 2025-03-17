# Step 4: Enhance Context Management

This document details the implementation of the context manager component for the coaching system.

## Overview

The context manager is responsible for:

1. Maintaining conversation history across user sessions
2. Consolidating older messages into summaries to manage token usage
3. Tracking user data including identities and progress
4. Providing formatted context for prompt templates
5. Persisting state between sessions

## Implementation Details

### 1. Create Context Manager Directory Structure

First, create the directory structure for the context manager components:

```
backend/src/discovita/service/coach/context/
├── __init__.py
├── manager.py        # Context manager implementation
├── persistence.py    # Context persistence
└── data/             # Directory for storing context data (for file-based persistence)
```

### 2. Implement Context Manager Class

The context manager handles maintaining conversation history and user data. See [manager.py](./04_context_manager/code/manager.py) for implementation details.

Key features:
- Loads and creates user context
- Adds messages to conversation history
- Consolidates older messages into summaries
- Updates user profile and metadata
- Integrates with persistence layer

### 3. Implement Context Persistence

The persistence layer handles saving and loading context. See [persistence.py](./04_context_manager/code/persistence.py) for implementation details.

Key features:
- Interface for different persistence implementations
- File-based persistence for development
- Database persistence for production
- Asynchronous operations to avoid blocking

### 4. Service Integration

The context manager integrates with the coach service to provide stateful conversations. See [service_integration.py](./04_context_manager/code/service_integration.py) for implementation details.

Key features:
- Loads user context at the start of each request
- Updates context with new messages
- Provides context for prompt formatting
- Executes actions that modify context
- Persists context at the end of each request

## API Flow with Context Manager

The context manager plays a central role in the coach API flow:

1. **Request Handling**:
   - When a request comes in, the service loads the user's context
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
   - At the end of the request, the updated context is saved
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

## Next Steps

After implementing the context manager:

1. Ensure it integrates well with the state machine and prompt manager
2. Implement the action system in Step 5
3. Update the API layer to use the new stateful service
