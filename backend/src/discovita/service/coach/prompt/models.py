"""Models for prompt management."""

from typing import Optional, List
from pydantic import BaseModel, Field
from ..models.state import IdentityState
from ..models.identity import IdentityCategory

class IdentitySummary(BaseModel):
    """Summary of an identity for prompt context."""
    id: str = Field(..., description="Unique identifier for the identity")
    description: str = Field(..., description="Description of the identity")
    state: IdentityState = Field(..., description="Current state of the identity")

class PromptContext(BaseModel):
    """Context data used to format prompt templates."""
    user_name: str
    user_goals: list[str]
    num_identities: int
    current_identity_description: Optional[str] = None
    identities_summary: list[IdentitySummary] = Field(default_factory=list, description="List of identity summaries")
    phase: str
    recent_messages: List[str] = []  # Recent conversation messages

    def format_goals(self) -> str:
        """Format goals as comma-separated string."""
        return ", ".join(self.user_goals)

    def format_identities(self) -> str:
        """Format identities summary as bulleted list with IDs."""
        if not self.identities_summary:
            return "No identities created yet."
            
        return "\n".join(
            f"- ID: {identity.id} | {identity.description} (state: {identity.state.value})"
            for identity in self.identities_summary
        )
        
    def user_summary(self) -> str:
        """Generate a summary of the user information."""
        return f"Name: {self.user_name}\nGoals: {self.format_goals()}"
        
    def format_recent_messages(self) -> str:
        """Format recent messages as a conversation."""
        if not self.recent_messages:
            return "No recent messages."
        return "\n".join(self.recent_messages)
        
    def format_identity_categories(self) -> str:
        """Format identity categories as a list of enum values."""
        return ", ".join([f"'{category.value}'" for category in IdentityCategory])
