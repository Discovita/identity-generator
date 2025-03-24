# State Machine Implementation Plan (Revised)

This document outlines the revised step-by-step implementation plan for integrating the state machine architecture into our coach service. The plan adapts the conceptual architecture from `master_plan_v1.md` to our specific codebase structure, with updated component interactions and step ordering.

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
6. Persists state and context across sessions

## Implementation Strategy

Our implementation will follow these principles:

1. **Complete Replacement**: We'll completely replace the existing implementation with the new state machine architecture
2. **Strong Typing**: All components will use Pydantic models with clear type definitions
3. **Modular Design**: Each component will be under 100 lines with clear responsibilities
4. **Test-Driven Development**: We'll write tests for each component before implementation
5. **Clear Separation of Concerns**: Each component will have a well-defined responsibility
6. **Dependency Injection**: Components will accept dependencies through their constructors

## High-Level Steps

1. **Define Core Models**: Create Pydantic models for states, transitions, actions, and context
2. **Implement State Machine**: Build the state transition engine
3. **Create Prompt Manager**: Develop state-specific prompt templates
4. **Add Persistence Layer (4A)**: Implement data storage for state, context, and identities
5. **Enhance Context Management (4B)**: Improve conversation history handling using the persistence layer
6. **Build Action System**: Implement the action parsing and execution
7. **Update Service Layer**: Integrate the new components with the existing API
8. **Update API Layer**: Integrate the new components with the existing API
9. **Update Frontend**: Update the frontend to work with the new backend

## Detailed Implementation Plan

### Step 1: Define Core Models
[Details: steps/01_core_models.md]

- Create `CoachingState` enum
- Define `StateTransition` model
- Create `Action` and `ActionResult` models
- Define `CoachContext` model for state machine context
- Create persistence models for database storage

### Step 2: Implement State Machine
[Details: steps/02_state_machine.md]

- Implement `CoachStateMachine` class
- Define state transitions and conditions
- Create state validation mechanism
- Write tests for state transitions
- Define allowed actions for each state

### Step 3: Create Prompt Manager
[Details: steps/03_prompt_manager.md]

- Define `PromptTemplate` model
- Implement `PromptManager` class
- Create state-specific prompt templates
- Add examples and counter-examples for each state
- Include action format examples in prompts

### Step 4A: Add Persistence Layer
[Details: steps/04A_persistence_layer.md]

- Define database interface for data access
- Create data models for state, context, identities, and user data
- Implement in-memory database for development and testing
- Implement SQL database for production
- Create factory for database creation
- Write tests for database operations

### Step 4B: Enhance Context Management
[Details: steps/04B_context_manager.md]

- Implement `ContextManager` class using the persistence layer
- Add context consolidation for long conversations
- Create user profile tracking
- Implement session management
- Add conversion between domain models and persistence models
- Write tests for context operations

### Step 5: Build Action System
[Details: steps/05_action_system.md]

- Implement `ActionExecutor` class
- Define action handlers for each action type
- Create action parsing from LLM responses
- Add validation against allowed actions per state
- Integrate with context manager for context updates
- Write tests for action execution

### Step 6: Update Service Layer
[Details: steps/06_service_layer.md]

- Create new `CoachService` class (replacing the existing one)
- Integrate state machine, prompt manager, context manager, and action executor
- Implement the new service flow
- Add dependency injection for components
- Write tests for service operations

### Step 8: Update API Layer
[Details: steps/08_api_layer.md]

- Replace existing API routes with new implementation
- Add endpoints for state management
- Create response models for state information
- Update documentation
- Write tests for API endpoints

### Step 9: Frontend Integration
[Details: steps/09_frontend_integration.md]

- Update TypeScript types for new API responses
- Add state visualization in UI
- Implement state-aware UI components
- Create transitions between states
- Add session management in the UI

## Component Interactions

The components will interact as follows:

1. **API Layer**:
   - Receives requests from the frontend
   - Calls the Service Layer to process requests
   - Returns responses to the frontend

