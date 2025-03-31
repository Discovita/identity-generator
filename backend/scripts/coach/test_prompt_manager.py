"""Test script to verify that the system_context.md file is included in the prompt."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from discovita.service.coach.models import CoachState, CoachingState, UserProfile, Message
from discovita.service.coach.prompt.manager import PromptManager

def main():
    """Test the prompt manager."""
    # Create a prompt manager
    prompt_manager = PromptManager()
    
    # Create a simple coach state for testing
    coach_state = CoachState(
        current_state=CoachingState.IDENTITY_BRAINSTORMING,
        user_profile=UserProfile(name="Test User", goals=[]),
        identities=[],
        conversation_history=[
            Message(role="user", content="I'm ready to brainstorm!"),
            Message(role="coach", content="Great! Let's get started.")
        ]
    )
    
    # Get the prompt
    prompt = prompt_manager.get_prompt(coach_state)
    
    # Check if system_context.md content is included
    if "Coaching System Context" in prompt:
        print("SUCCESS: system_context.md is included in the prompt!")
    else:
        print("ERROR: system_context.md is NOT included in the prompt!")
    
    # Print the first 500 characters of the prompt to verify
    print("\nFirst 500 characters of the prompt:")
    print(prompt[:500])
    
    # Print the section around where "Coaching System Context" should appear
    system_context_index = prompt.find("Coaching System Context")
    if system_context_index != -1:
        start_index = max(0, system_context_index - 100)
        end_index = min(len(prompt), system_context_index + 500)
        print("\nSection around 'Coaching System Context':")
        print(prompt[start_index:end_index])
    
if __name__ == "__main__":
    main()
