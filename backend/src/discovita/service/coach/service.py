"""Coaching service implementation."""

from ..openai.core import OpenAIService
from .actions.definitions import get_available_actions
from .actions.handler import apply_actions
from .models.action import ProcessMessageResult
from .models.llm import CoachLLMResponse
from .models.state import CoachState, Message
from .prompt.manager import PromptManager


class CoachService:
    """
    Service for handling coaching interactions.

    This service processes user messages, generates coach responses using OpenAI,
    and applies any actions returned by the LLM to update the coaching state.
    """

    def __init__(self, open_ai_service: OpenAIService, prompt_manager: PromptManager):
        self.open_ai_service = open_ai_service
        self.prompt_manager = prompt_manager

    async def process_message(
        self, message: str, state: CoachState
    ) -> ProcessMessageResult:
        """Process a user message and update the coaching state."""
        if not state.conversation_history:
            state = self.prompt_manager.add_initial_message_to_state(state)
        state.conversation_history.append(Message(role="user", content=message))
        system_prompt = self.prompt_manager.get_prompt(state)
        formatted_messages = self.open_ai_service.create_messages(
            system_message=system_prompt, messages=state.conversation_history
        )

        response = self.open_ai_service.create_structured_chat_completion(
            model="gpt-4o-2024-08-06",
            messages=formatted_messages,
            response_format=CoachLLMResponse,
        )

        if not response or not hasattr(response.choices[0].message, "parsed"):
            raise ValueError(f"Failed to parse LLM response")

        llm_response = response.choices[0].message.parsed

        # Apply actions
        new_state = apply_actions(state, llm_response.actions)

        # Add coach response to history
        new_state.conversation_history.append(
            Message(role="coach", content=llm_response.message)
        )

        # Construct final result with updated state
        return ProcessMessageResult(
            message=llm_response.message,
            state=new_state,
            actions=llm_response.actions,
            final_prompt=system_prompt,
        )
