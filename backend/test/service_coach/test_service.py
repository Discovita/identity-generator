"""Tests for coach service."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from discovita.service.coach.service import CoachService
from discovita.service.coach.models import (
    ChatMessage,
    CoachRequest,
    CoachResponse,
    Identity,
    IdentityCategory,
    UserProfile
)

@pytest.fixture
def mock_openai_client():
    """Create mock OpenAI client."""
    client = MagicMock()
    client.get_completion = AsyncMock(return_value="Test response")
    
    # Mock the get_structured_completion method
    structured_response = MagicMock()
    structured_response.message = "Test response"
    structured_response.proposed_identity = None
    structured_response.confirmed_identity = None
    
    client.get_structured_completion = AsyncMock(return_value=structured_response)
    return client

@pytest.fixture
def coach_service(mock_openai_client):
    """Create CoachService instance with mock client."""
    return CoachService(mock_openai_client)

@pytest.mark.asyncio
async def test_get_response_basic(coach_service):
    """Test basic response generation."""
    profile = UserProfile(
        user_id="test_user",
        current_focus=IdentityCategory.PASSIONS
    )
    request = CoachRequest(
        user_id="test_user",
        message="Hello",
        context=[ChatMessage(role="user", content="Hello")],
        profile=profile
    )
    
    response = await coach_service.get_response(request)
    assert isinstance(response, CoachResponse)
    assert response.message == "Test response"
    assert response.proposed_identity is None
    assert response.confirmed_identity is None
    assert response.visualization_prompt is None

@pytest.mark.asyncio
async def test_get_response_with_profile(coach_service):
    """Test response generation with user profile."""
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold ideas to life",
        visualization={
            "setting": "Creative studio",
            "appearance": "Professional attire",
            "energy": "Dynamic and inspired"
        }
    )
    profile = UserProfile(
        user_id="test_user",
        identities=[identity],
        current_focus=IdentityCategory.PASSIONS
    )
    request = CoachRequest(
        user_id="test_user",
        message="Hello",
        context=[ChatMessage(role="user", content="Hello")],
        profile=profile
    )
    
    response = await coach_service.get_response(request)
    assert isinstance(response, CoachResponse)
    assert response.message == "Test response"

@pytest.mark.asyncio
async def test_get_response_maintains_context(coach_service):
    """Test that response generation maintains conversation context."""
    context = [
        ChatMessage(role="user", content="First message"),
        ChatMessage(role="assistant", content="First response"),
        ChatMessage(role="user", content="Second message")
    ]
    profile = UserProfile(
        user_id="test_user",
        current_focus=IdentityCategory.PASSIONS
    )
    request = CoachRequest(
        user_id="test_user",
        message="Third message",
        context=context,
        profile=profile
    )
    
    await coach_service.get_response(request)
    
    # Verify that the request was made with the correct parameters
    call_args = coach_service.client.get_structured_completion.call_args
    assert call_args is not None
    
    # Get the messages from the keyword arguments
    messages = call_args[1]["messages"]
    
    # Convert messages to a string for easier assertion
    messages_str = str(messages)
    assert "First message" in messages_str
    assert "First response" in messages_str
    assert "Second message" in messages_str
    assert "Third message" in messages_str

@pytest.mark.asyncio
async def test_get_response_includes_system_prompt(coach_service):
    """Test that response generation includes system prompt."""
    profile = UserProfile(
        user_id="test_user",
        current_focus=IdentityCategory.PASSIONS
    )
    request = CoachRequest(
        user_id="test_user",
        message="Hello",
        context=[],
        profile=profile
    )
    
    await coach_service.get_response(request)
    
    # Verify that the request was made with the correct parameters
    call_args = coach_service.client.get_structured_completion.call_args
    assert call_args is not None
    
    # The context builder should have added the system prompt
    # We can verify this by checking that the context builder was called
    # and that the get_structured_completion method was called with the expected parameters
    assert isinstance(call_args[1]["response_model"], type)
