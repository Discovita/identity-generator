# Step 5: Build Action System

This document outlines the implementation plan for building the action system that will execute actions determined by the coach.

## Current Implementation

The current implementation does not have a formal action system. Instead, it:

- Extracts structured data (identities) from LLM responses
- Updates the response model with this data
- Relies on the frontend to handle any actions based on the response

## Target Implementation

The new action system will:

1. Parse actions from LLM responses
2. Validate actions against allowed actions for the current state
3. Execute actions using appropriate handlers
4. Update the context and database with the results
5. Support a variety of action types for different coaching functions

## Implementation Details

### 1. Action Models

Define the core models for the action system:

[05_action_system_code/models/action.py](./05_action_system_code/models/action.py)

Key models:
- `Action`: Represents an action to be executed
- `ActionResult`: Represents the result of an action execution
- `ActionDefinition`: Defines an available action and its parameters

### 2. Action Executor

The core component that executes actions:

[05_action_system_code/executor.py](./05_action_system_code/executor.py)

Key functionality:
- Parses actions from LLM responses
- Validates actions against allowed actions for the current state
- Executes actions using registered handlers
- Returns results of action execution

### 3. Action Handlers

Handlers for specific action types:

[05_action_system_code/handlers.py](./05_action_system_code/handlers.py)

Implemented handlers:
- `SaveUserInfoHandler`: Saves user information
- `SaveIdentityHandler`: Saves a new identity
- `MarkIntroductionCompleteHandler`: Marks the introduction as complete
- `TransitionStateHandler`: Requests a state transition

### 4. Action Parser

Parses actions from LLM responses:

[05_action_system_code/parser.py](./05_action_system_code/parser.py)

Features:
- Supports multiple action formats (default and XML)
- Handles error recovery for malformed actions
- Provides a factory function for creating parsers

## Integration with Other Components

The action system integrates with other components as follows:

1. **Service Layer**: The service layer calls the action executor to parse and execute actions from LLM responses
2. **Context Manager**: Action handlers update the context with the results of actions
3. **State Machine**: Action handlers request state transitions and validate actions against allowed actions
4. **Database**: Action handlers persist data to the database

## Action Flow

The flow of an action through the system:

1. LLM generates a response with embedded actions
2. Action executor parses actions from the response
3. Action executor validates actions against allowed actions for the current state
4. Action executor executes actions using appropriate handlers
5. Action handlers update the context and database
6. Action results are returned to the service layer

## Example Actions

### Save User Information

```
[ACTION:SAVE_USER_INFO]{"key": "goals", "value": "User wants to improve work-life balance"}[/ACTION]
```

### Save Identity

```
[ACTION:SAVE_IDENTITY]{"identity": "Creative Visionary", "category": "PASSIONS", "description": "Someone who sees possibilities and creates new things"}[/ACTION]
```

### Mark Introduction Complete

```
[ACTION:MARK_INTRODUCTION_COMPLETE]{}[/ACTION]
```

### Request State Transition

```
[ACTION:TRANSITION_STATE]{"target_state": "IDENTITY_DISCOVERY"}[/ACTION]
```

## Testing Strategy

1. **Unit Tests**:
   - Test action parsing with various formats and edge cases
   - Test action validation against allowed actions
   - Test each action handler with valid and invalid parameters

2. **Integration Tests**:
   - Test the complete flow from LLM response to action execution
   - Test integration with context manager and state machine
   - Test error handling and recovery

## Implementation Steps

1. Create the action models
2. Implement the action parser
3. Implement the action handlers
4. Implement the action executor
5. Write tests for each component
6. Integrate with the service layer

## Considerations

### Extensibility

The action system is designed to be extensible:

- New action types can be added by creating new handlers
- New action formats can be supported by creating new parsers
- The action executor can be extended to support new validation rules

### Error Handling

The action system includes robust error handling:

- Malformed actions are logged and skipped
- Invalid parameters are validated before execution
- Exceptions during execution are caught and reported

### Security

The action system includes security measures:

- Actions are validated against allowed actions for the current state
- Parameters are validated before execution
- The system is designed to fail safely if an action cannot be executed

## Next Steps

After implementing the action system, we need to:

1. Update the service layer to use the action system
2. Update the prompt templates to include action examples
3. Update the state machine to define allowed actions for each state
