# Simplified Implementation Plan

## Overview

This plan simplifies the coaching system to focus on a streamlined 3-phase process:
1. Introduction phase
2. Identity brainstorming (gathering 5 identities)
3. Identity refinement (walking through each identity until accepted)

The system will maintain state through a JSON object passed between frontend and backend, rather than using a persistence layer.

## Keeping Existing Components (Steps 1-3)

### Step 1: Core Models
- Keep existing models but simplify states to match 3-phase process
- Update CoachingState enum to only include:
  - INTRODUCTION
  - IDENTITY_BRAINSTORMING
  - IDENTITY_REFINEMENT
- Keep Action, ActionResult, and CoachContext models as is

### Step 2: State Machine
- Keep existing state machine implementation
- Update transitions to match simplified states:
  - INTRODUCTION → IDENTITY_BRAINSTORMING (when introduction complete)
  - IDENTITY_BRAINSTORMING → IDENTITY_REFINEMENT (when 5 identities collected)
  - IDENTITY_REFINEMENT → IDENTITY_BRAINSTORMING (when current identity accepted)
- Remove unused transition conditions

### Step 3: Prompt Manager
- Keep existing prompt manager implementation
- Update prompts to match simplified states
- Remove prompts for removed states
- Update examples to match new flow

## New Implementation Steps

### Step 4: Simplified Service Layer
- Create new CoachService class that:
  - Takes a JSON state object with each request
  - Uses state machine to manage flow
  - Returns updated JSON state with each response
- Remove all persistence-related code
- Define request/response models for the API

### Step 5: API Layer
- Create single endpoint for coach interaction
- Request body includes:
  - User message
  - Current state JSON
- Response includes:
  - Coach message
  - Updated state JSON
  - Any actions taken

### Step 6: Frontend Integration
- Create CoachContext component to manage state
- Store full state JSON in React state
- Pass state with each API request
- Update UI based on current state
- Show progress through the 3 phases

## Implementation Details

### State JSON Structure
```typescript
interface CoachState {
  currentState: "INTRODUCTION" | "IDENTITY_BRAINSTORMING" | "IDENTITY_REFINEMENT";
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
}
```

### API Endpoints

#### POST /api/coach/chat
Request:
```typescript
interface ChatRequest {
  message: string;
  state: CoachState;
}
```

Response:
```typescript
interface ChatResponse {
  message: string;
  state: CoachState;
  actions: Array<{
    type: string;
    params: Record<string, unknown>;
  }>;
}
```

### Frontend Components

1. ChatInterface
   - Displays conversation
   - Handles message input
   - Shows current phase

2. IdentityList
   - Shows collected identities
   - Indicates current identity being refined
   - Shows acceptance status

3. ProgressIndicator
   - Shows current phase
   - Shows progress (e.g., X/5 identities)

## Testing Strategy

1. Unit Tests
   - Test state transitions
   - Test prompt generation
   - Test state updates

2. Integration Tests
   - Test complete flows through all phases
   - Test state maintenance
   - Test action handling

3. Frontend Tests
   - Test state management
   - Test UI updates
   - Test API integration

## Migration Plan

1. Create new branch for simplified implementation
2. Keep Steps 1-3 implementation
3. Remove persistence layer code
4. Implement new service layer
5. Update API layer
6. Create new frontend components
7. Test complete flow
8. Document changes

## Next Steps

1. Update core models for simplified states
2. Modify state machine transitions
3. Update prompt templates
4. Begin implementing simplified service layer
