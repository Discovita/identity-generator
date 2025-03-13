This document references other documents in the `./code` 
subdirectory with square brackets such as [foo.py].  
You are invited to read those files as needed.

# Architecture Plan

## Core Components

1. **State Machine** - Central to managing the coaching process flow
2. **Prompt Manager** - Handles specialized prompts for each state
3. **Context Manager** - Manages conversation history and knowledge about the user
4. **Action Executor** - Executes actions determined by the coach
5. **Database Layer** - Persists user data, identities, actions, and state
6. **API Layer** - Provides interface for frontend communication

## System Flow

```
User Input → API → Context Manager → State Machine → Prompt Manager → LLM → 
Action Executor → Context Manager → Database → Response Formation → API → User
```

Let me provide high-level code for each of these components:

## State Machine

[state_machine.py]

## Prompt Manager

[prompt_manager.py]

## Context Manager

[context_manager.py]

## Action Executor

[action_executor.py]

## Coach API

[coach_api.py]

## LLM Service

[llm_service.py]

## DB Service

[db_service.py]

## Main Application

[main_application.py]

# Key Design Considerations

1. **State Machine Design**
   - Each coaching state has specific goals, prompts, and allowed actions
   - Transitions between states are conditional and controlled
   - Allows for a structured coaching process that follows Leigh Ann's methodology

2. **Context Management**
   - Handles long-term memory through context consolidation
   - Maintains recent conversation history for immediate context
   - Stores user data including identities, actions, and progress

3. **Action System**
   - LLM can trigger predefined actions like saving identities or updating user data
   - Actions are parsed from structured text in LLM responses
   - Each action has a specific handler and is validated against allowed actions for the current state

4. **Prompt Engineering**
   - State-specific prompts with examples and counter-examples
   - Clear instructions on goals and available actions for each state
   - Prompt templates utilize the context provided by the context manager

5. **Database Integration**
   - Persists user state, identities, actions, and conversation summaries
   - Allows the coaching process to continue across multiple sessions
   - Supports relationship between identities and actions

This architecture provides a clean separation of concerns while maintaining the stateful, context-sensitive coaching process you described. The system can guide users through Leigh Ann's structured methodology while adapting to their individual needs and progress.