# Alignment of Context Manager with Persistence Layer

This document outlines how the Context Manager (Step 04B) should be aligned with the Persistence Layer (Step 04A) to avoid duplication and ensure consistent implementation.

## Current Overlap

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

4. **Service Integration**:
   - Context Manager integration creates its own persistence instance
   - This should leverage the Persistence Layer instead

## Recommended Changes

### 1. Remove Duplicate Persistence Implementation

The Context Manager should not implement its own persistence mechanism. Instead:

- Remove `persistence.py` from the Context Manager
- Update the Context Manager to use the Persistence Layer's `DatabaseInterface`

### 2. Align Data Models

Ensure the data models are consistent between the two components:

- Map `CoachContext` to the Persistence Layer's `ContextRecord`
- Define clear conversion methods between the two if needed
- Ensure all fields in `CoachContext` can be stored in `ContextRecord`

### 3. Implement Context Operations Using Persistence Layer

Update the Context Manager's persistence methods:

```python
async def _load_from_persistence(self, user_id: str, session_id: str) -> Optional[CoachContext]:
    """Load context from persistence layer."""
    # Use the database interface from the persistence layer
    context_record = await self.db.get_context(user_id, session_id)
    
    if not context_record:
        return None
    
    # Convert from ContextRecord to CoachContext
    return self._convert_to_coach_context(context_record)

async def _save_to_persistence(self, context: CoachContext) -> None:
    """Save context to persistence layer."""
    # Convert from CoachContext to ContextRecord
    context_record = self._convert_to_context_record(context)
    
    # Use the database interface from the persistence layer
    await self.db.save_context(context_record)
```

### 4. Update Service Integration

Modify the `CoachService` to use the Persistence Layer:

```python
def __init__(
    self, 
    llm_client: OpenAIClient,
    db: DatabaseInterface  # Use the database interface from the persistence layer
):
    """Initialize the coach service."""
    self.llm_client = llm_client
    self.db = db
    
    # Create the state machine
    self.state_machine = create_state_machine()
    
    # Create the prompt manager
    self.prompt_manager = create_prompt_manager()
    
    # Create the context manager with the database
    self.context_manager = ContextManager(
        llm_client=llm_client,
        db=db  # Pass the database to the context manager
    )
```

### 5. Factory Integration

Use the Persistence Layer's factory to create the database instance:

```python
from discovita.service.coach.persistence import DatabaseType, create_database

# Create a database instance
db = create_database(DatabaseType.MEMORY)  # For development
# or
db = create_database(
    DatabaseType.SQL,
    connection_string="postgresql://user:password@localhost/coach"
)  # For production

# Create the coach service with the database
coach_service = CoachService(llm_client, db)
```

## Implementation Steps

1. Update the Context Manager to accept a `DatabaseInterface` in its constructor
2. Remove the duplicate persistence implementation from the Context Manager
3. Implement conversion methods between `CoachContext` and `ContextRecord`
4. Update the Context Manager's persistence methods to use the database interface
5. Update the service integration to use the Persistence Layer's factory

## Benefits

This approach provides several benefits:

1. **Eliminates Duplication**: Removes duplicate persistence code
2. **Consistent Implementation**: Ensures consistent data storage across components
3. **Separation of Concerns**: Context Manager focuses on context management, not persistence
4. **Flexibility**: Allows switching between different database implementations
5. **Maintainability**: Easier to maintain with a single persistence implementation

## Testing Strategy

1. **Unit Tests**:
   - Test the Context Manager with a mock database
   - Verify correct conversion between data models
   - Test context operations with the database interface

2. **Integration Tests**:
   - Test the Context Manager with the actual database implementations
   - Verify data flow through the system
   - Test session continuity across multiple interactions
