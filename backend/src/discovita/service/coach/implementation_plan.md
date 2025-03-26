# Coach Chatbot Implementation Plan

## Overview
This document outlines the implementation plan for a terminal-based coach chatbot that guides users through four key milestones:
1. Introduction
2. Identity Brainstorming (minimum 5 identities)
3. Identity Refinement (narrow down to 3)
4. Identity Visualization (visualization exercise for each identity)

The implementation will leverage existing code, particularly the `CoachService` class, while creating a simple terminal interface for interaction and storing conversation state in memory during a single session.

## System Architecture

### Core Components
1. **CoachService**: Use the existing service for handling coaching interactions
2. **TerminalCoach**: Wrapper class that manages the terminal interface and session state
3. **State Management**: Track the current milestone and progress using existing state models
4. **Prompt Templates**: Use existing templates for the different milestones
5. **Identity Storage**: In-memory storage of identities during the session

## Implementation Details

### 1. TerminalCoach Class

```python
class TerminalCoach:
    """Terminal interface for the coach service.
    
    This class:
    1. Provides a terminal UI for interacting with the coach
    2. Manages conversation history in memory
    3. Tracks the current coaching state
    4. Stores identities generated during the session
    """
    
    def __init__(self, openai_client: OpenAIClient):
        """Initialize the terminal coach.
        
        Args:
            openai_client: Client for OpenAI API interactions
        """
        # Initialize coach service
        self.coach_service = CoachService(openai_client)
        
        # Initialize state tracking
        self.conversation_history = []
        self.current_state = CoachingState.INTRODUCTION
        self.identities = {
            "draft": [],  # List of all brainstormed identities
            "refined": []  # List of refined identities (max 3)
        }
        self.current_focus_identity = None
        self.metadata = {
            ContextMetadataKey.INTRODUCTION_COMPLETED: False,
            ContextMetadataKey.DRAFT_IDENTITIES: [],
            ContextMetadataKey.CURRENT_IDENTITY_REFINED: False,
            ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED: False
        }
        
        # User profile (empty initially)
        self.user_profile = UserProfile(user_id="terminal_user", identities=[], current_focus=None)
    
    async def process_message(self, user_message: str) -> str:
        """Process a user message and generate a response.
        
        Args:
            user_message: The message from the user
            
        Returns:
            A response message from the coach
        """
        # Add user message to history
        self.conversation_history.append(ChatMessage(role="user", content=user_message))
        
        # Create request object
        request = CoachRequest(
            user_id="terminal_user",
            message=user_message,
            context=self.conversation_history.copy(),
            profile=self.user_profile
        )
        
        # Get response from coach service
        response = await self.coach_service.get_response(request)
        
        # Process any state changes or identity updates
        self._update_state(response)
        
        # Add assistant message to history
        self.conversation_history.append(ChatMessage(role="assistant", content=response.message))
        
        return response.message
    
    def _update_state(self, response: CoachResponse) -> None:
        """Update the session state based on the coach response.
        
        This method:
        1. Tracks proposed and confirmed identities
        2. Updates the current state based on the coaching progress
        3. Updates the user profile with new identities
        
        Args:
            response: The CoachResponse object
        """
        # Handle proposed identity
        if response.proposed_identity:
            proposed = response.proposed_identity
            # Add to draft identities if not already present
            if not any(i.name == proposed.name for i in self.identities["draft"]):
                self.identities["draft"].append(proposed)
                self.metadata[ContextMetadataKey.DRAFT_IDENTITIES] = self.identities["draft"]
        
        # Handle confirmed identity
        if response.confirmed_identity:
            confirmed = response.confirmed_identity
            
            # Add to user profile if not already present
            if not any(i.name == confirmed.name for i in self.user_profile.identities):
                self.user_profile.identities.append(confirmed)
            
            # Add to refined identities if in refinement state
            if self.current_state == CoachingState.IDENTITY_REFINEMENT:
                if not any(i.name == confirmed.name for i in self.identities["refined"]):
                    if len(self.identities["refined"]) < 3:
                        self.identities["refined"].append(confirmed)
                        # If we have 3 refined identities, mark as ready for visualization
                        if len(self.identities["refined"]) == 3:
                            self.metadata[ContextMetadataKey.CURRENT_IDENTITY_REFINED] = True
            
            # Set as current focus for visualization if in visualization state
            if self.current_state == CoachingState.IDENTITY_VISUALIZATION:
                self.current_focus_identity = confirmed
                self.user_profile.current_focus = confirmed.category
                # Mark as visualized
                self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = True
        
        # Update state based on progress
        self._check_state_transition()
    
    def _check_state_transition(self) -> None:
        """Check if we should transition to a new state based on current progress."""
        # Introduction → Identity Brainstorming
        if self.current_state == CoachingState.INTRODUCTION:
            # Simple heuristic: After 3 exchanges, mark introduction as complete
            if len(self.conversation_history) >= 6:  # 3 user messages + 3 assistant messages
                self.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True
                self.current_state = CoachingState.IDENTITY_BRAINSTORMING
        
        # Identity Brainstorming → Identity Refinement
        elif self.current_state == CoachingState.IDENTITY_BRAINSTORMING:
            # Transition when we have at least 5 draft identities
            if len(self.identities["draft"]) >= 5:
                self.current_state = CoachingState.IDENTITY_REFINEMENT
        
        # Identity Refinement → Identity Visualization
        elif self.current_state == CoachingState.IDENTITY_REFINEMENT:
            # Transition when we have 3 refined identities
            if len(self.identities["refined"]) == 3:
                self.current_state = CoachingState.IDENTITY_VISUALIZATION
                # Set first identity as focus
                if self.identities["refined"]:
                    self.current_focus_identity = self.identities["refined"][0]
                    self.user_profile.current_focus = self.identities["refined"][0].category
```

