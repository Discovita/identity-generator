from typing import Dict, Any, List, Optional
from uuid import UUID
import json
import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func

from .interface import DatabaseInterface
from .models.state import StateRecord
from .models.context import ContextRecord
from .models.identity import IdentityRecord
from .models.user import UserRecord

# Set up logging
logger = logging.getLogger(__name__)

# Define SQLAlchemy models
Base = declarative_base()

class StateTable(Base):
    """SQLAlchemy model for state records."""
    __tablename__ = "states"
    
    user_id = Column(String, primary_key=True)
    session_id = Column(String, primary_key=True)
    state = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ContextTable(Base):
    """SQLAlchemy model for context records."""
    __tablename__ = "contexts"
    
    user_id = Column(String, primary_key=True)
    session_id = Column(String, primary_key=True)
    messages = Column(JSON, nullable=False)
    user_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class IdentityTable(Base):
    """SQLAlchemy model for identity records."""
    __tablename__ = "identities"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class UserTable(Base):
    """SQLAlchemy model for user records."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class SQLDatabase(DatabaseInterface):
    """SQL implementation of the database interface."""
    
    def __init__(self, connection_string: str):
        """Initialize the SQL database."""
        self.engine = create_async_engine(connection_string)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
    
    async def initialize(self):
        """Initialize the database by creating tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    # State operations
    
    async def get_state(self, user_id: str, session_id: str) -> Optional[StateRecord]:
        """Get the current state for a user session."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(StateTable).where(
                    StateTable.user_id == user_id,
                    StateTable.session_id == session_id
                )
            )
            state_row = result.scalar_one_or_none()
            
            if state_row:
                return StateRecord(
                    user_id=state_row.user_id,
                    session_id=state_row.session_id,
                    state=state_row.state
                )
            return None
    
    async def save_state(self, state: StateRecord) -> None:
        """Save a state record."""
        async with self.session_maker() as session:
            # Check if state exists
            result = await session.execute(
                select(StateTable).where(
                    StateTable.user_id == state.user_id,
                    StateTable.session_id == state.session_id
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                # Update existing state
                await session.execute(
                    update(StateTable)
                    .where(
                        StateTable.user_id == state.user_id,
                        StateTable.session_id == state.session_id
                    )
                    .values(state=state.state)
                )
            else:
                # Insert new state
                await session.execute(
                    insert(StateTable).values(
                        user_id=state.user_id,
                        session_id=state.session_id,
                        state=state.state
                    )
                )
            
            await session.commit()
    
    async def delete_state(self, user_id: str, session_id: str) -> None:
        """Delete a state record."""
        async with self.session_maker() as session:
            await session.execute(
                delete(StateTable).where(
                    StateTable.user_id == user_id,
                    StateTable.session_id == session_id
                )
            )
            await session.commit()
    
    # Context operations
    
    async def get_context(self, user_id: str, session_id: str) -> Optional[ContextRecord]:
        """Get the context for a user session."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(ContextTable).where(
                    ContextTable.user_id == user_id,
                    ContextTable.session_id == session_id
                )
            )
            context_row = result.scalar_one_or_none()
            
            if context_row:
                return ContextRecord(
                    user_id=context_row.user_id,
                    session_id=context_row.session_id,
                    messages=context_row.messages,
                    user_data=context_row.user_data
                )
            return None
    
    async def save_context(self, context: ContextRecord) -> None:
        """Save a context record."""
        async with self.session_maker() as session:
            # Check if context exists
            result = await session.execute(
                select(ContextTable).where(
                    ContextTable.user_id == context.user_id,
                    ContextTable.session_id == context.session_id
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                # Update existing context
                await session.execute(
                    update(ContextTable)
                    .where(
                        ContextTable.user_id == context.user_id,
                        ContextTable.session_id == context.session_id
                    )
                    .values(
                        messages=context.messages,
                        user_data=context.user_data
                    )
                )
            else:
                # Insert new context
                await session.execute(
                    insert(ContextTable).values(
                        user_id=context.user_id,
                        session_id=context.session_id,
                        messages=context.messages,
                        user_data=context.user_data
                    )
                )
            
            await session.commit()
    
    async def delete_context(self, user_id: str, session_id: str) -> None:
        """Delete a context record."""
        async with self.session_maker() as session:
            await session.execute(
                delete(ContextTable).where(
                    ContextTable.user_id == user_id,
                    ContextTable.session_id == session_id
                )
            )
            await session.commit()
    
    # Identity operations
    
    async def get_identities(self, user_id: str) -> List[IdentityRecord]:
        """Get all identities for a user."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(IdentityTable).where(
                    IdentityTable.user_id == user_id
                )
            )
            identity_rows = result.scalars().all()
            
            return [
                IdentityRecord(
                    id=UUID(row.id),
                    user_id=row.user_id,
                    name=row.name,
                    category=row.category,
                    description=row.description
                )
                for row in identity_rows
            ]
    
    async def save_identity(
        self,
        user_id: str,
        identity: str,
        category: str,
        description: str = ""
    ) -> IdentityRecord:
        """Save an identity record."""
        identity_record = IdentityRecord(
            user_id=user_id,
            name=identity,
            category=category,
            description=description
        )
        
        async with self.session_maker() as session:
            await session.execute(
                insert(IdentityTable).values(
                    id=str(identity_record.id),
                    user_id=identity_record.user_id,
                    name=identity_record.name,
                    category=identity_record.category,
                    description=identity_record.description
                )
            )
            await session.commit()
        
        return identity_record
    
    async def delete_identity(self, user_id: str, identity_id: UUID) -> None:
        """Delete an identity record."""
        async with self.session_maker() as session:
            await session.execute(
                delete(IdentityTable).where(
                    IdentityTable.user_id == user_id,
                    IdentityTable.id == str(identity_id)
                )
            )
            await session.commit()
    
    # User operations
    
    async def get_user(self, user_id: str) -> Optional[UserRecord]:
        """Get a user record."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(UserTable).where(
                    UserTable.id == user_id
                )
            )
            user_row = result.scalar_one_or_none()
            
            if user_row:
                return UserRecord(
                    id=user_row.id,
                    data=user_row.data
                )
            return None
    
    async def save_user(self, user: UserRecord) -> None:
        """Save a user record."""
        async with self.session_maker() as session:
            # Check if user exists
            result = await session.execute(
                select(UserTable).where(
                    UserTable.id == user.id
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                # Update existing user
                await session.execute(
                    update(UserTable)
                    .where(UserTable.id == user.id)
                    .values(data=user.data)
                )
            else:
                # Insert new user
                await session.execute(
                    insert(UserTable).values(
                        id=user.id,
                        data=user.data
                    )
                )
            
            await session.commit()
    
    async def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Update a specific field in the user data."""
        async with self.session_maker() as session:
            # Get current user data
            result = await session.execute(
                select(UserTable).where(
                    UserTable.id == user_id
                )
            )
            user_row = result.scalar_one_or_none()
            
            if user_row:
                # Update existing user data
                data = user_row.data
                data[key] = value
                
                await session.execute(
                    update(UserTable)
                    .where(UserTable.id == user_id)
                    .values(data=data)
                )
            else:
                # Create new user with data
                await session.execute(
                    insert(UserTable).values(
                        id=user_id,
                        data={key: value}
                    )
                )
            
            await session.commit()
    
    # Session operations
    
    async def get_sessions_for_user(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(StateTable.session_id).where(
                    StateTable.user_id == user_id
                )
            )
            return result.scalars().all()
    
    async def get_user_id_for_session(self, session_id: str) -> Optional[str]:
        """Get the user ID for a session."""
        async with self.session_maker() as session:
            result = await session.execute(
                select(StateTable.user_id).where(
                    StateTable.session_id == session_id
                )
            )
            return result.scalar_one_or_none()
