"""Data models for coaching service."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import Field, BaseModel
from discovita.service.openai.models.llm_response import LLMResponseModel

class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")

class IdentityCategory(str, Enum):
    """Categories of identity in the coaching system."""
    PASSIONS = "passions_and_talents"
    MONEY_MAKER = "maker_of_money" 
    MONEY_KEEPER = "keeper_of_money"
    SPIRITUAL = "spiritual"
    APPEARANCE = "personal_appearance"
    HEALTH = "physical_expression"
    FAMILY = "familial_relations"
    ROMANTIC = "romantic_relation"
    ACTION = "doer_of_things"

class Identity(BaseModel):
    """Identity model representing a client's chosen identity."""
    category: IdentityCategory = Field(..., description="Category this identity belongs to")
    name: str = Field(..., description="Name of the identity (e.g. 'Creative Visionary')")
    affirmation: str = Field(..., description="'I am' statement and description")
    visualization: Optional[Dict] = Field(None, description="Visual representation details")

class UserProfile(BaseModel):
    """User profile tracking identities and coaching progress."""
    user_id: str = Field(..., description="Unique identifier for the user")
    identities: List[Identity] = Field(default_factory=list, description="User's chosen identities")
    current_focus: Optional[IdentityCategory] = Field(None, description="Current identity category focus")

class CoachRequest(BaseModel):
    """Request model for coach API."""
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="User's message")
    context: List[ChatMessage] = Field(default_factory=list, description="Previous chat context")
    profile: Optional[UserProfile] = Field(None, description="User's identity profile")

class CoachResponse(LLMResponseModel):
    """Response model for coach API."""
    message: str = Field(..., description="Coach's response message")
    suggested_identities: Optional[List[Identity]] = Field(None, description="Suggested new identities")
    visualization_prompt: Optional[Dict] = Field(None, description="Prompt for identity visualization")
