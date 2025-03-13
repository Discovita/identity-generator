"""Tests for coach service context builder."""

from discovita.service.coach.context_builder import ContextBuilder
from discovita.service.coach.models import (
    ChatMessage,
    Identity,
    IdentityCategory,
    UserProfile
)

def test_context_builder_initialization():
    """Test ContextBuilder initialization loads sample dialogue."""
    builder = ContextBuilder()
    assert hasattr(builder, "sample_dialogue")

def test_build_context_with_basic_messages():
    """Test building context with just messages."""
    builder = ContextBuilder()
    messages = [
        ChatMessage(role="user", content="Hello"),
        ChatMessage(role="assistant", content="Hi there")
    ]
    context = builder.build_context(messages, None)
    assert "system: " in context
    assert "user: Hello" in context
    assert "assistant: Hi there" in context

def test_build_context_with_profile():
    """Test building context with user profile."""
    builder = ContextBuilder()
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold ideas to life",
        visualization={
            "setting": "Creative workspace",
            "appearance": "Professional attire",
            "energy": "Dynamic and focused"
        }
    )
    profile = UserProfile(
        user_id="test_user",
        identities=[identity],
        current_focus=IdentityCategory.PASSIONS
    )
    messages = [ChatMessage(role="user", content="Hello")]
    
    context = builder.build_context(messages, profile)
    assert "Creative Visionary" in context
    assert "PASSIONS" in context
    assert "user: Hello" in context

def test_build_context_with_sample_dialogue():
    """Test context includes sample dialogue when available."""
    builder = ContextBuilder()
    # Temporarily set sample dialogue for testing
    builder.sample_dialogue = "Example dialogue content"
    
    messages = [ChatMessage(role="user", content="Hello")]
    context = builder.build_context(messages, None)
    assert "Example dialogue content" in context

def test_build_context_maintains_message_order():
    """Test context maintains correct message order."""
    builder = ContextBuilder()
    messages = [
        ChatMessage(role="user", content="First message"),
        ChatMessage(role="assistant", content="First response"),
        ChatMessage(role="user", content="Second message")
    ]
    context = builder.build_context(messages, None)
    
    # Extract just the user and assistant messages from the context
    context_lines = context.split('\n')
    user_assistant_lines = [line for line in context_lines 
                           if line.startswith("user:") or line.startswith("assistant:")]
    
    # Check that the messages appear in the correct order
    assert user_assistant_lines[0] == "user: First message"
    assert user_assistant_lines[1] == "assistant: First response"
    assert user_assistant_lines[2] == "user: Second message"
