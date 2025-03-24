"""Tests for the SQL database implementation."""

import pytest
from uuid import UUID
from datetime import datetime
import os
import tempfile

from discovita.db.sql.database import SQLDatabase
from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord
from discovita.service.coach.models.state import CoachingState

import pytest_asyncio

@pytest_asyncio.fixture
async def db():
    """Create a SQL database for testing."""
    # Use SQLite in-memory database for testing
    db = SQLDatabase("sqlite+aiosqlite:///:memory:")
    await db.initialize()
    yield db

@pytest.mark.asyncio
async def test_state_operations(db):
    """Test state operations."""
    # Create a state record
    state = StateRecord(
        user_id="user1",
        session_id="session1",
        state=CoachingState.INTRODUCTION
    )
    
    # Save the state
    await db.save_state(state)
    
    # Get the state
    retrieved_state = await db.get_state("user1", "session1")
    
    # Verify the state
    assert retrieved_state is not None
    assert retrieved_state.user_id == "user1"
    assert retrieved_state.session_id == "session1"
    assert retrieved_state.state == CoachingState.INTRODUCTION
    
    # Delete the state
    await db.delete_state("user1", "session1")
    
    # Verify the state is deleted
    retrieved_state = await db.get_state("user1", "session1")
    assert retrieved_state is None

@pytest.mark.asyncio
async def test_context_operations(db):
    """Test context operations."""
    # Create a context record
    context = ContextRecord(
        user_id="user1",
        session_id="session1",
        messages=[{"role": "user", "content": "Hello"}],
        user_data={"name": "Test User"}
    )
    
    # Save the context
    await db.save_context(context)
    
    # Get the context
    retrieved_context = await db.get_context("user1", "session1")
    
    # Verify the context
    assert retrieved_context is not None
    assert retrieved_context.user_id == "user1"
    assert retrieved_context.session_id == "session1"
    assert len(retrieved_context.messages) == 1
    assert retrieved_context.messages[0]["role"] == "user"
    assert retrieved_context.messages[0]["content"] == "Hello"
    assert retrieved_context.user_data["name"] == "Test User"
    
    # Delete the context
    await db.delete_context("user1", "session1")
    
    # Verify the context is deleted
    retrieved_context = await db.get_context("user1", "session1")
    assert retrieved_context is None

@pytest.mark.asyncio
async def test_identity_operations(db):
    """Test identity operations."""
    # Create an identity
    identity = await db.save_identity(
        user_id="user1",
        identity="Creative Visionary",
        category="passions_and_talents",
        description="I am a creative visionary"
    )
    
    # Verify the identity
    assert identity is not None
    assert identity.user_id == "user1"
    assert identity.name == "Creative Visionary"
    assert identity.category == "passions_and_talents"
    assert identity.description == "I am a creative visionary"
    
    # Get identities
    identities = await db.get_identities("user1")
    
    # Verify the identities
    assert len(identities) == 1
    assert identities[0].user_id == "user1"
    assert identities[0].name == "Creative Visionary"
    
    # Delete the identity
    await db.delete_identity("user1", identity.id)
    
    # Verify the identity is deleted
    identities = await db.get_identities("user1")
    assert len(identities) == 0

@pytest.mark.asyncio
async def test_user_operations(db):
    """Test user operations."""
    # Create a user record
    user = UserRecord(
        id="user1",
        data={"name": "Test User", "email": "test@example.com"}
    )
    
    # Save the user
    await db.save_user(user)
    
    # Get the user
    retrieved_user = await db.get_user("user1")
    
    # Verify the user
    assert retrieved_user is not None
    assert retrieved_user.id == "user1"
    assert retrieved_user.data["name"] == "Test User"
    assert retrieved_user.data["email"] == "test@example.com"
    
    # Update user data
    await db.update_user_data("user1", "age", 30)
    
    # Verify the update
    retrieved_user = await db.get_user("user1")
    assert retrieved_user.data["age"] == 30
    
    # Create a new user with update_user_data
    await db.update_user_data("user2", "name", "New User")
    
    # Verify the new user
    retrieved_user = await db.get_user("user2")
    assert retrieved_user is not None
    assert retrieved_user.id == "user2"
    assert retrieved_user.data["name"] == "New User"

@pytest.mark.asyncio
async def test_session_operations(db):
    """Test session operations."""
    # Create state records for multiple sessions
    await db.save_state(StateRecord(user_id="user1", session_id="session1", state=CoachingState.INTRODUCTION))
    await db.save_state(StateRecord(user_id="user1", session_id="session2", state=CoachingState.IDENTITY_BRAINSTORMING))
    await db.save_state(StateRecord(user_id="user2", session_id="session3", state=CoachingState.INTRODUCTION))
    
    # Get sessions for user
    sessions = await db.get_sessions_for_user("user1")
    
    # Verify the sessions
    assert len(sessions) == 2
    assert "session1" in sessions
    assert "session2" in sessions
    
    # Get user ID for session
    user_id = await db.get_user_id_for_session("session3")
    
    # Verify the user ID
    assert user_id == "user2"

@pytest.mark.asyncio
async def test_generic_operations(db):
    """Test generic operations."""
    # Create a state record
    state = StateRecord(
        user_id="user1",
        session_id="session1",
        state=CoachingState.INTRODUCTION
    )
    
    # Save using generic save
    saved_state = await db.save(state)
    
    # Get using generic get
    retrieved_state = await db.get(StateRecord, user_id="user1", session_id="session1")
    
    # Verify the state
    assert retrieved_state is not None
    assert retrieved_state.user_id == "user1"
    assert retrieved_state.state == CoachingState.INTRODUCTION
    
    # Update using generic update
    await db.update(
        StateRecord,
        keys={"user_id": "user1", "session_id": "session1"},
        values={"state": CoachingState.IDENTITY_BRAINSTORMING}
    )
    
    # Verify the update
    retrieved_state = await db.get(StateRecord, user_id="user1", session_id="session1")
    assert retrieved_state.state == CoachingState.IDENTITY_BRAINSTORMING
    
    # Delete using generic delete
    await db.delete(StateRecord, user_id="user1", session_id="session1")
    
    # Verify the delete
    retrieved_state = await db.get(StateRecord, user_id="user1", session_id="session1")
    assert retrieved_state is None
    
    # Test get_all
    await db.save(StateRecord(user_id="user1", session_id="session1", state=CoachingState.INTRODUCTION))
    await db.save(StateRecord(user_id="user1", session_id="session2", state=CoachingState.IDENTITY_BRAINSTORMING))
    
    # Get all states for user1
    states = await db.get_all(StateRecord, user_id="user1")
    
    # Verify the states
    assert len(states) == 2
    assert any(s.session_id == "session1" for s in states)
    assert any(s.session_id == "session2" for s in states)
