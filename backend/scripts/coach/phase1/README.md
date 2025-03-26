# Coach Chatbot - Phase 1

A terminal-based implementation of the coach chatbot that guides users through four key milestones:

1. **Introduction**: Brief back-and-forth to establish rapport
2. **Identity Brainstorming**: Generate at least 5 identity ideas
3. **Identity Refinement**: Narrow down to 3 core identities
4. **Identity Visualization**: Visualization exercise for each of the 3 identities

## Architecture

This implementation uses a layered architecture:

- **Extended Coach Service**: Wraps the existing `CoachService` with state-specific prompts
- **Terminal Coach**: Provides a terminal interface and manages conversation state
- **Extended Context Builder**: Adds support for state-specific prompts
- **Function Calling System**: Allows the LLM to update coaching state directly

## Components

- `main.py`: Entry point that initializes the services and runs the terminal interface
- `terminal_coach.py`: Manages the conversation state and terminal UI
- `extended_context_builder.py`: Extends the base ContextBuilder to use state-specific prompts
- `coach_functions.py`: Defines functions that the LLM can call to update state

## Function Calling Capability

The coach now uses OpenAI's function calling to allow the LLM to update the conversation state. This enables:

1. **Smarter State Transitions**: The LLM can proactively update state based on conversation
2. **Identity Management**: The LLM can add identities during brainstorming and refinement
3. **Visualization Control**: The LLM can control which identity is being visualized
4. **State Awareness**: The LLM can check current progress and state at any time

Available functions:

- `add_draft_identity`: Add new identity during brainstorming
- `add_refined_identity`: Add confirmed identity during refinement
- `set_focus_identity`: Set focus identity for visualization
- `mark_identity_visualized`: Mark identity as visualized
- `mark_introduction_completed`: Complete introduction phase
- `transition_to_next_state`: Force transition to next state
- `get_coaching_state`: Get current state information

## Prerequisites

- Python 3.7+
- OpenAI API key

## Setup

1. Create a `.env` file in the project root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Ensure the required dependencies are installed:
   - `python-dotenv`
   - OpenAI Python client

## Running the Chatbot

From the backend directory, run:

```bash
python -m scripts.coach.phase1.main
```

Or from the project root directory:

```bash
cd backend
python -m scripts.coach.phase1.main
```

## Implementation Details

### State Management

The chatbot automatically transitions between states based on progress:

- **Introduction → Identity Brainstorming**: After 3 exchanges (6 messages total) or when marked as completed via function call
- **Identity Brainstorming → Identity Refinement**: When at least 5 identities are collected in the draft list
- **Identity Refinement → Identity Visualization**: When exactly 3 identities are in the refined list

### Identity Tracking

The chatbot tracks identities in memory:
- `identities["draft"]`: All brainstormed identities (minimum 5 needed)
- `identities["refined"]`: Selected identities for refinement (maximum 3)
- `current_focus_identity`: The current identity being visualized
- `user_profile.identities`: All confirmed identities from the coach

### LLM Function Calling

The system now allows the LLM to update the state by calling functions. The process works as follows:

1. The LLM generates a response to the user's message
2. The system checks if the LLM wants to call a function to update state
3. If needed, the function is executed and state is updated
4. State transitions might be triggered based on function-driven updates

This approach allows for more dynamic and responsive coaching that better adapts to the conversation flow.

### Debugging Information

The terminal interface displays debugging information after each exchange:
- Current state (Introduction, Identity Brainstorming, Identity Refinement, or Identity Visualization)
- Number of draft identities in Brainstorming state
- Number of refined identities in Refinement state
- Current focus identity and visualization status in Visualization state

### Special Handling for Visualization

In the Visualization state, the chatbot:
1. Sets the first refined identity as the initial focus
2. Marks an identity as visualized after a successful response
3. Automatically moves to the next unvisualized identity

## Next Steps

1. Add persistent storage for conversation history
2. Implement user authentication
3. Create a web interface
4. Add additional coaching milestones (Action Planning, Accountability)
5. Enhance visualization features with image generation 