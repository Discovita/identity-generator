"""SQL database operations."""

from typing import Dict, Any, List, Optional, Type, Tuple
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from discovita.db.sql.converters import model_to_table_values, table_to_model, get_primary_key_columns

async def get_record(
    session: AsyncSession,
    model_type: Type[BaseModel],
    table_class,
    **keys
) -> Optional[BaseModel]:
    """Get a record by its keys."""
    # Build the query
    query = select(table_class)
    for key, value in keys.items():
        if isinstance(value, UUID):
            value = str(value)
        query = query.where(getattr(table_class, key) == value)
    
    # Execute the query
    result = await session.execute(query)
    row = result.scalar_one_or_none()
    
    if row:
        return table_to_model(model_type, row)
    return None

async def get_all_records(
    session: AsyncSession,
    model_type: Type[BaseModel],
    table_class,
    **filters
) -> List[BaseModel]:
    """Get all records matching the filters."""
    # Build the query
    query = select(table_class)
    for key, value in filters.items():
        if isinstance(value, UUID):
            value = str(value)
        query = query.where(getattr(table_class, key) == value)
    
    # Execute the query
    result = await session.execute(query)
    rows = result.scalars().all()
    
    return [table_to_model(model_type, row) for row in rows]

async def save_record(
    session: AsyncSession,
    record: BaseModel,
    table_class
) -> BaseModel:
    """Save a record."""
    # Set timestamps if the model has them
    now = datetime.now()
    if hasattr(record, "created_at") and not getattr(record, "created_at"):
        setattr(record, "created_at", now)
    if hasattr(record, "updated_at"):
        setattr(record, "updated_at", now)
    
    # Convert model to table values
    values = model_to_table_values(record)
    
    # Get primary key columns
    pk_columns = get_primary_key_columns(table_class)
    
    # Build the primary key filter
    pk_filter = {}
    for column in pk_columns:
        pk_filter[column] = values[column]
    
    # Check if record exists
    query = select(table_class)
    for key, value in pk_filter.items():
        query = query.where(getattr(table_class, key) == value)
    
    result = await session.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing record
        stmt = update(table_class).where(
            *[getattr(table_class, key) == value for key, value in pk_filter.items()]
        ).values(**values)
        await session.execute(stmt)
    else:
        # Insert new record
        stmt = insert(table_class).values(**values)
        await session.execute(stmt)
    
    return record

async def delete_record(
    session: AsyncSession,
    table_class,
    **keys
) -> None:
    """Delete a record by its keys."""
    # Build the query
    stmt = delete(table_class)
    for key, value in keys.items():
        if isinstance(value, UUID):
            value = str(value)
        stmt = stmt.where(getattr(table_class, key) == value)
    
    # Execute the query
    await session.execute(stmt)

async def update_record(
    session: AsyncSession,
    table_class,
    keys: Dict[str, Any],
    values: Dict[str, Any]
) -> None:
    """Update specific fields in a record."""
    # Convert UUID values to strings
    for key, value in keys.items():
        if isinstance(value, UUID):
            keys[key] = str(value)
    
    # Process values for update
    processed_values = {}
    for key, value in values.items():
        if isinstance(value, UUID):
            processed_values[key] = str(value)
        elif isinstance(value, Enum):
            # Handle any enum type
            processed_values[key] = value.value
        else:
            processed_values[key] = value
    
    # Build the query
    stmt = update(table_class)
    for key, value in keys.items():
        stmt = stmt.where(getattr(table_class, key) == value)
    
    # Add updated_at timestamp if the model has it
    if hasattr(table_class, "updated_at"):
        processed_values["updated_at"] = datetime.now()
    
    # Execute the query
    stmt = stmt.values(**processed_values)
    await session.execute(stmt)
