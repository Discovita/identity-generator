"""Coaching service implementation."""

from typing import Dict, Any

from .models.state import CoachState, Message
from .models.action import ProcessMessageResult, Action
from .models.llm import CoachLLMResponse
from .prompt.manager import PromptManager
from .actions.definitions import get_available_actions
from .actions.handler import apply_actions
from ..openai.client.client import OpenAIClient
from ..openai.client.operations.responses.responses import ResponseInput, ResponseTools

class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(
        self,
        client: OpenAIClient,
        prompt_manager: PromptManager
    ):
        self.client = client
        self.prompt_manager = prompt_manager
    
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
        
        # Get the system prompt
        system_prompt = self.prompt_manager.get_prompt(state)
        
        if first_user_msg:
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
        
        # Get structured response from LLM
        response = await self.client.get_structured_response_with_responses(
            input_data=input_data,
            response_model=CoachLLMResponse
        )
        
        if not response.is_valid or not response.parsed:
            raise ValueError(f"Failed to parse LLM response: {response.error}")
            
        llm_response = response.parsed
        
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
            final_prompt=system_prompt
        )
