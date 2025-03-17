from typing import Dict, Any, List, Optional
from uuid import UUID

from .interface import DatabaseInterface
from .models.state import StateRecord
from .models.context import ContextRecord
from .models.identity import IdentityRecord
from .models.user import UserRecord

class InMemoryDatabase(DatabaseInterface):
    """In-memory implementation of the database interface."""
    
    def __init__(self):
        """Initialize the in-memory database."""
        self._state_records: Dict[str, StateRecord] = {}
        self._context_records: Dict[str, ContextRecord] = {}
        self._identity_records: Dict[str, List[IdentityRecord]] = {}
        self._user_records: Dict[str, UserRecord] = {}
    
    # State operations
    
    async def get_state(self, user_id: str, session_id: str) -> Optional[StateRecord]:
        """Get the current state for a user session."""
        key = f"{user_id}:{session_id}"
        return self._state_records.get(key)
    
    async def save_state(self, state: StateRecord) -> None:
        """Save a state record."""
        key = f"{state.user_id}:{state.session_id}"
        self._state_records[key] = state
    
    async def delete_state(self, user_id: str, session_id: str) -> None:
        """Delete a state record."""
        key = f"{user_id}:{session_id}"
        if key in self._state_records:
            del self._state_records[key]
    
    # Context operations
    
    async def get_context(self, user_id: str, session_id: str) -> Optional[ContextRecord]:
        """Get the context for a user session."""
        key = f"{user_id}:{session_id}"
        return self._context_records.get(key)
    
    async def save_context(self, context: ContextRecord) -> None:
        """Save a context record."""
        key = f"{context.user_id}:{context.session_id}"
        self._context_records[key] = context
    
    async def delete_context(self, user_id: str, session_id: str) -> None:
        """Delete a context record."""
        key = f"{user_id}:{session_id}"
        if key in self._context_records:
            del self._context_records[key]
    
    # Identity operations
    
    async def get_identities(self, user_id: str) -> List[IdentityRecord]:
        """Get all identities for a user."""
        return self._identity_records.get(user_id, [])
    
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
        
        if user_id not in self._identity_records:
            self._identity_records[user_id] = []
        
        self._identity_records[user_id].append(identity_record)
        return identity_record
    
    async def delete_identity(self, user_id: str, identity_id: UUID) -> None:
        """Delete an identity record."""
        if user_id in self._identity_records:
            self._identity_records[user_id] = [
                i for i in self._identity_records[user_id]
                if i.id != identity_id
            ]
    
    # User operations
    
    async def get_user(self, user_id: str) -> Optional[UserRecord]:
        """Get a user record."""
        return self._user_records.get(user_id)
    
    async def save_user(self, user: UserRecord) -> None:
        """Save a user record."""
        self._user_records[user.id] = user
    
    async def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Update a specific field in the user data."""
        user = self._user_records.get(user_id)
        if user:
            user.data[key] = value
        else:
            user = UserRecord(id=user_id, data={key: value})
            self._user_records[user_id] = user
    
    # Session operations
    
    async def get_sessions_for_user(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        sessions = []
        for key in self._state_records:
            if key.startswith(f"{user_id}:"):
                sessions.append(key.split(":", 1)[1])
        return sessions
    
    async def get_user_id_for_session(self, session_id: str) -> Optional[str]:
        """Get the user ID for a session."""
        for key in self._state_records:
            if key.endswith(f":{session_id}"):
                return key.split(":", 1)[0]
        return None