2. **Service Layer**:
   - Coordinates the interaction between components
   - Initializes and configures components
   - Processes requests and generates responses

3. **State Machine**:
   - Evaluates state transitions based on context
   - Validates state changes
   - Provides allowed actions for each state

4. **Prompt Manager**:
   - Provides state-specific prompts
   - Formats prompts with context
   - Includes examples and counter-examples

5. **Context Manager**:
   - Loads and saves context using the Persistence Layer
   - Manages conversation history
   - Consolidates older messages
   - Provides context for prompt formatting

6. **Action System**:
   - Parses actions from LLM responses
   - Validates actions against allowed actions
   - Executes actions using appropriate handlers
   - Updates context through the Context Manager

7. **Persistence Layer**:
   - Provides a consistent interface for data storage
   - Stores and retrieves state, context, identities, and user data
   - Supports multiple storage backends

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
│   ├── state.py          # State-related models
│   ├── action.py         # Action-related models
│   └── context.py        # Context-related models
├── state/
│   ├── __init__.py
│   ├── machine.py        # State machine implementation
│   ├── transitions.py    # State transition definitions
│   └── validation.py     # State validation
├── prompt/
│   ├── __init__.py
│   ├── manager.py        # Prompt manager implementation
│   ├── templates.py      # Prompt template definitions
│   └── examples.py       # Example conversations
├── persistence/
│   ├── __init__.py
│   ├── interface.py      # Database interface
│   ├── in_memory_db.py   # In-memory database implementation
│   ├── sql_db.py         # SQL database implementation
│   ├── factory.py        # Database factory
│   └── models/           # Persistence models
│       ├── __init__.py
│       ├── state.py      # State record model
│       ├── context.py    # Context record model
│       ├── identity.py   # Identity record model
│       └── user.py       # User record model
├── context/
│   ├── __init__.py
│   ├── manager.py        # Context manager implementation
│   └── models.py         # Context-specific models and conversions
├── action/
│   ├── __init__.py
│   ├── executor.py       # Action executor implementation
│   ├── handlers.py       # Action handler implementations
│   ├── parser.py         # Action parsing from LLM responses
│   └── models.py         # Action-specific models
├── service.py            # New service implementation
└── factory.py            # Factory for creating service and components
```

### Testing Strategy

For each component, we will:

1. Write unit tests for core functionality
2. Create integration tests for component interactions
3. Develop end-to-end tests for complete flows
4. Use mock implementations for dependencies

### Dependency Injection

Components will accept dependencies through their constructors:

```python
class ContextManager:
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface,
        max_recent_messages: int = 10
    ):
        self.llm_client = llm_client
        self.db = db
        self.max_recent_messages = max_recent_messages

class ActionExecutor:
    def __init__(
        self,
        context_manager: ContextManager,
        db: DatabaseInterface,
        state_machine: CoachStateMachine
    ):
        self.context_manager = context_manager
        self.db = db
        self.state_machine = state_machine

class CoachService:
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface
    ):
        self.llm_client = llm_client
        self.db = db
        
        # Create components
        self.state_machine = create_state_machine()
        self.prompt_manager = create_prompt_manager()
        self.context_manager = ContextManager(llm_client, db)
        self.action_executor = create_action_executor(
            self.context_manager, db, self.state_machine
        )
```

### Session Management

The system will support multiple sessions per user:

1. Each session will have a unique session ID
2. The session ID will be used to load and save context
3. The frontend will maintain the session ID across requests
4. The API will accept the session ID as a parameter

## Next Steps

1. Complete the implementation of the core models (Step 1)
2. Implement the state machine (Step 2)
3. Create the prompt manager (Step 3)
4. Implement the persistence layer (Step 4A)
5. Enhance the context manager (Step 4B)
6. Build the action system (Step 5)
7. Update the service layer (Step 6)
8. Update the API layer (Step 8)
9. Update the frontend (Step 9)
