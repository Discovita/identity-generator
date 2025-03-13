from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class UserRecord(BaseModel):
    """Model for storing user information."""
    id: str = Field(..., description="User ID")
    data: Dict[str, Any] = Field(default_factory=dict, description="User data")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
