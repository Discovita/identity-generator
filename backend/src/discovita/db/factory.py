"""Factory for creating database instances."""

from typing import Optional
import logging
from enum import Enum, auto

from discovita.db.interface import DatabaseInterface
from discovita.db.in_memory_db import InMemoryDatabase
from discovita.db.sql.database import SQLDatabase

# Set up logging
logger = logging.getLogger(__name__)

class DatabaseType(Enum):
    """Enum for database types."""
    MEMORY = auto()
    SQL = auto()

def create_database(
    db_type: DatabaseType,
    connection_string: Optional[str] = None
) -> DatabaseInterface:
    """
    Create a database implementation based on the specified type.
    
    Args:
        db_type: The type of database to create (DatabaseType.MEMORY, DatabaseType.SQL)
        connection_string: The connection string for the database (required for SQL)
    
    Returns:
        An implementation of the DatabaseInterface
    
    Raises:
        ValueError: If an invalid database type is specified or if a required parameter is missing
    """
    if db_type == DatabaseType.MEMORY:
        logger.info("Creating in-memory database")
        return InMemoryDatabase()
    
    elif db_type == DatabaseType.SQL:
        if not connection_string:
            raise ValueError("Connection string is required for SQL database")
        
        logger.info(f"Creating SQL database with connection string: {connection_string}")
        return SQLDatabase(connection_string)
    
    else:
        raise ValueError(f"Unknown database type: {db_type}")

async def initialize_database(db: DatabaseInterface) -> None:
    """
    Initialize the database if needed.
    
    Args:
        db: The database implementation to initialize
    """
    # Check if the database has an initialize method
    if hasattr(db, "initialize") and callable(getattr(db, "initialize")):
        logger.info("Initializing database")
        await db.initialize()
    else:
        logger.info("Database does not require initialization")
