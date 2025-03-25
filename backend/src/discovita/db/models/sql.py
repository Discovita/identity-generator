"""SQLAlchemy models for database tables."""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class State(Base):
    """SQLAlchemy model for state table."""
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False)
    session_id = Column(String(36), nullable=False)
    state_data = Column(JSON, nullable=False)  # Serialized CoachingState
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Context(Base):
    """SQLAlchemy model for context table."""
    __tablename__ = "contexts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), nullable=False)
    session_id = Column(String(36), nullable=False)
    messages = Column(JSON, nullable=False, default=list)
    user_data = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Identity(Base):
    """SQLAlchemy model for identity table."""
    __tablename__ = "identities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    """SQLAlchemy model for user table."""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    data = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    states = relationship("State", backref="user", cascade="all, delete-orphan")
    contexts = relationship("Context", backref="user", cascade="all, delete-orphan")
    identities = relationship("Identity", backref="user", cascade="all, delete-orphan")
