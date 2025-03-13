"""Persistence layer implementation for the coach state machine."""

from .interface import DatabaseInterface
from .in_memory_db import InMemoryDatabase
from .sql_db import SQLDatabase
from .factory import DatabaseType, create_database, initialize_database
from .models import StateRecord, ContextRecord, IdentityRecord, UserRecord

__all__ = [
    'DatabaseInterface',
    'InMemoryDatabase',
    'SQLDatabase',
    'DatabaseType',
    'create_database',
    'initialize_database',
    'StateRecord',
    'ContextRecord',
    'IdentityRecord',
    'UserRecord'
]
