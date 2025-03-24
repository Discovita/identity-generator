"""Interface for database operations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypeVar, Generic, Type, Union
from uuid import UUID
from pydantic import BaseModel

from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord

T = TypeVar('T', bound=BaseModel)

class DatabaseInterface(ABC):
    """Interface for database operations."""
    
    # Generic operations
    
    @abstractmethod
    async def get(self, model_type: Type[T], **keys) -> Optional[T]:
        """Get a record by its keys."""
        pass
    
    @abstractmethod
    async def get_all(self, model_type: Type[T], **filters) -> List[T]:
        """Get all records matching the filters."""
        pass
    
    @abstractmethod
    async def save(self, record: T) -> T:
        """Save a record."""
        pass
    
    @abstractmethod
    async def delete(self, model_type: Type[T], **keys) -> None:
        """Delete a record by its keys."""
        pass
    
    @abstractmethod
    async def update(self, model_type: Type[T], keys: Dict[str, Any], values: Dict[str, Any]) -> None:
        """Update specific fields in a record."""
        pass
    
    # Convenience methods for specific models
    
    async def get_state(self, user_id: str, session_id: str) -> Optional[StateRecord]:
        """Get the current state for a user session."""
        return await self.get(StateRecord, user_id=user_id, session_id=session_id)
    
    async def save_state(self, state: StateRecord) -> None:
        """Save a state record."""
        await self.save(state)
    
    async def delete_state(self, user_id: str, session_id: str) -> None:
        """Delete a state record."""
        await self.delete(StateRecord, user_id=user_id, session_id=session_id)
    
    async def get_context(self, user_id: str, session_id: str) -> Optional[ContextRecord]:
        """Get the context for a user session."""
        return await self.get(ContextRecord, user_id=user_id, session_id=session_id)
    
    async def save_context(self, context: ContextRecord) -> None:
        """Save a context record."""
        await self.save(context)
    
    async def delete_context(self, user_id: str, session_id: str) -> None:
        """Delete a context record."""
        await self.delete(ContextRecord, user_id=user_id, session_id=session_id)
    
    async def get_identities(self, user_id: str) -> List[IdentityRecord]:
        """Get all identities for a user."""
        return await self.get_all(IdentityRecord, user_id=user_id)
    
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
        return await self.save(identity_record)
    
    async def delete_identity(self, user_id: str, identity_id: UUID) -> None:
        """Delete an identity record."""
        await self.delete(IdentityRecord, user_id=user_id, id=identity_id)
    
    async def get_user(self, user_id: str) -> Optional[UserRecord]:
        """Get a user record."""
        return await self.get(UserRecord, id=user_id)
    
    async def save_user(self, user: UserRecord) -> None:
        """Save a user record."""
        await self.save(user)
    
    async def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Update a specific field in the user data."""
        user = await self.get_user(user_id)
        if user:
            user.data[key] = value
            await self.save(user)
        else:
            user = UserRecord(id=user_id, data={key: value})
            await self.save(user)
    
    # Session operations
    
    @abstractmethod
    async def get_sessions_for_user(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        pass
    
    @abstractmethod
    async def get_user_id_for_session(self, session_id: str) -> Optional[str]:
        """Get the user ID for a session."""
        pass
