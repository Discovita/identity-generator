"""Prompt manager for coaching service."""

from typing import Dict, Set, Optional
from pathlib import Path

from ..models import CoachState, CoachingState, ActionType
from .models import PromptContext
from .templates import PromptTemplate
from .loader import PromptLoader

class PromptManager:
    """Manages prompt templates and generates prompts for the coaching system."""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the prompt manager."""
        self.loader = PromptLoader(prompts_dir)
        self.templates: Dict[CoachingState, PromptTemplate] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all prompt templates."""
        for state in CoachingState:
            self.templates[state] = self.loader.load_template(state)
    
    def _build_prompt_context(self, state: CoachState) -> PromptContext:
        """Build prompt context from coach state."""
        current_identity_desc = None
        if (state.current_identity_index is not None 
            and state.current_identity_index < len(state.identities)):
            current_identity_desc = state.identities[state.current_identity_index].description
            
        return PromptContext(
            user_name=state.user_profile.name,
            user_goals=state.user_profile.goals,
            num_identities=len(state.identities),
            current_identity_description=current_identity_desc,
            identities_summary=[
                (i.description, i.is_accepted) for i in state.identities
            ],
            phase=state.current_state.value
        )
    
    def get_prompt(self, state: CoachState) -> str:
        """Get a formatted prompt for the current state using the provided context."""
        if state.current_state not in self.templates:
            raise ValueError(f"No template found for state: {state.current_state}")
            
        template = self.templates[state.current_state]
        context = self._build_prompt_context(state)
        
        # Format the template with the context
        formatted_prompt = template.template.format(
            user_name=context.user_name,
            user_goals=context.format_goals(),
            num_identities=context.num_identities,
            current_identity=context.current_identity_description or "None",
            identities_summary=context.format_identities(),
            phase=context.phase
        )
        
        # Add examples if available
        if template.examples:
            examples_text = "\n\n# Examples\n\n"
            for example in template.examples:
                description = f"## {example.description}\n\n" if example.description else ""
                examples_text += f"{description}User: {example.user}\n\nCoach: {example.coach}\n\n"
            formatted_prompt += examples_text
        
        # Add counter-examples if available
        if template.counter_examples:
            counter_examples_text = "\n\n# Counter-Examples (Do Not Respond Like This)\n\n"
            for example in template.counter_examples:
                description = f"## {example.description}\n\n" if example.description else ""
                counter_examples_text += f"{description}User: {example.user}\n\nCoach: {example.coach}\n\n"
            formatted_prompt += counter_examples_text
        
        return formatted_prompt
    
    def get_allowed_actions(self, state: CoachingState) -> Set[ActionType]:
        """Get the set of allowed actions for the current state."""
        if state not in self.templates:
            return set()
        return self.templates[state].allowed_actions
    
    def reload_templates(self) -> None:
        """Reload all templates from disk."""
        self._load_templates()
