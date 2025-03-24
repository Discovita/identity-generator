"""SQL implementation of the database interface."""

from typing import Dict, Any, List, Optional, Type, cast
from uuid import UUID
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

from discovita.db.interface import DatabaseInterface, T
from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord
from discovita.db.sql.models import Base, StateTable, ContextTable, IdentityTable, UserTable
from discovita.db.sql.operations import (
    get_record, get_all_records, save_record, delete_record, update_record
)

# Set up logging
logger = logging.getLogger(__name__)

class SQLDatabase(DatabaseInterface):
    """SQL implementation of the database interface."""
    
    def __init__(self, connection_string: str):
        """Initialize the SQL database."""
        self.engine = create_async_engine(connection_string)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
        logger.info(f"Initialized SQL database with connection string: {connection_string}")
        
        # Map model types to table classes
        self.model_to_table = {
            StateRecord: StateTable,
            ContextRecord: ContextTable,
            IdentityRecord: IdentityTable,
            UserRecord: UserTable
        }
    
    async def initialize(self):
        """Initialize the database by creating tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Created database tables")
    
    def _get_table_for_model(self, model_type: Type[T]) -> Type:
        """Get the SQLAlchemy table class for a model type."""
        if model_type not in self.model_to_table:
            raise ValueError(f"Unknown model type: {model_type}")
        return self.model_to_table[model_type]
    
    # Generic operations
    
    async def get(self, model_type: Type[T], **keys) -> Optional[T]:
        """Get a record by its keys."""
        table_class = self._get_table_for_model(model_type)
        
        async with self.session_maker() as session:
            result = await get_record(session, model_type, table_class, **keys)
            return cast(Optional[T], result)
    
    async def get_all(self, model_type: Type[T], **filters) -> List[T]:
        """Get all records matching the filters."""
        table_class = self._get_table_for_model(model_type)
        
        async with self.session_maker() as session:
            results = await get_all_records(session, model_type, table_class, **filters)
            return cast(List[T], results)
    
    async def save(self, record: T) -> T:
        """Save a record."""
        model_type = type(record)
        table_class = self._get_table_for_model(model_type)
        
        async with self.session_maker() as session:
            result = await save_record(session, record, table_class)
            await session.commit()
            return cast(T, result)
    
    async def delete(self, model_type: Type[T], **keys) -> None:
        """Delete a record by its keys."""
        table_class = self._get_table_for_model(model_type)
        
        async with self.session_maker() as session:
            await delete_record(session, table_class, **keys)
            await session.commit()
    
    async def update(self, model_type: Type[T], keys: Dict[str, Any], values: Dict[str, Any]) -> None:
        """Update specific fields in a record."""
        table_class = self._get_table_for_model(model_type)
        
        async with self.session_maker() as session:
            await update_record(session, table_class, keys, values)
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
