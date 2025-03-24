# Revised Alignment of Context Manager with Other Components

This document outlines how the Context Manager (Step 04B) should be aligned with both the Persistence Layer (Step 04A) and the Action System (Step 05) to avoid duplication and ensure consistent implementation.

## Alignment with Persistence Layer (Step 04A)

### Current Overlap

The current implementation plans show several areas of overlap between the Context Manager and Persistence Layer:

1. **Persistence Implementation**:
   - Context Manager has its own persistence classes (`ContextPersistence`, `FileContextPersistence`, `DatabaseContextPersistence`)
   - Persistence Layer has a more comprehensive implementation with `DatabaseInterface` and specific implementations

2. **Data Models**:
   - Context Manager uses a `CoachContext` model
   - Persistence Layer has specific models (`StateRecord`, `ContextRecord`, `IdentityRecord`, `UserRecord`)

3. **Context Operations**:
   - Context Manager has placeholder methods for loading and saving context
   - Persistence Layer provides comprehensive methods for all data types

### Recommended Changes

1. **Remove Duplicate Persistence Implementation**:
   - Remove `persistence.py` from the Context Manager
   - Update the Context Manager to use the Persistence Layer's `DatabaseInterface`

2. **Align Data Models**:
   - Map `CoachContext` to the Persistence Layer's `ContextRecord`
   - Define clear conversion methods between the two if needed
   - Ensure all fields in `CoachContext` can be stored in `ContextRecord`

3. **Implement Context Operations Using Persistence Layer**:
   - Update the Context Manager to use the database interface for loading and saving context
   - Implement conversion methods between domain models and persistence models

## Alignment with Action System (Step 05)

### Current Overlap

The current implementation plans show several areas of overlap between the Context Manager and Action System:

1. **Action Execution**:
   - Context Manager has methods for executing actions directly
   - Action System provides a comprehensive action execution framework

2. **Action Handlers**:
   - Context Manager implements action handling directly
   - Action System provides dedicated handlers for different action types

### Recommended Changes

1. **Remove Action Execution from Context Manager**:
   - The Context Manager should not execute actions directly
   - It should provide methods for updating context that can be called by action handlers

2. **Focus on Context Management**:
   - The Context Manager should focus on managing conversation context
   - It should provide methods for loading, saving, and updating context
   - It should not be responsible for parsing or executing actions

3. **Provide Context Update Methods**:
   - The Context Manager should provide methods for updating context that can be called by action handlers
   - These methods should be focused on specific context updates, not action execution

## Revised Context Manager Implementation

### Core Responsibilities

The Context Manager should focus on:

1. Loading and saving context using the Persistence Layer
2. Adding messages to conversation history
3. Consolidating older messages into summaries
4. Providing methods for updating context that can be called by action handlers
5. Converting between domain models and persistence models

### Context Manager Interface

```python
class ContextManager:
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface,
        max_recent_messages: int = 10
    ):
        """Initialize the context manager."""
        self.llm_client = llm_client
        self.db = db
        self.max_recent_messages = max_recent_messages
    
    async def load_context(self, user_id: str, session_id: str) -> CoachContext:
        """Load or create context for a user session."""
        # Implementation using the persistence layer
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context to the persistence layer."""
        # Implementation using the persistence layer
    
    async def add_message(self, context: CoachContext, role: str, content: str) -> CoachContext:
        """Add a message to the conversation history."""
        # Implementation
    
    async def update_user_profile(self, context: CoachContext, profile: UserProfile) -> CoachContext:
        """Update the user profile in the context."""
        # Implementation
    
    async def update_metadata(self, context: CoachContext, key: str, value: Any) -> CoachContext:
        """Update a metadata value in the context."""
        # Implementation
    
    async def _consolidate_context(self, context: CoachContext) -> CoachContext:
        """Consolidate older messages into a summary."""
        # Implementation
```

### Action Handler Integration

Action handlers from the Action System will use the Context Manager to update context:

```python
class SaveIdentityHandler(ActionHandler):
    def __init__(self, context_manager: ContextManager, db: DatabaseInterface):
        self.context_manager = context_manager
        self.db = db
    
    async def execute(self, action: Action, context: CoachContext) -> ActionResult:
        # Extract identity data from action
        identity_data = action.params.get("identity", {})
        status = action.params.get("status", "")
        
        # Update context metadata
        if status == "proposed":
            await self.context_manager.update_metadata(
                context, 
                "proposed_identity", 
                identity_data
            )
        elif status == "confirmed":
            await self.context_manager.update_metadata(
                context, 
                "confirmed_identity", 
                identity_data
            )
            
            # Also add to draft identities for state transitions
            draft_identities = context.metadata.get("draft_identities", [])
            draft_identities.append(identity_data)
            await self.context_manager.update_metadata(
                context, 
                "draft_identities", 
                draft_identities
            )
            
            # Save the identity to the database
            await self.db.save_identity(
                context.user_id,
                identity_data.get("name", ""),
                identity_data.get("category", ""),
                identity_data.get("description", "")
            )
        
        return ActionResult(success=True, message="Identity saved")
```

## Service Layer Integration

The Service Layer will integrate the Context Manager, Persistence Layer, and Action System:

```python
class CoachService:
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface
    ):
        """Initialize the coach service."""
        self.llm_client = llm_client
        self.db = db
        
        # Create the state machine
        self.state_machine = create_state_machine()
        
        # Create the prompt manager
        self.prompt_manager = create_prompt_manager()
        
        # Create the context manager
        self.context_manager = ContextManager(
            llm_client=llm_client,
            db=db
        )
        
        # Create the action executor
        self.action_executor = create_action_executor(
            context_manager=self.context_manager,
            db=self.db,
            state_machine=self.state_machine
        )
    
    async def get_response(self, request: CoachRequest) -> CoachResponse:
        """Get a response from the coach."""
        # Generate a session ID if not provided
        session_id = request.session_id or str(uuid4())
        
        # Load or create context for this user session
        context = await self.context_manager.load_context(request.user_id, session_id)
        
        # Update context with user profile if provided
        if request.profile:
            context = await self.context_manager.update_user_profile(
                context, 
                request.profile
            )
        
        # Add the user's message to the context
        context = await self.context_manager.add_message(
            context, 
            "user", 
            request.message
        )
        
        # Get the current state
        current_state = context.current_state
        
        # Get the prompt for the current state
        prompt = self.prompt_manager.get_prompt(current_state, context)
        
        # Get structured completion from OpenAI
        structured_response = await self.llm_client.get_structured_completion(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": request.message}
            ],
            response_model=CoachStructuredResponse
        )
        
        # Execute actions from the response
        action_results = await self.action_executor.execute_actions(
            structured_response.message,
            context
        )
        
        # Check for state transitions
        self.state_machine.transition(context)
        
        # Add the assistant's response to the context
        context = await self.context_manager.add_message(
            context, 
            "assistant", 
            structured_response.message
        )
        
        # Extract visualization prompt if an identity was proposed or confirmed
        visualization_prompt = None
        
        # Check proposed identity first
        if structured_response.proposed_identity and structured_response.proposed_identity.visualization:
            visualization_prompt = structured_response.proposed_identity.visualization
        # If no proposed identity with visualization, check confirmed identity
        elif structured_response.confirmed_identity and structured_response.confirmed_identity.visualization:
            visualization_prompt = structured_response.confirmed_identity.visualization
        
        return CoachResponse(
            message=structured_response.message,
            proposed_identity=structured_response.proposed_identity,
            confirmed_identity=structured_response.confirmed_identity,
            visualization_prompt=visualization_prompt,
            current_state=context.current_state.value,
            session_id=session_id
        )
```

## Benefits of This Approach

1. **Clear Separation of Concerns**:
   - Context Manager focuses on context management
   - Persistence Layer focuses on data storage
   - Action System focuses on action execution

2. **Reduced Duplication**:
   - No duplicate persistence implementation
   - No duplicate action handling

3. **Improved Maintainability**:
   - Each component has a clear responsibility
   - Changes to one component have minimal impact on others

4. **Better Testability**:
   - Each component can be tested independently
   - Mock implementations can be used for testing

## Implementation Steps

1. Update the Context Manager to use the Persistence Layer
2. Remove action execution from the Context Manager
3. Implement the Action System as a separate component
4. Update the Service Layer to integrate all components
