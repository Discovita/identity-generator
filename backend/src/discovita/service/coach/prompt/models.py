"""Models for prompt management."""

from typing import Optional
from pydantic import BaseModel

class PromptContext(BaseModel):
    """Context data used to format prompt templates."""
    user_name: str
    user_goals: list[str]
    num_identities: int
    current_identity_description: Optional[str] = None
    identities_summary: list[tuple[str, bool]]  # List of (description, is_accepted) tuples
    phase: str

    def format_goals(self) -> str:
        """Format goals as comma-separated string."""
        return ", ".join(self.user_goals)

    def format_identities(self) -> str:
        """Format identities summary as bulleted list."""
        return "\n".join(
            f"- {desc} ({'accepted' if accepted else 'not accepted'})"
            for desc, accepted in self.identities_summary
        )
