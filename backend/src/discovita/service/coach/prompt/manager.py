"""Prompt manager for coaching service."""

from typing import Dict, Optional, Set

from ..models import ActionType, CoachingState, CoachState, Message
from .loader import PromptLoader
from .models import IdentitySummary, PromptContext
from .templates import PromptTemplate


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

    def get_initial_message(self) -> Message:
        """
        Load the initial welcome message from the shared prompts directory.
        """
        initial_message_path = self.loader.prompts_dir / "shared" / "initial_message.md"
        initial_content = self.loader._read_markdown_file(initial_message_path)
        return Message(role="coach", content=initial_content)

    def _build_prompt_context(self, state: CoachState) -> PromptContext:
        """Build prompt context from coach state."""
        current_identity_desc = None
        if state.current_identity_id is not None:
            for identity in state.identities:
                if identity.id == state.current_identity_id:
                    current_identity_desc = identity.description
                    break

        # Format recent messages from conversation history
        recent_messages = []
        if state.conversation_history:
            # Take the last 5 messages or fewer if there aren't that many
            for entry in state.conversation_history[-5:]:
                if entry.role == "user":
                    recent_messages.append(f"User: {entry.content}")
                else:
                    recent_messages.append(f"Coach: {entry.content}")

        return PromptContext(
            user_name=state.user_profile.name,
            user_goals=state.user_profile.goals,
            num_identities=len(state.identities),
            current_identity_description=current_identity_desc,
            identities_summary=[
                IdentitySummary(id=i.id, description=i.description, state=i.state)
                for i in state.identities
            ],
            phase=state.current_state.value,
            recent_messages=recent_messages,
        )

    def get_prompt(self, state: CoachState) -> str:
        """Get a formatted prompt for the current state using the provided context."""
        if state.current_state not in self.templates:
            raise ValueError(f"No template found for state: {state.current_state}")

        template = self.templates[state.current_state]
        context = self._build_prompt_context(state)

        # Load shared prompt components
        action_instructions_path = (
            self.loader.prompts_dir / "shared" / "action_instructions.md"
        )
        system_context_path = self.loader.prompts_dir / "shared" / "system_context.md"

        action_instructions = self.loader._read_markdown_file(action_instructions_path)
        system_context = self.loader._read_markdown_file(system_context_path)

        # Format the template with the context
        formatted_prompt = template.template.format(
            user_name=context.user_name,
            user_goals=context.format_goals(),
            num_identities=context.num_identities,
            current_identity=context.current_identity_description or "None",
            current_focus=context.current_identity_description or "None",
            identities_summary=context.format_identities(),
            phase=context.phase,
            user_summary=context.user_summary(),
            recent_messages=context.format_recent_messages(),
            identities=context.format_identities(),
            identity_categories=context.format_identity_categories(),
        )

        # Format and add shared components at the beginning
        formatted_action_instructions = action_instructions.format(
            identity_categories=context.format_identity_categories()
        )

        # Combine all components
        formatted_prompt = (
            f"{formatted_action_instructions}\n\n{system_context}\n\n{formatted_prompt}"
        )

        # Add examples if available
        if template.examples:
            examples_text = "\n\n# Examples\n\n"
            for example in template.examples:
                description = (
                    f"## {example.description}\n\n" if example.description else ""
                )
                examples_text += (
                    f"{description}User: {example.user}\n\nCoach: {example.coach}\n\n"
                )
            formatted_prompt += examples_text

        # Add counter-examples if available
        if template.counter_examples:
            counter_examples_text = (
                "\n\n# Counter-Examples (Do Not Respond Like This)\n\n"
            )
            for example in template.counter_examples:
                description = (
                    f"## {example.description}\n\n" if example.description else ""
                )
                counter_examples_text += (
                    f"{description}User: {example.user}\n\nCoach: {example.coach}\n\n"
                )
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

    def add_initial_message_to_state(self, state: CoachState) -> CoachState:
        """
        Add the initial welcome message to a CoachState's conversation history.
        """
        initial_message = self.get_initial_message()

        updated_state = CoachState(
            current_state=state.current_state,
            user_profile=state.user_profile,
            identities=state.identities.copy() if state.identities else [],
            proposed_identity=state.proposed_identity,
            current_identity_id=state.current_identity_id,
            conversation_history=[initial_message] + (state.conversation_history or []),
            metadata=state.metadata.copy() if state.metadata else {},
        )

        return updated_state
