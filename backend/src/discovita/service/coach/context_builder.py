"""Builds coaching conversation context."""

from typing import Optional
from .models import Message, CoachState
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

    def build_context(self, state: CoachState) -> str:
        """Build complete context string including system prompt and state."""
        messages = [Message(role="system", content=SYSTEM_PROMPT)]
        
        if self.sample_dialogue:
            messages.append(Message(
                role="system",
                content=f"Reference this sample dialogue style: {self.sample_dialogue}"
            ))
        
        # Add user profile context
        profile_context = (
            "Current user profile:\n"
            f"Name: {state.user_profile.name}\n"
            f"Goals: {', '.join(state.user_profile.goals)}"
        )
        messages.append(Message(role="system", content=profile_context))
        
        # Add current state context
        state_context = (
            "Current state:\n"
            f"Phase: {state.current_state.value}\n"
            f"Identities: {len(state.identities)} created\n"
            f"Current identity: {state.current_identity_index if state.current_identity_index is not None else 'None'}"
        )
        messages.append(Message(role="system", content=state_context))
        
        # Add conversation history
        messages.extend(state.conversation_history)
        
        return "\n".join(f"{msg.role}: {msg.content}" for msg in messages)
