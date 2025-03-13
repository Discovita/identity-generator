from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class ContextRecord(BaseModel):
    """Model for storing conversation context."""
    user_id: str = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Conversation messages")
    user_data: Dict[str, Any] = Field(default_factory=dict, description="User-specific data")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
