# Step 7: Add Persistence Layer

This document outlines the implementation plan for adding a persistence layer to the coach state machine architecture.

## Current Implementation

The current implementation does not have a formal persistence layer. Instead, it:

- Relies on in-memory storage during a session
- Does not persist state across sessions
- Requires re-establishing context with each new session

## Target Implementation

The new persistence layer will:

1. Provide a consistent interface for data storage operations
2. Support multiple storage backends (in-memory, SQL)
3. Persist state, context, identities, and user data
4. Enable session continuity across multiple interactions
5. Support data recovery and migration

## Implementation Details

### 1. Database Interface

Define a common interface for all database implementations:

[07_persistence_layer_code/interface.py](./07_persistence_layer_code/interface.py)

Key features:
- Abstract base class with required methods
- Comprehensive operations for all data types
- Asynchronous methods for non-blocking I/O

### 2. Data Models

Define the core data models for the persistence layer:

- [07_persistence_layer_code/models/state.py](./07_persistence_layer_code/models/state.py) - State records
- [07_persistence_layer_code/models/context.py](./07_persistence_layer_code/models/context.py) - Context records
- [07_persistence_layer_code/models/identity.py](./07_persistence_layer_code/models/identity.py) - Identity records
- [07_persistence_layer_code/models/user.py](./07_persistence_layer_code/models/user.py) - User records

### 3. In-Memory Implementation

Implement an in-memory database for development and testing:

[07_persistence_layer_code/in_memory_db.py](./07_persistence_layer_code/in_memory_db.py)

Features:
- Simple dictionary-based storage
- No persistence across application restarts
- Useful for testing and development

### 4. SQL Implementation

Implement a SQL database for production use:

[07_persistence_layer_code/sql_db.py](./07_persistence_layer_code/sql_db.py)

Features:
- SQLAlchemy ORM for database operations
- Support for multiple SQL databases (PostgreSQL, SQLite)
- Proper transaction handling and error recovery

### 5. Factory

Create a factory for creating database instances:

[07_persistence_layer_code/factory.py](./07_persistence_layer_code/factory.py)

Features:
- Enum-based database type selection
- Configuration-based instantiation
- Database initialization support

## Integration with Other Components

The persistence layer integrates with other components as follows:

1. **State Machine**: The state machine uses the persistence layer to store and retrieve state
2. **Context Manager**: The context manager uses the persistence layer to store and retrieve context
3. **Action Executor**: Action handlers use the persistence layer to persist changes
4. **Service Layer**: The service layer initializes and configures the persistence layer

## Data Flow

The flow of data through the persistence layer:

1. Service layer initializes the database with the appropriate implementation
2. Components retrieve data from the database as needed
3. Components update data in the database when changes occur
4. Database persists data according to its implementation

## Example Usage

### Creating a Database

```python
from discovita.service.coach.persistence import DatabaseType, create_database

# Create an in-memory database
db = create_database(DatabaseType.MEMORY)

# Create a SQL database
db = create_database(
    DatabaseType.SQL,
    connection_string="postgresql://user:password@localhost/coach"
)
```

### Using the Database

```python
# Get state
state = await db.get_state(user_id, session_id)

# Save state
await db.save_state(StateRecord(
    user_id=user_id,
    session_id=session_id,
    state="INTRODUCTION"
))

# Get identities
identities = await db.get_identities(user_id)
```

## Testing Strategy

1. **Unit Tests**:
   - Test each database implementation with mock data
   - Verify correct data storage and retrieval
   - Test error handling and edge cases

2. **Integration Tests**:
   - Test the persistence layer with other components
   - Verify data flow through the system
   - Test session continuity across multiple interactions

## Implementation Steps

1. Define the database interface
2. Create the data models
3. Implement the in-memory database
4. Implement the SQL database
5. Create the factory
6. Write tests for each component
7. Integrate with other components

## Considerations

### Performance

The persistence layer is designed for performance:

- Asynchronous methods for non-blocking I/O
- Efficient data structures for in-memory storage
- Connection pooling for SQL databases
- Minimal database queries through caching

### Security

The persistence layer includes security measures:

- No direct SQL queries (using ORM)
- Parameterized queries to prevent SQL injection
- No sensitive data in logs
- Proper error handling to prevent information leakage

### Scalability

The persistence layer is designed for scalability:

- Support for multiple database backends
- Separation of interface and implementation
- Asynchronous operations for high concurrency
- Minimal locking for better throughput

## Next Steps

After implementing the persistence layer, we need to:

1. Update the state machine to use the persistence layer
2. Update the context manager to use the persistence layer
3. Update the action executor to use the persistence layer
4. Update the service layer to initialize and configure the persistence layer
