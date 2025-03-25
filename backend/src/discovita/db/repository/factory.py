"""Factory for creating repository instances."""

from enum import Enum
from typing import Dict, Type, TypeVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from discovita.db.repository.base import Repository
from discovita.db.repository.sql_state import SQLStateRepository
from discovita.db.repository.memory_state import InMemoryStateRepository
from discovita.db.domain.state import State

T = TypeVar('T')

class RepositoryType(Enum):
    """Type of repository implementation."""
    SQL = "sql"
    MEMORY = "memory"

class RepositoryFactory:
    """Factory for creating repository instances."""
    
    def __init__(self, repository_type: RepositoryType, session: Optional[AsyncSession] = None):
        """Initialize the factory.
        
        Args:
            repository_type: Type of repositories to create
            session: SQLAlchemy session (required for SQL repositories)
        """
        if repository_type == RepositoryType.SQL and not session:
            raise ValueError("SQLAlchemy session required for SQL repositories")
        
        self.repository_type = repository_type
        self.session = session
        
        # Map domain types to repository implementations
        self._repository_map: Dict[Type[T], Dict[RepositoryType, Type[Repository]]] = {
            State: {
                RepositoryType.SQL: SQLStateRepository,
                RepositoryType.MEMORY: InMemoryStateRepository
            }
        }
    
    def get_repository(self, model_type: Type[T]) -> Repository:
        """Get a repository instance for a domain model type.
        
        Args:
            model_type: Domain model class
            
        Returns:
            Repository instance for the model type
            
        Raises:
            KeyError: If no repository implementation exists for the model type
        """
        if model_type not in self._repository_map:
            raise KeyError(f"No repository implementation for {model_type.__name__}")
        
        implementations = self._repository_map[model_type]
        if self.repository_type not in implementations:
            raise KeyError(
                f"No {self.repository_type.value} implementation for {model_type.__name__}"
            )
        
        repo_class = implementations[self.repository_type]
        if self.repository_type == RepositoryType.SQL:
            return repo_class(self.session)
        return repo_class()
