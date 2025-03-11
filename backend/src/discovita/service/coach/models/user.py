"""User profile models for coaching service."""

from typing import List, Optional
from pydantic import BaseModel, Field

from .identity import Identity, IdentityCategory

class UserProfile(BaseModel):
    """User profile tracking identities and coaching progress."""
    user_id: str = Field(..., description="Unique identifier for the user")
    identities: List[Identity] = Field(default_factory=list, description="User's chosen identities")
    current_focus: Optional[IdentityCategory] = Field(None, description="Current identity category focus")
