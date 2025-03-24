"""Test enum serialization and deserialization in the database."""

import pytest
import pytest_asyncio
from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from discovita.db.sql.database import SQLDatabase
from discovita.db.in_memory_db import InMemoryDatabase

# Define a test enum
class TestEnum(Enum):
    """Test enum for database serialization tests."""
    VALUE_ONE = "value_one"
    VALUE_TWO = "value_two"
    VALUE_THREE = "value_three"

# Define a test model with an enum field
class TestEnumRecord(BaseModel):
    """Test model with an enum field."""
    id: str = Field(..., description="Record ID")
    enum_field: TestEnum = Field(..., description="Enum field")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

# Add the model to the database model mappings
@pytest_asyncio.fixture
async def sql_db():
    """Create a SQL database for testing."""
    db = SQLDatabase("sqlite+aiosqlite:///:memory:")
    
    # Add TestEnumRecord to model_to_table mapping
    from discovita.db.sql.models import Base
    from sqlalchemy import Column, String, DateTime
    from sqlalchemy.sql import func
    
    # Define a table for TestEnumRecord
    class TestEnumTable(Base):
        """SQLAlchemy model for test enum records."""
        __tablename__ = "test_enums"
        
        id = Column(String, primary_key=True)
        enum_field = Column(String, nullable=False)
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Add the mapping
    db.model_to_table[TestEnumRecord] = TestEnumTable
    
    await db.initialize()
    yield db

@pytest_asyncio.fixture
def in_memory_db():
    """Create an in-memory database for testing."""
    return InMemoryDatabase()

@pytest.mark.asyncio
async def test_enum_sql_save_and_load(sql_db):
    """Test saving and loading a record with an enum field in SQL database."""
    # Create a record with an enum field
    record = TestEnumRecord(
        id="test1",
        enum_field=TestEnum.VALUE_TWO
    )
    
    # Save the record
    saved_record = await sql_db.save(record)
    
    # Verify the saved record
    assert saved_record.id == "test1"
    assert saved_record.enum_field == TestEnum.VALUE_TWO
    
    # Load the record
    loaded_record = await sql_db.get(TestEnumRecord, id="test1")
    
    # Verify the loaded record
    assert loaded_record is not None
    assert loaded_record.id == "test1"
    assert loaded_record.enum_field == TestEnum.VALUE_TWO
    assert isinstance(loaded_record.enum_field, TestEnum)
    
    # Update the record with a different enum value
    await sql_db.update(
        TestEnumRecord,
        keys={"id": "test1"},
        values={"enum_field": TestEnum.VALUE_THREE}
    )
    
    # Load the updated record
    updated_record = await sql_db.get(TestEnumRecord, id="test1")
    
    # Verify the updated record
    assert updated_record is not None
    assert updated_record.enum_field == TestEnum.VALUE_THREE
    assert isinstance(updated_record.enum_field, TestEnum)

@pytest.mark.asyncio
async def test_enum_in_memory_save_and_load(in_memory_db):
    """Test saving and loading a record with an enum field in in-memory database."""
    # Create a record with an enum field
    record = TestEnumRecord(
        id="test1",
        enum_field=TestEnum.VALUE_ONE
    )
    
    # Save the record
    await in_memory_db.save(record)
    
    # Load the record
    loaded_record = await in_memory_db.get(TestEnumRecord, id="test1")
    
    # Verify the loaded record
    assert loaded_record is not None
    assert loaded_record.id == "test1"
    assert loaded_record.enum_field == TestEnum.VALUE_ONE
    assert isinstance(loaded_record.enum_field, TestEnum)
    
    # Update the record with a different enum value
    await in_memory_db.update(
        TestEnumRecord,
        keys={"id": "test1"},
        values={"enum_field": TestEnum.VALUE_THREE}
    )
    
    # Load the updated record
    updated_record = await in_memory_db.get(TestEnumRecord, id="test1")
    
    # Verify the updated record
    assert updated_record is not None
    assert updated_record.enum_field == TestEnum.VALUE_THREE
    assert isinstance(updated_record.enum_field, TestEnum)
