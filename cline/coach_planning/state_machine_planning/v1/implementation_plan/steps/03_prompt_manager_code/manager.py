from typing import Dict, Any, List, Set, Optional
import os
from pathlib import Path

from discovita.service.coach.models import CoachingState, ActionType, CoachContext
from .templates import PromptTemplate
from .loader import PromptLoader

class PromptManager:
    """Manages prompt templates and generates prompts for the coaching system."""
    
    def __init__(self, prompts_dir: str = None):
        """Initialize the prompt manager."""
        self.loader = PromptLoader(prompts_dir)
        self.templates: Dict[CoachingState, PromptTemplate] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all prompt templates."""
        for state in CoachingState:
            self.templates[state] = self.loader.load_template(state)
    
    def get_prompt(self, state: CoachingState, context: CoachContext) -> Optional[str]:
        """Get a formatted prompt for the current state using the provided context."""
        if state not in self.templates:
            return None
            
        template = self.templates[state]
        
        # Ensure all required context keys are present
        prompt_context = context.get_prompt_context()
        missing_keys = [key for key in template.required_context_keys if key not in prompt_context]
        if missing_keys:
            raise ValueError(f"Missing required context keys: {missing_keys}")
        
        # Format the template with the context
        formatted_prompt = template.template.format(**prompt_context)
        
        # Add examples if available
        if template.examples:
            examples_text = "\n\n# Examples\n\n"
            for example in template.examples:
                examples_text += f"User: {example.user}\n\nCoach: {example.coach}\n\n"
            formatted_prompt += examples_text
        
        # Add counter-examples if available
        if template.counter_examples:
            counter_examples_text = "\n\n# Counter-Examples (Do Not Respond Like This)\n\n"
            for example in template.counter_examples:
                counter_examples_text += f"User: {example.user}\n\nCoach: {example.coach}\n\n"
            formatted_prompt += counter_examples_text
        
        return formatted_prompt
    
    def get_allowed_actions(self, state: CoachingState) -> List[ActionType]:
        """Get the list of allowed actions for the current state."""
        if state not in self.templates:
            return []
        return list(self.templates[state].allowed_actions)
    
    def reload_templates(self) -> None:
        """Reload all templates from disk."""
        self._load_templates()
