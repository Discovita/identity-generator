# State Machine Implementation Plan

This document outlines the step-by-step implementation plan for integrating the state machine architecture into our coach service. The plan adapts the conceptual architecture from `master_plan_v1.md` to our specific codebase structure.

## Current Architecture Overview

Our current coach service implementation:

- Uses a simple request-response model without persistent state management
- Relies on a single system prompt with limited context management
- Handles identity proposals and confirmations through structured responses
- Lacks a formal state transition mechanism for guiding the coaching process

## Target Architecture

We will implement a state machine-based architecture that:

1. Maintains coaching state across sessions
2. Uses state-specific prompts and allowed actions
3. Manages conversation context more effectively
4. Enables structured actions triggered by the LLM
5. Provides a clear coaching flow with defined transitions

## Implementation Strategy

Our implementation will follow these principles:

1. **Complete Replacement**: We'll completely replace the existing implementation with the new state machine architecture
2. **Strong Typing**: All components will use Pydantic models with clear type definitions
3. **Modular Design**: Each component will be under 100 lines with clear responsibilities
4. **Test-Driven Development**: We'll write tests for each component before implementation

## High-Level Steps

1. **Define Core Models**: Create Pydantic models for states, transitions, actions, and context
2. **Implement State Machine**: Build the state transition engine
3. **Create Prompt Manager**: Develop state-specific prompt templates
4. **Enhance Context Management**: Improve conversation history handling
5. **Build Action System**: Implement the action parsing and execution
6. **Update API Layer**: Integrate the new components with the existing API
7. **Add Persistence Layer**: Implement state and context persistence
8. **Update Frontend**: Update the frontend to work with the new backend

## Detailed Implementation Plan

### Step 1: Define Core Models
[Details: steps/01_core_models.md]

- Create `CoachingState` enum
- Define `StateTransition` model
- Create `Action` and `ActionResult` models
- Define `CoachContext` model for state machine context

### Step 2: Implement State Machine
[Details: steps/02_state_machine.md]

- Implement `CoachStateMachine` class
- Define state transitions and conditions
- Create state persistence mechanism
- Write tests for state transitions

### Step 3: Create Prompt Manager
[Details: steps/03_prompt_manager.md]

- Define `PromptTemplate` model
- Implement `PromptManager` class
- Create state-specific prompt templates
- Add examples and counter-examples for each state

### Step 4: Enhance Context Management
[Details: steps/04_context_manager.md]

- Implement `ContextManager` class
- Add context consolidation for long conversations
- Create user profile tracking
- Integrate with existing identity models

### Step 5: Build Action System
[Details: steps/05_action_system.md]

- Implement `ActionExecutor` class
- Define action handlers for each action type
- Create action parsing from LLM responses
- Add validation against allowed actions per state

### Step 6: Update Service Layer
[Details: steps/06_service_layer.md]

- Create new `CoachService` class (replacing the existing one)
- Integrate state machine, prompt manager, context manager, and action executor
- Implement the new service flow
- Add new endpoints for state management

### Step 7: Add Persistence Layer
[Details: steps/07_persistence_layer.md]

- Define database models for state and context
- Implement repository pattern for data access
- Add state recovery for continuing sessions
- Create data storage strategy

### Step 8: Update API Layer
[Details: steps/08_api_layer.md]

- Replace existing API routes with new implementation
- Add endpoints for state management
- Create response models for state information
- Update documentation

### Step 9: Frontend Integration
[Details: steps/09_frontend_integration.md]

- Update TypeScript types for new API responses
- Add state visualization in UI
- Implement state-aware UI components
- Create transitions between states

## Implementation Considerations

### Code Organization

The new components will be organized as follows:

```
backend/src/discovita/service/coach/
├── models/
│   ├── __init__.py
│   ├── chat.py           # Chat message models
│   ├── identity.py       # Identity models
│   ├── request_response.py # API request/response models
│   ├── user.py           # User profile models
│   ├── state.py          # New: State-related models
│   ├── action.py         # New: Action-related models
│   └── context.py        # New: Context-related models
├── state/
│   ├── __init__.py
│   ├── machine.py        # State machine implementation
│   ├── transitions.py    # State transition definitions
│   └── persistence.py    # State persistence
├── prompt/
│   ├── __init__.py
│   ├── manager.py        # Prompt manager implementation
│   ├── templates.py      # Prompt template definitions
│   └── examples.py       # Example conversations
├── action/
│   ├── __init__.py
│   ├── executor.py       # Action executor implementation
│   ├── handlers.py       # Action handler implementations
│   └── parser.py         # Action parsing from LLM responses
├── context/
│   ├── __init__.py
│   ├── manager.py        # Context manager implementation
│   └── consolidation.py  # Context consolidation logic
└── service.py            # New service implementation
```

### Testing Strategy

For each component, we will:

1. Write unit tests for core functionality
2. Create integration tests for component interactions
3. Develop end-to-end tests for complete flows

## Next Steps

1. Create the detailed implementation docs for each step
2. Set up project tracking for implementation tasks
3. Begin implementation with core models and state machine
4. Establish regular review checkpoints
