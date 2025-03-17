"""Context models for coaching service."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from .chat import ChatMessage
from .user import UserProfile
from .state import CoachingState

class CoachContext(BaseModel):
    """Context for the coaching process."""
    user_id: str = Field(..., description="Unique identifier for the user")
    current_state: CoachingState = Field(
        default=CoachingState.INTRODUCTION, 
        description="Current state in the coaching process"
    )
    conversation_history: List[ChatMessage] = Field(
        default_factory=list, 
        description="Recent conversation history"
    )
    consolidated_summary: str = Field(
        "", 
        description="Summary of older conversation history"
    )
    user_profile: Optional[UserProfile] = Field(
        None, 
        description="User's profile information"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata for the coaching process"
    )
    
    def get_prompt_context(self) -> Dict[str, Any]:
        """Get context formatted for prompt templates."""
        # Format the conversation history
        recent_messages = "\n\n".join(
            f"{msg.role.capitalize()}: {msg.content}" 
            for msg in self.conversation_history
        )
        
        # Format identities if available
        identities_str = ""
        if self.user_profile and self.user_profile.identities:
            identities_str = "\n".join(
                f"- {i.category.name}: {i.name}" 
                for i in self.user_profile.identities
            )
        
        # Format current focus if available
        current_focus = "None"
        if self.user_profile and self.user_profile.current_focus:
            current_focus = self.user_profile.current_focus.name
        
        return {
            "user_summary": self.consolidated_summary,
            "recent_messages": recent_messages,
            "identities": identities_str,
            "current_focus": current_focus,
            "state": self.current_state.value,
            **self.metadata  # Include any additional metadata
        }
