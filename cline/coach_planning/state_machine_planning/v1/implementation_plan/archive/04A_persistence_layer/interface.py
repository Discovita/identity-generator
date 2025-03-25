from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from uuid import UUID

from .models.state import StateRecord
from .models.context import ContextRecord
from .models.identity import IdentityRecord
from .models.user import UserRecord

class DatabaseInterface(ABC):
    """Interface for database operations."""
    
    # State operations
    
    @abstractmethod
    async def get_state(self, user_id: str, session_id: str) -> Optional[StateRecord]:
        """Get the current state for a user session."""
        pass
    
    @abstractmethod
    async def save_state(self, state: StateRecord) -> None:
        """Save a state record."""
        pass
    
    @abstractmethod
    async def delete_state(self, user_id: str, session_id: str) -> None:
        """Delete a state record."""
        pass
    
    # Context operations
    
    @abstractmethod
    async def get_context(self, user_id: str, session_id: str) -> Optional[ContextRecord]:
        """Get the context for a user session."""
        pass
    
    @abstractmethod
    async def save_context(self, context: ContextRecord) -> None:
        """Save a context record."""
        pass
    
    @abstractmethod
    async def delete_context(self, user_id: str, session_id: str) -> None:
        """Delete a context record."""
        pass
    
    # Identity operations
    
    @abstractmethod
    async def get_identities(self, user_id: str) -> List[IdentityRecord]:
        """Get all identities for a user."""
        pass
    
    @abstractmethod
    async def save_identity(
        self,
        user_id: str,
        identity: str,
        category: str,
        description: str = ""
    ) -> IdentityRecord:
        """Save an identity record."""
        pass
    
    @abstractmethod
    async def delete_identity(self, user_id: str, identity_id: UUID) -> None:
        """Delete an identity record."""
        pass
    
    # User operations
    
    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[UserRecord]:
        """Get a user record."""
        pass
    
    @abstractmethod
    async def save_user(self, user: UserRecord) -> None:
        """Save a user record."""
        pass
    
    @abstractmethod
    async def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Update a specific field in the user data."""
        pass
    
    # Session operations
    
    @abstractmethod
    async def get_sessions_for_user(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        pass
    
    @abstractmethod
    async def get_user_id_for_session(self, session_id: str) -> Optional[str]:
        """Get the user ID for a session."""
        pass
