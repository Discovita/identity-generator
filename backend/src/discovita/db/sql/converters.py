"""Conversion utilities for SQL database."""

from typing import Dict, Any, Type, List
from uuid import UUID
from enum import Enum
from pydantic import BaseModel

from discovita.db.models.state import StateRecord
from discovita.db.models.identity import IdentityRecord
from discovita.service.coach.models.state import CoachingState

def model_to_table_values(record: BaseModel) -> Dict[str, Any]:
    """Convert a model to a dictionary of values for a table."""
    values = {}
    for key, value in record.model_dump().items():
        if isinstance(value, UUID):
            values[key] = str(value)
        elif isinstance(value, Enum):
            # Handle any enum type
            values[key] = value.value
        else:
            values[key] = value
    return values

def table_to_model(model_type: Type[BaseModel], table_row) -> BaseModel:
    """Convert a table row to a model."""
    values = {}
    for column in table_row.__table__.columns:
        column_name = column.name
        value = getattr(table_row, column_name)
        
        # Get the expected field type from the model
        if hasattr(model_type, "__annotations__"):
            field_type = model_type.__annotations__.get(column_name)
            
            # Convert value based on field type
            if field_type is not None:
                # Handle UUID conversion
                if field_type is UUID and isinstance(value, str):
                    value = UUID(value)
                # Handle Enum conversion
                elif isinstance(value, str) and hasattr(field_type, "__mro__") and Enum in field_type.__mro__:
                    # Direct Enum subclass
                    value = field_type(value)
        
        values[column_name] = value
    
    return model_type(**values)

def get_primary_key_columns(table_class) -> List[str]:
    """Get the primary key column names for a table class."""
    return [column.name for column in table_class.__table__.primary_key.columns]
