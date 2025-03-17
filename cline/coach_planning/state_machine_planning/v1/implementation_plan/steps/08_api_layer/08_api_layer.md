# Step 8: Update API Layer

This document outlines the implementation plan for updating the API layer to support the state machine architecture.

## Current Implementation

The current API implementation is minimal:

- Single endpoint `/user_input` that handles all coaching interactions
- Simple request/response model without state management
- Dependency injection for the CoachService

```python
@router.post("/user_input", response_model=CoachResponse)
async def handle_user_input(
    request: CoachRequest,
    service: CoachService = Depends(get_coach_service)
) -> CoachResponse:
    """Handle user input and get coach response."""
    return await service.get_response(request)
```

## Target Implementation

We need to update the API layer to:

1. Support state-aware interactions
2. Provide endpoints for state management
3. Enable action execution
4. Maintain backward compatibility where possible

## Implementation Details

### 1. New Models

Create new request and response models in `models/request_response.py`:

```python
class CoachStateRequest(BaseModel):
    """Request model for state-aware coach API."""
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Session identifier for state tracking")

class CoachStateResponse(BaseModel):
    """Response model for state-aware coach API."""
    message: str = Field(..., description="Coach's response message")
    current_state: str = Field(..., description="Current state of the coaching process")
    proposed_identity: Optional[Identity] = Field(None, description="A single identity being proposed")
    confirmed_identity: Optional[Identity] = Field(None, description="A single identity that has been confirmed")
    visualization_prompt: Optional[Dict] = Field(None, description="Prompt for identity visualization")
    available_actions: List[str] = Field(default_factory=list, description="Actions available in current state")
    session_id: str = Field(..., description="Session identifier for state tracking")

class StateInfoResponse(BaseModel):
    """Response model for state information."""
    current_state: str = Field(..., description="Current state name")
    description: str = Field(..., description="Description of the current state")
    available_actions: List[str] = Field(default_factory=list, description="Actions available in current state")
    next_possible_states: List[str] = Field(default_factory=list, description="Possible next states")
```

### 2. Updated Router

Update the coach router in `api/routes/coach.py`:

```python
"""Coach route handlers."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ...service.coach.models.request_response import (
    CoachStateRequest, 
    CoachStateResponse,
    StateInfoResponse
)
from ...service.coach.service import CoachService
from ..dependencies import get_coach_service

router = APIRouter()

@router.post("/chat", response_model=CoachStateResponse)
async def handle_chat(
    request: CoachStateRequest,
    service: CoachService = Depends(get_coach_service)
) -> CoachStateResponse:
    """Handle user chat message with state management."""
    return await service.process_message(request)

@router.get("/state/{user_id}", response_model=StateInfoResponse)
async def get_state(
    user_id: str,
    session_id: Optional[str] = None,
    service: CoachService = Depends(get_coach_service)
) -> StateInfoResponse:
    """Get current state information for a user."""
    return await service.get_state_info(user_id, session_id)

@router.post("/session/new/{user_id}", response_model=StateInfoResponse)
async def create_session(
    user_id: str,
    service: CoachService = Depends(get_coach_service)
) -> StateInfoResponse:
    """Create a new coaching session."""
    return await service.create_new_session(user_id)

@router.post("/session/reset/{session_id}", response_model=StateInfoResponse)
async def reset_session(
    session_id: str,
    service: CoachService = Depends(get_coach_service)
) -> StateInfoResponse:
    """Reset a coaching session to initial state."""
    return await service.reset_session(session_id)

# Legacy endpoint for backward compatibility
@router.post("/user_input", response_model=CoachStateResponse)
async def handle_user_input(
    request: CoachRequest,
    service: CoachService = Depends(get_coach_service)
) -> CoachStateResponse:
    """Legacy endpoint for backward compatibility."""
    # Convert legacy request to new format
    state_request = CoachStateRequest(
        user_id=request.user_id,
        message=request.message,
        session_id=None  # Will create new session
    )
    return await service.process_message(state_request)
```

### 3. Updated Dependencies

Update the dependencies in `api/dependencies.py`:

```python
async def get_coach_service(
    client: OpenAIClient = Depends(get_openai_client),
    db_service: DatabaseService = Depends(get_database_service)
) -> CoachService:
    """Get coach service with state machine architecture."""
    # Create component instances
    state_machine = CoachStateMachine()
    prompt_manager = PromptManager()
    context_manager = ContextManager(db_service)
    action_executor = ActionExecutor(context_manager, state_machine, db_service)
    
    # Create and return service
    return CoachService(
        client=client,
        state_machine=state_machine,
        prompt_manager=prompt_manager,
        context_manager=context_manager,
        action_executor=action_executor
    )

async def get_database_service(
    settings: Settings = Depends(get_settings)
) -> DatabaseService:
    """Get database service for state persistence."""
    return DatabaseService(connection_string=settings.database_url)
```

## Integration with Frontend

The frontend will need to be updated to work with the new API:

1. Update API client to use the new endpoints
2. Add state visualization in the UI
3. Handle session management
4. Display available actions to the user

## Testing Strategy

1. **Unit Tests**:
   - Test each endpoint with various inputs
   - Verify correct response models
   - Test error handling

2. **Integration Tests**:
   - Test the complete flow from API to service
   - Verify state transitions
   - Test session management

3. **End-to-End Tests**:
   - Test the complete user journey
   - Verify frontend integration

## Implementation Steps

1. Create new request/response models
2. Update the router with new endpoints
3. Update the dependencies
4. Implement the service layer to support the new API
5. Add tests for the new endpoints
6. Update the frontend to use the new API

## Considerations

### Backward Compatibility

The legacy endpoint `/user_input` is maintained for backward compatibility. It converts the old request format to the new format and creates a new session if needed.

### Error Handling

All endpoints should include proper error handling:

```python
@router.get("/state/{user_id}", response_model=StateInfoResponse)
async def get_state(
    user_id: str,
    session_id: Optional[str] = None,
    service: CoachService = Depends(get_coach_service)
) -> StateInfoResponse:
    """Get current state information for a user."""
    try:
        return await service.get_state_info(user_id, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving state: {str(e)}")
```

### Authentication and Authorization

The API should integrate with the existing authentication system. All endpoints should verify that the user has permission to access the requested resources.

### Documentation

Update the API documentation to reflect the new endpoints and models. Include examples of how to use each endpoint.

## Next Steps

After implementing the API layer, we need to:

1. Implement the service layer to support the new API
2. Update the frontend to use the new API
3. Test the complete system
