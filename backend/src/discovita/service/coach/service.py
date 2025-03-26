"""Coaching service implementation."""

from typing import Dict, Any

from .models.state import CoachState, Message
from .models.action import ProcessMessageResult, Action
from .models.llm import CoachLLMResponse
from .prompt.manager import PromptManager
from .state.machine import StateMachine
from .actions.definitions import get_available_actions
from .actions.handler import apply_actions
from ..openai.client.client import OpenAIClient
from ..openai.client.operations.responses.responses import ResponseInput, ResponseTools

class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(
        self,
        client: OpenAIClient,
        prompt_manager: PromptManager,
        state_machine: StateMachine
    ):
        self.client = client
        self.prompt_manager = prompt_manager
        self.state_machine = state_machine
    
    async def process_message(
        self, 
        message: str, 
        state: CoachState
    ) -> ProcessMessageResult:
        """Process a user message and update the coaching state."""
        # Add user message to history
        state.conversation_history.append(
            Message(role="user", content=message)
        )
        
        # Get LLM response
        # Convert conversation history to messages with correct roles
        messages = []
        
        # For the first message, combine system prompt with user message
        first_user_msg = next(
            (msg for msg in state.conversation_history if msg.role == "user"),
            None
        )
        if first_user_msg:
            system_prompt = self.prompt_manager.get_prompt(state)
            combined_content = f"{system_prompt}\n\nUser message: {first_user_msg.content}"
            messages.append({"role": "user", "content": combined_content})
            
            # Add remaining messages
            remaining = False
            for msg in state.conversation_history:
                if msg == first_user_msg:
                    remaining = True
                    continue
                if remaining:
                    role = "assistant" if msg.role == "coach" else msg.role
                    messages.append({"role": role, "content": msg.content})
        
        # Get structured completion
        input_data = ResponseInput.from_dict_list(messages)
        
        # Get LLM response with function definitions
        tools = ResponseTools(
            tools=get_available_actions(),
            tool_choice=None  # Allow model to choose when to use tools
        )
        
        response = await self.client.get_structured_response_with_responses(
            input_data=input_data,
            response_model=CoachLLMResponse,
            tools=tools
        )
        
        if not response.is_valid or not response.parsed:
            raise ValueError(f"Failed to parse LLM response: {response.error}")
            
        llm_response = response.parsed
        
        # Apply actions and check transitions
        new_state = apply_actions(state, llm_response.actions)
        new_state = self.state_machine.check_transitions(new_state)
        
        # Add coach response to history
        new_state.conversation_history.append(
            Message(role="coach", content=llm_response.message)
        )
        
        # Construct final result with updated state
        return ProcessMessageResult(
            message=llm_response.message,
            state=new_state,
            actions=llm_response.actions
        )
