"""In-memory implementation of the database interface."""

from typing import Dict, Any, List, Optional, Tuple, Type, TypeVar, Generic, cast
from uuid import UUID
from datetime import datetime
import logging
from pydantic import BaseModel

from discovita.db.interface import DatabaseInterface, T
from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord

# Set up logging
logger = logging.getLogger(__name__)

class InMemoryDatabase(DatabaseInterface):
    """In-memory implementation of the database interface."""
    
    def __init__(self):
        """Initialize the in-memory database."""
        # Store records by model type and primary key
        self.storage: Dict[Type[BaseModel], Dict[Tuple, BaseModel]] = {
            StateRecord: {},
            ContextRecord: {},
            IdentityRecord: {},
            UserRecord: {}
        }
        self.session_user_map: Dict[str, str] = {}
        logger.info("Initialized in-memory database")
    
    def _get_key_for_model(self, model_type: Type[T], **keys) -> Optional[Tuple]:
        """Get the primary key tuple for a model type."""
        # Handle composite keys for specific models
        if model_type == StateRecord or model_type == ContextRecord:
            return (keys["user_id"], keys["session_id"])
        elif model_type == IdentityRecord:
            if "id" in keys:
                return (keys["user_id"], keys["id"])
            else:
                return None  # Can't get a specific identity without an ID
        
        # Default handling for models with 'id' as primary key
        if "id" in keys:
            return (keys["id"],)
        
        return None
    
    def _get_model_storage(self, model_type: Type[T]) -> Dict[Tuple, T]:
        """Get the storage dictionary for a model type."""
        if model_type not in self.storage:
            # Initialize storage for new model types
            self.storage[model_type] = {}
            logger.info(f"Initialized storage for model type: {model_type.__name__}")
        return cast(Dict[Tuple, T], self.storage[model_type])
    
    # Generic operations
    
    async def get(self, model_type: Type[T], **keys) -> Optional[T]:
        """Get a record by its keys."""
        key = self._get_key_for_model(model_type, **keys)
        if key is None:
            return None
        
        storage = self._get_model_storage(model_type)
        return storage.get(key)
    
    async def get_all(self, model_type: Type[T], **filters) -> List[T]:
        """Get all records matching the filters."""
        storage = self._get_model_storage(model_type)
        
        # Filter records based on provided filters
        result = []
        for record in storage.values():
            match = True
            for key, value in filters.items():
                if getattr(record, key, None) != value:
                    match = False
                    break
            if match:
                result.append(record)
        
        return result
    
    async def save(self, record: T) -> T:
        """Save a record."""
        model_type = type(record)
        
        # Set timestamps if the model has them
        now = datetime.now()
        if hasattr(record, "created_at") and not getattr(record, "created_at"):
            setattr(record, "created_at", now)
        if hasattr(record, "updated_at"):
            setattr(record, "updated_at", now)
        
        # Get the key for the record
        key_dict = {}
        if model_type == StateRecord or model_type == ContextRecord:
            key_dict = {"user_id": record.user_id, "session_id": record.session_id}
            # Update session user map
            self.session_user_map[record.session_id] = record.user_id
        elif model_type == IdentityRecord:
            key_dict = {"user_id": record.user_id, "id": record.id}
        elif hasattr(record, "id"):
            # Default handling for models with 'id' field
            key_dict = {"id": record.id}
        
        key = self._get_key_for_model(model_type, **key_dict)
        
        # Save the record
        storage = self._get_model_storage(model_type)
        storage[key] = record
        
        return record
    
    async def delete(self, model_type: Type[T], **keys) -> None:
        """Delete a record by its keys."""
        key = self._get_key_for_model(model_type, **keys)
        if key is None:
            return
        
        storage = self._get_model_storage(model_type)
        if key in storage:
            del storage[key]
    
    async def update(self, model_type: Type[T], keys: Dict[str, Any], values: Dict[str, Any]) -> None:
        """Update specific fields in a record."""
        record = await self.get(model_type, **keys)
        if record:
            for key, value in values.items():
                setattr(record, key, value)
            
            if hasattr(record, "updated_at"):
                setattr(record, "updated_at", datetime.now())
            
            await self.save(record)
    
    # Session operations
    
    async def get_sessions_for_user(self, user_id: str) -> List[str]:
        """Get all session IDs for a user."""
        return [
            session_id for session_id, uid in self.session_user_map.items()
            if uid == user_id
        ]
    
    async def get_user_id_for_session(self, session_id: str) -> Optional[str]:
        """Get the user ID for a session."""
        return self.session_user_map.get(session_id)
