"""Tests for state repository implementations."""

import pytest
from datetime import datetime
from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession

from discovita.service.coach.models.state import CoachingState
from discovita.db.domain.state import State
from discovita.db.repository.base import Repository
from discovita.db.repository.memory_state import InMemoryStateRepository
from discovita.db.repository.factory import RepositoryFactory, RepositoryType

@pytest.fixture
async def memory_repo() -> InMemoryStateRepository:
    """Get an in-memory repository."""
    return InMemoryStateRepository()

@pytest.fixture
async def sql_repo(db_session: AsyncSession) -> Repository[State, Any]:
    """Get a SQL repository."""
    factory = RepositoryFactory(RepositoryType.SQL, db_session)
    return factory.get_repository(State)

@pytest.mark.parametrize("repo_fixture", ["memory_repo", "sql_repo"])
@pytest.mark.asyncio
async def test_save_and_get_state(request, repo_fixture: str):
    """Test saving and retrieving a state."""
    repo = request.getfixturevalue(repo_fixture)
    
    # Create test state
    state = State(
        user_id="test_user",
        session_id="test_session",
        state=CoachingState.INTRODUCTION
    )
    
    # Save state
    saved_state = await repo.save(state)
    assert saved_state.user_id == state.user_id
    assert saved_state.session_id == state.session_id
    assert saved_state.state == CoachingState.INTRODUCTION
    assert saved_state.created_at is not None
    assert saved_state.updated_at is not None
    
    # Get state
    retrieved_state = await repo.get(state.key)
    assert retrieved_state is not None
    assert retrieved_state.user_id == state.user_id
    assert retrieved_state.session_id == state.session_id
    assert retrieved_state.state == CoachingState.INTRODUCTION

@pytest.mark.parametrize("repo_fixture", ["memory_repo", "sql_repo"])
@pytest.mark.asyncio
async def test_update_state(request, repo_fixture: str):
    """Test updating a state."""
    repo = request.getfixturevalue(repo_fixture)
    
    # Create and save initial state
    state = State(
        user_id="test_user",
        session_id="test_session",
        state=CoachingState.INTRODUCTION
    )
    await repo.save(state)
    
    # Update state
    await repo.update(
        state.key,
        {"state": CoachingState.IDENTITY_BRAINSTORMING}
    )
    
    # Verify update
    updated_state = await repo.get(state.key)
    assert updated_state is not None
    assert updated_state.state == CoachingState.IDENTITY_BRAINSTORMING
    assert updated_state.updated_at > updated_state.created_at

@pytest.mark.parametrize("repo_fixture", ["memory_repo", "sql_repo"])
@pytest.mark.asyncio
async def test_delete_state(request, repo_fixture: str):
    """Test deleting a state."""
    repo = request.getfixturevalue(repo_fixture)
    
    # Create and save state
    state = State(
        user_id="test_user",
        session_id="test_session",
        state=CoachingState.INTRODUCTION
    )
    await repo.save(state)
    
    # Delete state
    await repo.delete(state.key)
    
    # Verify deletion
    deleted_state = await repo.get(state.key)
    assert deleted_state is None

@pytest.mark.parametrize("repo_fixture", ["memory_repo", "sql_repo"])
@pytest.mark.asyncio
async def test_get_all_states(request, repo_fixture: str):
    """Test getting all states with filters."""
    repo = request.getfixturevalue(repo_fixture)
    
    # Create test states
    states = [
        State(
            user_id="user1",
            session_id="session1",
            state=CoachingState.INTRODUCTION
        ),
        State(
            user_id="user1",
            session_id="session2",
            state=CoachingState.IDENTITY_BRAINSTORMING
        ),
        State(
            user_id="user2",
            session_id="session1",
            state=CoachingState.INTRODUCTION
        )
    ]
    
    # Save all states
    for state in states:
        await repo.save(state)
    
    # Get states for user1
    user1_states = await repo.get_all(user_id="user1")
    assert len(user1_states) == 2
    assert all(s.user_id == "user1" for s in user1_states)
    
    # Get states for session1
    session1_states = await repo.get_all(session_id="session1")
    assert len(session1_states) == 2
    assert all(s.session_id == "session1" for s in session1_states)
