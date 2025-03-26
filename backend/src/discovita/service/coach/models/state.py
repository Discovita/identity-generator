"""State models for coaching service."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CoachingState(str, Enum):
    """Represents the possible states in the coaching process."""
    INTRODUCTION = "introduction"
    IDENTITY_BRAINSTORMING = "identity_brainstorming"
    IDENTITY_REFINEMENT = "identity_refinement"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive enum values."""
        if isinstance(value, str):
            # Try to match case-insensitively
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None

class Message(BaseModel):
    """A single message in the conversation history."""
    role: str = Field(..., description="Role of the message sender (user or coach)")
    content: str = Field(..., description="Content of the message")

class IdentityState(str, Enum):
    """Represents the possible states of an identity."""
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REFINEMENT_COMPLETE = "refinement_complete"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive enum values."""
        if isinstance(value, str):
            # Try to match case-insensitively
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None

class Identity(BaseModel):
    """Represents a single identity with its state."""
    id: str = Field(..., description="Unique identifier for the identity")
    description: str = Field(..., description="Description of the identity")
    state: IdentityState = Field(IdentityState.PROPOSED, description="Current state of the identity")
    notes: List[str] = Field(default_factory=list, description="Notes about the identity")

class UserProfile(BaseModel):
    """User information and goals."""
    name: str = Field(..., description="User's name")
    goals: List[str] = Field(default_factory=list, description="User's goals")

class CoachState(BaseModel):
    """
    Complete state of a coaching session.
    This object is passed with each request/response to maintain stateless operation.
    """
    current_state: CoachingState = Field(..., description="Current state of the coaching session")
    user_profile: UserProfile = Field(..., description="User's profile information")
    identities: List[Identity] = Field(default_factory=list, description="List of confirmed identities")
    proposed_identity: Optional[Identity] = Field(None, description="Currently proposed identity, cleared unless explicitly proposed by LLM")
    current_identity_index: Optional[int] = Field(None, description="Index of current identity being refined")
    conversation_history: List[Message] = Field(default_factory=list, description="History of conversation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
