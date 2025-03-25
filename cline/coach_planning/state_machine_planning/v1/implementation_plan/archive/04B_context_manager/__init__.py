from .manager import ContextManager
from .persistence import ContextPersistence, FileContextPersistence, DatabaseContextPersistence

def create_context_manager(
    llm_client, 
    persistence: ContextPersistence = None,
    max_recent_messages: int = 10
) -> ContextManager:
    """Create and configure a context manager."""
    if persistence is None:
        persistence = FileContextPersistence()
    
    manager = ContextManager(
        llm_client=llm_client,
        max_recent_messages=max_recent_messages
    )
    
    return manager

__all__ = [
    'ContextManager',
    'ContextPersistence',
    'FileContextPersistence',
    'DatabaseContextPersistence',
    'create_context_manager'
]
