"""Tests for coach service context models."""

from discovita.service.coach.models import (
    CoachingState,
    CoachContext,
    ChatMessage,
    UserProfile,
    Identity,
    IdentityCategory
)

def test_coach_context_prompt_formatting():
    """Test the CoachContext's get_prompt_context method formats data correctly."""
    # Create test data
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold ideas to life",
        visualization=None
    )
    
    profile = UserProfile(
        user_id="test_user",
        identities=[identity],
        current_focus=IdentityCategory.PASSIONS
    )
    
    conversation = [
        ChatMessage(role="user", content="Hello, I'm looking for guidance"),
        ChatMessage(role="assistant", content="I'm here to help you discover your identities")
    ]
    
    # Create context with all data populated
    context = CoachContext(
        user_id="test_user",
        current_state=CoachingState.IDENTITY_BRAINSTORMING,
        conversation_history=conversation,
        consolidated_summary="User is interested in creative pursuits",
        user_profile=profile,
        metadata={"session_count": 3}
    )
    
    # Get formatted context
    prompt_context = context.get_prompt_context()
    
    # Verify formatting
    assert prompt_context["user_summary"] == "User is interested in creative pursuits"
    assert "User: Hello, I'm looking for guidance" in prompt_context["recent_messages"]
    assert "Assistant: I'm here to help you" in prompt_context["recent_messages"]
    assert "- PASSIONS: Creative Visionary" in prompt_context["identities"]
    assert prompt_context["current_focus"] == "PASSIONS"
    assert prompt_context["state"] == "identity_brainstorming"
    assert prompt_context["session_count"] == 3

def test_coach_context_with_missing_data():
    """Test the CoachContext handles missing optional data gracefully."""
    # Create minimal context
    context = CoachContext(
        user_id="test_user",
        current_state=CoachingState.INTRODUCTION
    )
    
    # Get formatted context
    prompt_context = context.get_prompt_context()
    
    # Verify defaults for missing data
    assert prompt_context["user_summary"] == ""
    assert prompt_context["recent_messages"] == ""
    assert prompt_context["identities"] == ""
    assert prompt_context["current_focus"] == "None"
    assert prompt_context["state"] == "introduction"
