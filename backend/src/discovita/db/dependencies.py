"""Database dependencies for FastAPI."""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from discovita.config import get_settings
from discovita.db.repository.factory import RepositoryFactory, RepositoryType
from discovita.db.sql.session import get_session

settings = get_settings()

async def get_repository_factory(
    session: AsyncSession = Depends(get_session)
) -> AsyncGenerator[RepositoryFactory, None]:
    """Get a repository factory.
    
    This dependency provides a repository factory configured based on settings.
    For SQL repositories, it automatically manages the database session.
    
    Args:
        session: Database session (injected by FastAPI)
        
    Yields:
        RepositoryFactory: Factory for creating repositories
    """
    repo_type = (
        RepositoryType.SQL if settings.use_sql_database
        else RepositoryType.MEMORY
    )
    
    factory = RepositoryFactory(
        repository_type=repo_type,
        session=session if repo_type == RepositoryType.SQL else None
    )
    
    try:
        yield factory
    finally:
        # Session cleanup is handled by get_session dependency
        pass
