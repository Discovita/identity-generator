"""Test script for coach introduction state."""

import asyncio
from typing import List

from discovita.config import Settings
from discovita.service.coach.models.state import (
    CoachState,
    CoachingState,
    UserProfile,
    Message
)
from discovita.service.coach.service import CoachService
from discovita.service.coach.prompt.manager import PromptManager
from discovita.service.coach.state.machine import StateMachine
from discovita.service.openai.client.client import OpenAIClient

async def test_introduction():
    """Test the coach's introduction state response."""
    # Initialize components
    settings = Settings.from_env()
    client = OpenAIClient(api_key=settings.openai_api_key)
    prompt_manager = PromptManager()
    state_machine = StateMachine()
    
    service = CoachService(
        client=client,
        prompt_manager=prompt_manager,
        state_machine=state_machine
    )
    
    # Create initial state
    state = CoachState(
        current_state=CoachingState.INTRODUCTION,
        user_profile=UserProfile(
            name="Test User",
            goals=[]
        ),
        identities=[],
        conversation_history=[],
        proposed_identity=None,
        current_identity_index=None
    )
    
    # Process a simple hello message
    result = await service.process_message("Hello", state)
    
    # Print results for inspection
    print("\nTest Results:")
    print("-------------")
    print(f"Coach Response: {result.message}")
    print(f"New State: {result.state.current_state}")
    print(f"Actions Taken: {result.actions}")
    
    # Basic validation
    assert result.state.current_state == CoachingState.INTRODUCTION, \
        "Should remain in introduction state"
    assert len(result.state.conversation_history) == 2, \
        "Should have user message and coach response"
    assert result.message, "Should have non-empty coach response"
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_introduction())
