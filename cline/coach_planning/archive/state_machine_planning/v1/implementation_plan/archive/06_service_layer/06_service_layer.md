# Step 6: Update Service Layer

This document outlines the implementation plan for updating the service layer to support the state machine architecture.

## Current Implementation

The current service implementation is straightforward:

```python
class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
        self.context_builder = ContextBuilder()
    
    async def get_response(
        self,
        request: CoachRequest
    ) -> CoachResponse:
        # Build messages with system prompt
        # Get structured completion from OpenAI
        # Return response with proposed/confirmed identities
```

The current service:
- Takes a user message and context
- Builds a prompt with system instructions and context
- Gets a structured response from the LLM
- Returns the response with any proposed or confirmed identities

## Target Implementation

The new service layer will:

1. Integrate all components of the state machine architecture
2. Manage the flow of data between components
3. Provide methods for the API layer to interact with the system
4. Handle state transitions and action execution

## Implementation Details

### 1. New Service Class

The core service class will handle the main coaching interactions:

[06_service_layer_code/service.py](./06_service_layer_code/service.py)

Key methods:
- `process_message`: Process a user message with state management
- `get_state_info`: Get information about the current state
- `create_new_session`: Create a new coaching session
- `reset_session`: Reset a coaching session to initial state

### 2. Service Factory

A factory function to simplify service creation:

[06_service_layer_code/factory.py](./06_service_layer_code/factory.py)

This factory:
- Creates all required component instances
- Wires them together correctly
- Returns a fully configured service

### 3. Error Handling

Robust error handling for the service layer:

[06_service_layer_code/error_handling.py](./06_service_layer_code/error_handling.py)

Features:
- Custom exception types for different error categories
- Error handling function that returns appropriate responses
- Logging of errors for debugging

### 4. Backward Compatibility

Support for the legacy API:

[06_service_layer_code/backward_compatibility.py](./06_service_layer_code/backward_compatibility.py)

This provides:
- A mixin class for backward compatibility
- Conversion between old and new request/response models
- Seamless integration with existing code

## Component Interactions

The service layer orchestrates the interactions between components:

1. **API → Service**: The API layer calls service methods with user requests
2. **Service → Context Manager**: The service uses the context manager to retrieve and update context
3. **Service → State Machine**: The service gets the current state and available actions
4. **Service → Prompt Manager**: The service gets prompts for the current state
5. **Service → LLM Client**: The service sends prompts to the LLM and gets responses
6. **Service → Action Executor**: The service passes LLM responses to the action executor
7. **Service → API**: The service returns responses to the API layer

## Testing Strategy

1. **Unit Tests**:
   - Test each method with mocked dependencies
   - Verify correct interactions between components
   - Test error handling

2. **Integration Tests**:
   - Test the service with real dependencies
   - Verify end-to-end flow
   - Test state transitions and action execution

## Implementation Steps

1. Create the new service class
2. Implement the core methods
3. Add error handling
4. Create factory function
5. Write tests
6. Update dependencies

## Considerations

### Performance

The service should be optimized for performance:

1. Use asynchronous methods for I/O operations
2. Cache frequently used data
3. Minimize database queries
4. Use efficient data structures

### Logging

The service should include comprehensive logging:

```python
async def process_message(
    self,
    request: CoachStateRequest
) -> CoachStateResponse:
    """Process a user message with state management."""
    logger.info(f"Processing message for user {request.user_id}, session {request.session_id}")
    
    # Implementation as above
    
    logger.info(f"Message processed. State: {updated_state.value}")
    return response
```

## Next Steps

After implementing the service layer, we need to:

1. Implement the action system
2. Add persistence layer
3. Update the API layer
4. Update the frontend
