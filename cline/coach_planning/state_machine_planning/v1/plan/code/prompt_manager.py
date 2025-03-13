from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    template: str
    required_context_keys: List[str]
    examples: List[Dict[str, Any]]
    counter_examples: List[Dict[str, Any]]
    allowed_actions: List[str]

class PromptManager:
    def __init__(self):
        self.templates: Dict[CoachingState, PromptTemplate] = {}
        self._setup_templates()
    
    def _setup_templates(self) -> None:
        """Initialize prompt templates for each state."""
        self.templates[CoachingState.INTRODUCTION] = PromptTemplate(
            template="""
            You are Leigh Ann, a professional life coach. Your goal is to introduce the client to your coaching process.
            Explain how you'll help them identify their core identities (such as "visionary entrepreneur" or "father and husband").
            Ask if they have any questions before proceeding to the identity brainstorming phase.
            
            Current user information: {user_summary}
            Recent conversation: {recent_messages}
            """,
            required_context_keys=["user_summary", "recent_messages"],
            examples=[{"user": "Hi, I'm new here", "coach": "Welcome! I'm Leigh Ann, your personal life coach..."}],
            counter_examples=[{"user": "Hi", "coach": "Let's jump straight into identifying your core values"}],
            allowed_actions=["SAVE_USER_INFO", "MARK_INTRODUCTION_COMPLETE", "TRANSITION_STATE"]
        )
        
        self.templates[CoachingState.IDENTITY_BRAINSTORMING] = PromptTemplate(
            template="""
            You are Leigh Ann, helping your client brainstorm their core identities.
            Guide them to reflect on different roles and aspects of themselves that feel meaningful and empowering.
            Look for patterns and help them articulate these identities clearly.
            Each identity should feel authentic and inspiring to them.
            
            Current user information: {user_summary}
            Identities discussed so far: {draft_identities}
            Recent conversation: {recent_messages}
            """,
            required_context_keys=["user_summary", "draft_identities", "recent_messages"],
            examples=[{"user": "I think I see myself as a leader", "coach": "That's interesting! Tell me more about how you see yourself as a leader. What kind of leader are you?"}],
            counter_examples=[{"user": "I think I see myself as a leader", "coach": "Great, let's move on to the next exercise"}],
            allowed_actions=["SAVE_IDENTITY", "SAVE_USER_INFO", "TRANSITION_STATE"]
        )
        
        # Add more templates for other states
    
    def get_prompt(self, state: CoachingState, context: Dict[str, Any]) -> Optional[str]:
        """Get a formatted prompt for the current state using the provided context."""
        if state not in self.templates:
            return None
            
        template = self.templates[state]
        
        # Ensure all required context keys are present
        missing_keys = [key for key in template.required_context_keys if key not in context]
        if missing_keys:
            raise ValueError(f"Missing required context keys: {missing_keys}")
            
        # Format the template with the context
        return template.template.format(**context)
        
    def get_allowed_actions(self, state: CoachingState) -> List[str]:
        """Get the list of allowed actions for the current state."""
        if state not in self.templates:
            return []
        return self.templates[state].allowed_actions

