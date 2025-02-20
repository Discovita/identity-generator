"""Tests for coach service models."""

import pytest
from discovita.service.coach.models import (
    ChatMessage,
    Identity,
    IdentityCategory,
    UserProfile,
    CoachRequest,
    CoachResponse
)

def test_chat_message_creation():
    """Test ChatMessage model creation and validation."""
    message = ChatMessage(role="user", content="Hello")
    assert message.role == "user"
    assert message.content == "Hello"

def test_identity_creation():
    """Test Identity model creation and validation."""
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold, beautiful ideas to life",
        visualization={
            "setting": "Modern studio",
            "appearance": "Artistic attire",
            "energy": "Focused and inspired"
        }
    )
    assert identity.category == IdentityCategory.PASSIONS
    assert identity.name == "Creative Visionary"
    assert identity.visualization is not None
    assert identity.visualization.get("setting") == "Modern studio"

def test_user_profile_creation():
    """Test UserProfile model creation and validation."""
    identity = Identity(
        category=IdentityCategory.PASSIONS,
        name="Creative Visionary",
        affirmation="I bring bold ideas to life",
        visualization={
            "setting": "Creative workspace",
            "appearance": "Professional",
            "energy": "Dynamic"
        }
    )
    profile = UserProfile(
        user_id="test_user",
        identities=[identity],
        current_focus=IdentityCategory.PASSIONS
    )
    assert profile.user_id == "test_user"
    assert len(profile.identities) == 1
    assert profile.current_focus == IdentityCategory.PASSIONS

def test_coach_request_creation():
    """Test CoachRequest model creation and validation."""
    message = ChatMessage(role="user", content="Hello")
    profile = UserProfile(
        user_id="test_user",
        current_focus=IdentityCategory.PASSIONS
    )
    request = CoachRequest(
        user_id="test_user",
        message="Hello coach",
        context=[message],
        profile=profile
    )
    assert request.user_id == "test_user"
    assert request.message == "Hello coach"
    assert len(request.context) == 1

def test_coach_response_creation():
    """Test CoachResponse model creation and validation."""
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
    response = CoachResponse(
        message="Let's explore your creative identity",
        suggested_identities=[identity],
        visualization_prompt={
            "setting": "Modern studio",
            "appearance": "Artistic attire",
            "energy": "Focused"
        }
    )
    assert "creative identity" in response.message
    assert response.suggested_identities is not None
    assert len(response.suggested_identities) == 1
    assert response.visualization_prompt is not None
    assert response.visualization_prompt.get("setting") == "Modern studio"
