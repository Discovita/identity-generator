"""Extended context builder with state-specific prompts."""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add the backend directory to the path
current_file = Path(__file__)
backend_dir = current_file.parents[2]  # Go up to backend directory
sys.path.insert(0, str(backend_dir))

from src.discovita.service.coach.context_builder import ContextBuilder
from src.discovita.service.coach.models import CoachingState


class ExtendedContextBuilder(ContextBuilder):
    """Extended context builder that adds support for state-specific prompts."""

    def __init__(self):
        """Initialize the extended context builder."""
        super().__init__()

    def get_introduction_prompt(self) -> str:
        """Get the introduction state prompt."""
        return self._load_state_prompt("introduction")

    def get_brainstorming_prompt(self) -> str:
        """Get the identity brainstorming state prompt."""
        return self._load_state_prompt("identity_brainstorming")

    def get_refinement_prompt(self) -> str:
        """Get the identity refinement state prompt."""
        return self._load_state_prompt("identity_refinement")

    def get_visualization_prompt(self) -> str:
        """Get the identity visualization state prompt."""
        return self._load_state_prompt("identity_visualization")

    def get_system_prompt_with_functions(
        self, current_state: CoachingState, state_info: Dict[str, Any]
    ) -> str:
        """Get the system prompt with instructions for using functions.

        Args:
            current_state: The current coaching state
            state_info: Additional state information for context

        Returns:
            System prompt with function usage instructions
        """
        # Get base prompt for current state
        state_prompt = self._load_state_prompt(current_state.value)

        # Add function information
        function_instructions = """
You have access to the following functions to update the coaching conversation state:

1. add_draft_identity - Add a new identity during brainstorming 
2. add_refined_identity - Add a confirmed identity during refinement
3. set_focus_identity - Set an identity as focus for visualization
4. mark_identity_visualized - Mark current focus identity as visualized
5. mark_introduction_completed - Complete introduction and move to brainstorming
6. transition_to_next_state - Force transition to a specific state
7. get_coaching_state - Get the current state and progress information

Use these functions to update the coaching state as the conversation progresses. For example:
- When the user expresses interest in a specific identity, use add_draft_identity
- When the user confirms they want to refine an identity, use add_refined_identity
- When you've completed visualizing an identity, use mark_identity_visualized

The system will automatically transition between states based on progress, but you can use 
these functions to ensure the state reflects the conversation accurately.
"""

        # Add state information
        state_information = f"""
Current coaching state: {current_state.value}
"""
        for key, value in state_info.items():
            if isinstance(value, (str, int, bool, float)):
                state_information += f"{key}: {value}\n"

        # Combine prompts
        return f"{state_prompt}\n\n{function_instructions}\n\n{state_information}"

    def _load_state_prompt(self, state_name: str) -> str:
        """Load a state-specific prompt.

        Args:
            state_name: The name of the state to load the prompt for

        Returns:
            The state-specific prompt or the default system prompt if not found
        """
        # Calculate the project root directory
        backend_dir = Path(__file__).parents[2]

        # Try to load from prompts/states directory
        file_path = (
            backend_dir
            / "src/discovita/service/coach/prompts/states"
            / f"{state_name}.md"
        )

        if file_path.exists():
            with open(file_path, "r") as f:
                return f.read()

        # Fall back to general system prompt if state-specific prompt is not found
        return self.get_system_prompt()