### 2. Terminal Interface

```python
async def run_terminal_interface(self):
    """Run the terminal interface for the coach chatbot."""
    print("Welcome to the Coach Chatbot!")
    print("Type 'exit' to quit the conversation.\n")
    
    # Initial message from the coach
    init_message = "Hello! I'm Leigh Ann, your personal coach. I'm here to help you explore and develop powerful identities that align with your goals and values. How are you today?"
    print(f"Coach: {init_message}")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nCoach: Thank you for the conversation! Goodbye!")
            break
        
        # Process message and get response
        coach_response = await self.process_message(user_input)
        
        # Display response
        print(f"\nCoach: {coach_response}")
        
        # Display current state information (for debugging)
        state_info = f"\n[DEBUG] Current state: {self.current_state.value}"
        if self.current_state == CoachingState.IDENTITY_BRAINSTORMING:
            state_info += f", Draft identities: {len(self.identities['draft'])}"
        elif self.current_state == CoachingState.IDENTITY_REFINEMENT:
            state_info += f", Refined identities: {len(self.identities['refined'])}"
        elif self.current_state == CoachingState.IDENTITY_VISUALIZATION:
            current_identity = self.current_focus_identity.name if self.current_focus_identity else "None"
            state_info += f", Current focus: {current_identity}"
            state_info += f", Visualized: {self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED]}"
        print(state_info)
        
        # Special handling for identity visualization state
        if (self.current_state == CoachingState.IDENTITY_VISUALIZATION and 
            self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] and
            len(self.identities["refined"]) > 0):
            
            # Move to next identity if available
            visualized_identities = [i for i in self.identities["refined"] 
                                    if i.name == self.current_focus_identity.name]
            if len(visualized_identities) < len(self.identities["refined"]):
                # Find next unvisualized identity
                for identity in self.identities["refined"]:
                    if not any(i.name == identity.name for i in visualized_identities):
                        self.current_focus_identity = identity
                        self.user_profile.current_focus = identity.category
                        self.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = False
                        print(f"\n[DEBUG] Moving to next identity: {identity.name}")
                        break
```

### 3. Extended Context Builder

We need to make a small extension to the `ContextBuilder` to provide state-specific prompts:

```python
# Add these methods to the existing ContextBuilder class

def get_introduction_prompt(self):
    """Get the introduction state prompt."""
    return self._load_state_prompt("introduction")

def get_brainstorming_prompt(self):
    """Get the identity brainstorming state prompt."""
    return self._load_state_prompt("identity_brainstorming")

def get_refinement_prompt(self):
    """Get the identity refinement state prompt."""
    return self._load_state_prompt("identity_refinement")

def get_visualization_prompt(self):
    """Get the identity visualization state prompt."""
    return self._load_state_prompt("identity_visualization")

def _load_state_prompt(self, state_name):
    """Load a state-specific prompt."""
    file_path = os.path.join(os.path.dirname(__file__), f"prompts/states/{state_name}.md")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    # Fall back to general system prompt if state-specific prompt is not found
    return self.get_system_prompt()
```

## Main Script

```python
#!/usr/bin/env python
"""Terminal-based coach chatbot."""

import asyncio
import os
from dotenv import load_dotenv

from discovita.service.openai.client.client import OpenAIClient
from discovita.service.coach.terminal_coach import TerminalCoach

async def main():
    """Run the coach chatbot."""
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    openai_client = OpenAIClient()
    
    # Initialize terminal coach
    coach = TerminalCoach(openai_client)
    
    # Run terminal interface
    await coach.run_terminal_interface()

if __name__ == "__main__":
    asyncio.run(main())
```

## Implementation Steps

1. **Create Terminal Interface Wrapper**
   - Implement `TerminalCoach` class that uses the existing `CoachService`
   - Create terminal interface loop for user interaction

2. **Extend ContextBuilder**
   - Add methods to access state-specific prompts
   - Ensure compatibility with existing code

3. **Implement State Logic**
   - Logic to track and transition between the four states
   - Track identities through the process

4. **Testing and Refinement**
   - Test each milestone individually
   - Ensure smooth transitions between states
   - Verify identity tracking and visualization

## Advantages of This Approach

1. **Leverages Existing Code**: Uses the existing `CoachService` implementation instead of reimplementing it
2. **Separation of Concerns**: Keeps the service logic separate from the terminal interface
3. **Maintainability**: Changes to the core service can be made without affecting the terminal interface
4. **Extensibility**: The same service can be used with different interfaces (terminal, web, etc.)

## Next Steps After Initial Implementation

1. Add persistent storage for conversation history
2. Implement user authentication
3. Create a web interface
4. Add additional coaching milestones (Action Planning, Accountability)
5. Enhance visualization features with image generation 