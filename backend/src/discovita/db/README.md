# Discovita Database Interfaces

This directory contains database interfaces and persistence implementations for the Discovita identity generator application.

## Overview

The database package provides abstract interfaces and concrete implementations for persistent storage of state and context information in the coaching system. This persistence layer is designed to support the state machine architecture of the coaching service.

## Components

### StateStore Interface

The `StateStore` abstract class defines the interface for persistence operations:

```python
class StateStore:
    """Interface for state persistence."""
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user."""
        
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user."""
```

This interface provides the contract that all state persistence implementations must follow, with two main operations:

- **load_context**: Retrieves a user's coaching context by their user ID
- **save_context**: Persists a coaching context for later retrieval

### InMemoryStateStore Implementation

The `InMemoryStateStore` class provides an in-memory implementation of the `StateStore` interface:

```python
class InMemoryStateStore(StateStore):
    """In-memory implementation of state persistence."""
```

This implementation is marked as planned for "Step 7: Persistence Layer" and is not yet fully implemented. When completed, it will:

1. Store coaching contexts in memory using a dictionary with user IDs as keys
2. Provide fast, temporary storage for coaching contexts
3. Be suitable for development and testing, but not for production use as data is lost when the application restarts

## Integration with Coach Context

The `StateStore` works directly with `CoachContext` objects from the coaching service, which contain:

- User ID
- Current coaching state
- Conversation history
- Consolidated conversation summary
- User profile information
- Additional metadata

## Usage

### Loading a Context

```python
# Initialize a state store implementation
state_store = InMemoryStateStore()

# Load a user's context
user_id = "user-123"
context = await state_store.load_context(user_id)

if context:
    # Context exists, use it
    current_state = context.current_state
else:
    # No context found, create a new one
    context = CoachContext(user_id=user_id)
```

### Saving a Context

```python
# Update the context
context.current_state = CoachingState.IDENTITY_BRAINSTORMING
context.conversation_history.append(chat_message)

# Save the updated context
await state_store.save_context(context)
```

## Planned Implementations

The current module has a placeholder for the `InMemoryStateStore` implementation. Future implementations may include:

- **FileStateStore**: Persists contexts to disk as JSON or other serialized format
- **SQLStateStore**: Stores contexts in a SQL database
- **DynamoDBStateStore**: Uses AWS DynamoDB for persistence
- **RedisStateStore**: Leverages Redis for high-performance caching and persistence

## Design Considerations

1. **Async Interface**: The interface uses async/await for all operations to support non-blocking I/O
2. **Separation of Concerns**: The abstract interface separates the persistence contract from implementation details
3. **Statefulness**: The implementation may maintain internal state (like the in-memory dictionary) 
4. **Exception Handling**: Implementations should handle and properly propagate storage-related exceptions

## Development Status

The persistence layer is currently marked as "Step 7" in the implementation plan, indicating it's a planned component but not yet fully implemented. 