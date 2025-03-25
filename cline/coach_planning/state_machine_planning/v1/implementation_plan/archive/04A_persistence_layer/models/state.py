from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StateRecord(BaseModel):
    """Model for storing state information."""
    user_id: str = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    state: str = Field(..., description="Current state")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
