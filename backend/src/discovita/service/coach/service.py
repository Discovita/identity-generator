"""Coaching service implementation."""

from typing import Dict, Any

from .models.state import CoachState, Message
from .models.action import ProcessMessageResult
from .prompt.manager import PromptManager
from .state.machine import StateMachine
from .actions.definitions import get_available_actions
from .actions.handler import apply_actions
from ..openai.client.client import OpenAIClient
from ..openai.client.operations.responses.responses import ResponseInput

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
        # Start with system prompt
        messages = [{"role": "system", "content": self.prompt_manager.get_prompt(state)}]
        
        # Add conversation history with correct roles
        for msg in state.conversation_history:
            role = "assistant" if msg.role == "coach" else msg.role
            messages.append({"role": role, "content": msg.content})
        
        # Get structured completion
        input_data = ResponseInput.from_dict_list(messages)
        
        response = await self.client.get_structured_response_with_responses(
            messages=messages,
            available_functions=get_available_actions(),
            response_model=ProcessMessageResult,
            input_data=input_data
        )
        
        if not response.is_valid or not response.parsed:
            raise ValueError(f"Failed to parse LLM response: {response.error}")
            
        result = response.parsed
        
        # Apply actions and check transitions
        new_state = apply_actions(state, result.actions)
        new_state = self.state_machine.check_transitions(new_state)
        
        # Add coach response to history
        new_state.conversation_history.append(
            Message(role="coach", content=result.message)
        )
        
        return ProcessMessageResult(
            message=result.message,
            state=new_state,
            actions=result.actions
        )
