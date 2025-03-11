"""Builds coaching conversation context."""

from typing import List, Optional
from .models import ChatMessage, UserProfile
from .prompts import SYSTEM_PROMPT, load_sample_dialogue

class ContextBuilder:
    """Builds and formats conversation context."""

    def __init__(self):
        self.sample_dialogue = load_sample_dialogue()

    def get_system_prompt(self) -> str:
        """Get the system prompt."""
        return SYSTEM_PROMPT
    
    def get_sample_dialogue(self) -> str:
        """Get the sample dialogue."""
        return self.sample_dialogue

    def build_context(
        self,
        context: List[ChatMessage],
        profile: Optional[UserProfile]
    ) -> str:
        """Build complete context string including system prompt and profile."""
        messages = [ChatMessage(role="system", content=SYSTEM_PROMPT)]
        
        if self.sample_dialogue:
            messages.append(ChatMessage(
                role="system",
                content=f"Reference this sample dialogue style: {self.sample_dialogue}"
            ))
        
        if profile:
            identities_str = "\n".join(
                f"- {i.category.name}: {i.name}" for i in profile.identities
            )
            profile_context = (
                "Current user profile:\n"
                f"Identities:\n{identities_str}\n"
                f"Current focus: {profile.current_focus.name if profile.current_focus else 'None'}"
            )
            messages.append(ChatMessage(role="system", content=profile_context))
        
        messages.extend(context)
        return "\n".join(f"{msg.role}: {msg.content}" for msg in messages)
