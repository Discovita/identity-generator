"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar('T')  # Domain model type
K = TypeVar('K')  # Key type

class Repository(Generic[T, K], ABC):
    """Generic repository interface.
    
    This defines the contract for all repositories. Each repository implementation
    must handle conversion between domain models and storage models.
    
    Type Parameters:
        T: Domain model type (e.g., State, Context)
        K: Key type for the model (e.g., tuple[str, str] for user_id+session_id)
    """
    
    @abstractmethod
    async def get(self, key: K) -> Optional[T]:
        """Get a record by its key."""
        pass
    
    @abstractmethod
    async def get_all(self, **filters: Dict[str, Any]) -> List[T]:
        """Get all records matching the filters."""
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save a record."""
        pass
    
    @abstractmethod
    async def delete(self, key: K) -> None:
        """Delete a record by its key."""
        pass
    
    @abstractmethod
    async def update(self, key: K, values: Dict[str, Any]) -> None:
        """Update specific fields in a record."""
        pass
