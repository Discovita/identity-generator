"""Tests for the state store."""

import pytest
from uuid import UUID
from datetime import datetime

from discovita.db.state_store import StateStore, DatabaseStateStore, InMemoryStateStore
from discovita.db.in_memory_db import InMemoryDatabase
from discovita.service.coach.models import CoachContext, CoachingState, ChatMessage, UserProfile, Identity, IdentityCategory

import pytest_asyncio

@pytest_asyncio.fixture
def db():
    """Create an in-memory database for testing."""
    return InMemoryDatabase()

@pytest_asyncio.fixture
def state_store(db):
    """Create a database state store for testing."""
    return DatabaseStateStore(db)

@pytest_asyncio.fixture
def memory_store(db):
    """Create an in-memory state store for testing."""
    return InMemoryStateStore(db)

@pytest.fixture
def sample_context():
    """Create a sample context for testing."""
    return CoachContext(
        user_id="user1",
        current_state=CoachingState.INTRODUCTION,
        conversation_history=[
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there")
        ],
        consolidated_summary="User is new to the system",
        user_profile=UserProfile(
            user_id="user1",
            identities=[
                Identity(
                    category=IdentityCategory.PASSIONS,
                    name="Creative Visionary",
                    affirmation="I am a creative visionary",
                    visualization=None
                )
            ],
            current_focus=IdentityCategory.PASSIONS
        ),
        metadata={"introduction_completed": True}
    )

@pytest.mark.asyncio
async def test_database_state_store_save_load(state_store, sample_context):
    """Test saving and loading context with the database state store."""
    # Save the context
    await state_store.save_context(sample_context, "session1")
    
    # Load the context
    loaded_context = await state_store.load_context("user1", "session1")
    
    # Verify the context
    assert loaded_context is not None
    assert loaded_context.user_id == "user1"
    assert loaded_context.current_state == CoachingState.INTRODUCTION
    assert len(loaded_context.conversation_history) == 2
    assert loaded_context.conversation_history[0].role == "user"
    assert loaded_context.conversation_history[0].content == "Hello"
    assert loaded_context.consolidated_summary == "User is new to the system"
    assert loaded_context.user_profile is not None
    assert len(loaded_context.user_profile.identities) == 1
    assert loaded_context.user_profile.identities[0].name == "Creative Visionary"
    assert loaded_context.user_profile.current_focus == IdentityCategory.PASSIONS
    assert loaded_context.metadata["introduction_completed"] is True

@pytest.mark.asyncio
async def test_in_memory_state_store(memory_store, sample_context):
    """Test the in-memory state store."""
    # Save the context
    await memory_store.save_context(sample_context, "session1")
    
    # Load the context
    loaded_context = await memory_store.load_context("user1", "session1")
    
    # Verify the context
    assert loaded_context is not None
    assert loaded_context.user_id == "user1"
    assert loaded_context.current_state == CoachingState.INTRODUCTION
    
    # Modify the context
    loaded_context.current_state = CoachingState.IDENTITY_BRAINSTORMING
    await memory_store.save_context(loaded_context, "session1")
    
    # Load the context again
    reloaded_context = await memory_store.load_context("user1", "session1")
    
    # Verify the changes
    assert reloaded_context.current_state == CoachingState.IDENTITY_BRAINSTORMING

@pytest.mark.asyncio
async def test_in_memory_state_store_with_db_fallback(db, sample_context):
    """Test the in-memory state store with database fallback."""
    # Create a database state store and save a context
    db_store = DatabaseStateStore(db)
    await db_store.save_context(sample_context, "session1")
    
    # Create an in-memory state store with the same database
    memory_store = InMemoryStateStore(db)
    
    # Load the context (should come from the database)
    loaded_context = await memory_store.load_context("user1", "session1")
    
    # Verify the context
    assert loaded_context is not None
    assert loaded_context.user_id == "user1"
    assert loaded_context.current_state == CoachingState.INTRODUCTION
    
    # Modify the context
    loaded_context.current_state = CoachingState.IDENTITY_BRAINSTORMING
    await memory_store.save_context(loaded_context, "session1")
    
    # Load the context directly from the database
    db_context = await db_store.load_context("user1", "session1")
    
    # Verify the changes were persisted to the database
    assert db_context.current_state == CoachingState.IDENTITY_BRAINSTORMING
