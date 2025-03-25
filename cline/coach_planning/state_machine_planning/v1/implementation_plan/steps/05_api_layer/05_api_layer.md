# Step 5: API Layer Implementation

## Overview

This step implements a simplified API layer with a single endpoint for coach interaction that handles stateless request/response flow.

## Implementation Details

### FastAPI Implementation

```python
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Import models from service layer
from .service.coach.models import (
    CoachingState,
    CoachState,
    Action,
    ProcessMessageResult
)

class ChatRequest(BaseModel):
    """
    Request body for the chat endpoint.
    Contains the user's message and current state.
    """
    message: str
    state: CoachState

class ChatResponse(BaseModel):
    """
    Response body from the chat endpoint.
    Contains the coach's response, updated state, and any actions taken.
    """
    message: str
    state: CoachState
    actions: List[Action]

app = FastAPI()

@app.post("/api/coach/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return the coach's response.
    
    Args:
        request: ChatRequest containing:
            - message: The user's message
            - state: Current state of the coaching session
            
    Returns:
        ChatResponse containing:
            - message: The coach's response
            - state: Updated coaching state
            - actions: List of actions performed
            
    Raises:
        HTTPException: If message processing fails
    """
    try:
        result = await coach_service.process_message(
            request.message,
            request.state
        )
        
        return ChatResponse(
            message=result.message,
            state=result.state,
            actions=result.actions
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )
```

### Key Components

1. **Request/Response Models**
   - Clear Pydantic models for type safety
   - Complete state included in each request/response
   - Actions returned for frontend processing

2. **Single Endpoint**
   - One endpoint handles all coach interactions
   - Stateless design - all state passed in request
   - Simple error handling with appropriate status codes

3. **Service Integration**
   - Direct integration with CoachService
   - No database or persistence layer
   - Async support for LLM calls

### API Documentation

#### POST /api/coach/chat

Request Body:
```typescript
interface ChatRequest {
  message: string;
  state: {
    currentState: CoachingState;  // Enum value
    userProfile: {
      name: string;
      goals: string[];
    };
    identities: Array<{
      id: string;
      description: string;
      isAccepted: boolean;
    }>;
    currentIdentityIndex: number | null;
    conversationHistory: Array<{
      role: "user" | "coach";
      content: string;
    }>;
    metadata: Record<string, unknown>;
  };
}
```

Response Body:
```typescript
interface ChatResponse {
  message: string;
  state: CoachState;  // Same structure as request state
  actions: Array<{
    type: string;
    params: Record<string, unknown>;
  }>;
}
```

### Testing Strategy

1. **Unit Tests**
   - Test request/response model validation
   - Test error handling
   - Test state updates

2. **Integration Tests**
   - Test complete request flow
   - Test service integration
   - Test error scenarios

3. **API Tests**
   - Test endpoint with various states
   - Test invalid requests
   - Test response formats

## Implementation Steps

1. Create request/response models
2. Implement chat endpoint
3. Add error handling
4. Add API documentation
5. Write comprehensive tests

## Dependencies

- FastAPI for API framework
- Service layer from Step 4
- Pydantic for data validation

## Next Steps

1. Implement frontend integration
2. Add API documentation
3. Add monitoring and logging
