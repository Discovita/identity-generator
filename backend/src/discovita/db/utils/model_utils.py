"""Utilities for working with database models."""

from typing import Dict, Any, Tuple, Type, Optional
from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from discovita.db.models.state import StateRecord
from discovita.db.models.context import ContextRecord
from discovita.db.models.identity import IdentityRecord
from discovita.db.models.user import UserRecord

def get_primary_key_for_model(model_type: Type[BaseModel], **keys) -> Optional[Tuple]:
    """Get the primary key tuple for a model type."""
    if model_type == StateRecord or model_type == ContextRecord:
        return (keys["user_id"], keys["session_id"])
    elif model_type == IdentityRecord:
        if "id" in keys:
            return (keys["user_id"], keys["id"])
        else:
            return None  # Can't get a specific identity without an ID
    elif model_type == UserRecord:
        return (keys["id"],)
    elif hasattr(model_type, "__annotations__") and "id" in model_type.__annotations__:
        # Generic handling for models with an 'id' field as primary key
        return (keys["id"],)
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_primary_key_dict_from_record(record: BaseModel) -> Dict[str, Any]:
    """Extract primary key fields from a record."""
    model_type = type(record)
    
    if model_type == StateRecord or model_type == ContextRecord:
        return {"user_id": record.user_id, "session_id": record.session_id}
    elif model_type == IdentityRecord:
        return {"user_id": record.user_id, "id": record.id}
    elif model_type == UserRecord:
        return {"id": record.id}
    elif hasattr(record, "id"):
        # Generic handling for models with an 'id' field
        return {"id": record.id}
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def update_timestamps(record: BaseModel) -> None:
    """Update timestamps on a record."""
    now = datetime.now()
    if hasattr(record, "created_at") and not getattr(record, "created_at"):
        setattr(record, "created_at", now)
    if hasattr(record, "updated_at"):
        setattr(record, "updated_at", now)

def convert_value_for_storage(value: Any) -> Any:
    """Convert a value to a format suitable for storage."""
    if isinstance(value, UUID):
        return str(value)
    elif isinstance(value, Enum):
        return value.value
    else:
        return value

def convert_dict_for_storage(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a dictionary of values to a format suitable for storage."""
    return {key: convert_value_for_storage(value) for key, value in data.items()}
