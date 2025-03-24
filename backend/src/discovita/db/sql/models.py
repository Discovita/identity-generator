"""SQLAlchemy models for the SQL database implementation."""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func

# Define SQLAlchemy models
Base = declarative_base()

class StateTable(Base):
    """SQLAlchemy model for state records."""
    __tablename__ = "states"
    
    user_id = Column(String, primary_key=True)
    session_id = Column(String, primary_key=True)
    state = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ContextTable(Base):
    """SQLAlchemy model for context records."""
    __tablename__ = "contexts"
    
    user_id = Column(String, primary_key=True)
    session_id = Column(String, primary_key=True)
    messages = Column(JSON, nullable=False)
    user_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class IdentityTable(Base):
    """SQLAlchemy model for identity records."""
    __tablename__ = "identities"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class UserTable(Base):
    """SQLAlchemy model for user records."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
