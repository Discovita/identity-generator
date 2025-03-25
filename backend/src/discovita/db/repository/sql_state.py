"""SQL implementation of state repository."""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from discovita.db.repository.base import Repository
from discovita.db.domain.state import State
from discovita.db.sql.state import SQLState

class SQLStateRepository(Repository[State, Tuple[str, str]]):
    """SQL implementation of state repository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_domain(self, sql_state: SQLState) -> State:
        """Convert SQL model to domain model."""
        return State(
            user_id=sql_state.user_id,
            session_id=sql_state.session_id,
            state=sql_state.state_data,
            created_at=sql_state.created_at,
            updated_at=sql_state.updated_at
        )
    
    def _to_sql(self, state: State) -> SQLState:
        """Convert domain model to SQL model."""
        return SQLState(
            user_id=state.user_id,
            session_id=state.session_id,
            state_data=state.state.model_dump(),
            created_at=state.created_at or datetime.utcnow(),
            updated_at=state.updated_at or datetime.utcnow()
        )
    
    async def get(self, key: Tuple[str, str]) -> Optional[State]:
        """Get a state by user_id and session_id."""
        user_id, session_id = key
        stmt = select(SQLState).where(
            SQLState.user_id == user_id,
            SQLState.session_id == session_id
        )
        result = await self.session.execute(stmt)
        sql_state = result.scalar_one_or_none()
        return self._to_domain(sql_state) if sql_state else None
    
    async def get_all(self, **filters: Dict[str, Any]) -> List[State]:
        """Get all states matching the filters."""
        stmt = select(SQLState)
        for key, value in filters.items():
            stmt = stmt.where(getattr(SQLState, key) == value)
        
        result = await self.session.execute(stmt)
        return [self._to_domain(s) for s in result.scalars()]
    
    async def save(self, state: State) -> State:
        """Save a state."""
        sql_state = self._to_sql(state)
        self.session.add(sql_state)
        await self.session.flush()
        return self._to_domain(sql_state)
    
    async def delete(self, key: Tuple[str, str]) -> None:
        """Delete a state by user_id and session_id."""
        user_id, session_id = key
        stmt = delete(SQLState).where(
            SQLState.user_id == user_id,
            SQLState.session_id == session_id
        )
        await self.session.execute(stmt)
    
    async def update(self, key: Tuple[str, str], values: Dict[str, Any]) -> None:
        """Update specific fields in a state."""
        user_id, session_id = key
        stmt = update(SQLState).where(
            SQLState.user_id == user_id,
            SQLState.session_id == session_id
        ).values(**values, updated_at=datetime.utcnow())
        await self.session.execute(stmt)
