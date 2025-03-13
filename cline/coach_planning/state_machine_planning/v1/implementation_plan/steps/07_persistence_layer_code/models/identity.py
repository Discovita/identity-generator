from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class IdentityRecord(BaseModel):
    """Model for storing identity information."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    user_id: str = Field(..., description="User ID")
    name: str = Field(..., description="Identity name")
    category: str = Field(..., description="Identity category")
    description: str = Field("", description="Identity description")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
