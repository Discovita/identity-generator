# Step 4B: Context Manager Implementation

## Overview

The context manager is responsible for maintaining conversation state and user data across interactions. It builds upon the persistence layer (Step 4A) to provide reliable state management.

## Key Requirements

1. **Session Management**
   - Track user sessions using the persistence layer's session operations
   - Support multiple active sessions per user
   - Handle session creation and retrieval

2. **Conversation History**
   - Store and retrieve message history
   - Implement message consolidation for long conversations
   - Maintain conversation continuity across sessions

3. **State Management**
   - Track current coaching state
   - Store state-specific metadata
   - Support state transitions

4. **User Data**
   - Maintain user profiles and preferences
   - Track progress and achievements
   - Store identity-related information

## Architecture

### Models

1. **Domain Models**
   ```python
   class CoachContext(BaseModel):
       user_id: str
       session_id: str
       current_state: CoachingState
       conversation_history: List[ChatMessage]
       consolidated_summary: Optional[str] = None
       metadata: Dict[str, Any]
   ```

2. **Persistence Models**
   - Leverage existing `ContextRecord` from persistence layer
   - Add any additional fields needed for context management
   - Ensure proper enum handling for state fields

### Components

1. **Context Manager**
   - Core class managing context operations
   - Interfaces with persistence layer
   - Handles context loading and saving
   - Implements conversation consolidation logic

2. **Context Builder**
   - Constructs prompt context from current state
   - Formats conversation history for LLM
   - Applies consolidation rules

3. **Context Converter**
   - Converts between domain and persistence models
   - Handles serialization of complex types
   - Maintains type safety

## Integration Points

1. **Persistence Layer**
   - Uses in-memory database by default (configured via factory)
   - Falls back to SQL database when persistence is required
   - Leverages session management capabilities

2. **State Machine**
   - Provides state information to context
   - Receives context updates for transition evaluation
   - Maintains state consistency

3. **LLM Service**
   - Receives formatted context for prompts
   - Returns structured responses
   - Updates context based on responses

## Implementation Steps

1. Create context manager module structure
2. Implement core context manager class
3. Add context building utilities
4. Integrate with persistence layer
5. Add conversation consolidation
6. Implement context conversion
7. Add tests

## Testing Strategy

1. **Unit Tests**
   - Context manager operations
   - Conversation consolidation
   - Model conversions
   - State handling

2. **Integration Tests**
   - Persistence layer integration
   - State machine interaction
   - LLM service integration

3. **End-to-End Tests**
   - Complete conversation flows
   - Session management
   - State transitions

## Success Criteria

1. Context persists across sessions
2. Conversation history is properly maintained
3. State transitions are reliable
4. Type safety is maintained
5. All tests pass

## Dependencies

1. Persistence Layer (Step 4A)
   - Must be completed and tested
   - Both in-memory and SQL implementations working
   - Enum handling implemented

2. State Machine Models
   - CoachingState enum
   - State transition definitions
   - State-specific metadata

## Future Considerations

1. Performance optimization for large contexts
2. Additional consolidation strategies
3. Context versioning
4. Migration handling
5. Backup and recovery
