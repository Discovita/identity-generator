"""Test configuration and fixtures."""

import os
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from discovita.db.sql.base import Base

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Override database URL for testing
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["USE_SQL_DATABASE"] = "true"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

# Create test session factory
test_session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@pytest.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Set up test database.
    
    This fixture runs automatically for all tests and handles:
    1. Creating all tables before each test
    2. Dropping all tables after each test
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session for testing.
    
    This fixture provides a session with automatic rollback.
    """
    async with test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
