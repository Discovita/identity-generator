from typing import Dict, List, Optional, Any
from uuid import uuid4

from .models.request_response import CoachStateRequest, CoachStateResponse, StateInfoResponse
from .models.state import CoachingState
from .models.context import CoachContext
from .state.machine import CoachStateMachine
from .prompt.manager import PromptManager
from .context.manager import ContextManager
from .action.executor import ActionExecutor
from ..openai.client.client import OpenAIClient

class CoachService:
    """Service for handling coaching interactions with state machine architecture."""
    
    def __init__(
        self,
        client: OpenAIClient,
        state_machine: CoachStateMachine,
        prompt_manager: PromptManager,
        context_manager: ContextManager,
        action_executor: ActionExecutor
    ):
        self.client = client
        self.state_machine = state_machine
        self.prompt_manager = prompt_manager
        self.context_manager = context_manager
        self.action_executor = action_executor
    
    async def process_message(
        self,
        request: CoachStateRequest
    ) -> CoachStateResponse:
        """Process a user message with state management."""
        # Get or create session
        session_id = request.session_id or str(uuid4())
        
        # Get current state and context
        state = await self.state_machine.get_current_state(request.user_id, session_id)
        context = await self.context_manager.get_context(request.user_id, session_id)
        
        # Add the new message to context
        await self.context_manager.add_message(
            user_id=request.user_id,
            session_id=session_id,
            role="user",
            content=request.message
        )
        
        # Get prompt for current state
        prompt = self.prompt_manager.get_prompt_for_state(
            state=state,
            context=context
        )
        
        # Get LLM response
        llm_response = await self.client.get_completion(prompt)
        
        # Parse actions from response
        actions = self.action_executor.parse_actions_from_response(llm_response)
        
        # Execute actions
        action_results = await self.action_executor.execute_actions(
            actions=actions,
            user_id=request.user_id,
            session_id=session_id,
            state=state
        )
        
        # Add assistant message to context
        await self.context_manager.add_message(
            user_id=request.user_id,
            session_id=session_id,
            role="assistant",
            content=llm_response
        )
        
        # Get updated state after action execution
        updated_state = await self.state_machine.get_current_state(request.user_id, session_id)
        
        # Extract identity information (if any)
        proposed_identity = context.proposed_identity
        confirmed_identity = context.confirmed_identity
        
        # Get available actions for current state
        available_actions = self.state_machine.get_available_actions(updated_state)
        
        # Create response
        return CoachStateResponse(
            message=llm_response,
            current_state=updated_state.value,
            proposed_identity=proposed_identity,
            confirmed_identity=confirmed_identity,
            visualization_prompt=context.visualization_prompt,
            available_actions=[action.name for action in available_actions],
            session_id=session_id
        )
    
    async def get_state_info(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> StateInfoResponse:
        """Get information about the current state."""
        # Get current state
        state = await self.state_machine.get_current_state(user_id, session_id)
        
        # Get state description
        description = self.state_machine.get_state_description(state)
        
        # Get available actions
        available_actions = self.state_machine.get_available_actions(state)
        
        # Get possible next states
        next_states = self.state_machine.get_possible_next_states(state)
        
        return StateInfoResponse(
            current_state=state.value,
            description=description,
            available_actions=[action.name for action in available_actions],
            next_possible_states=[state.value for state in next_states]
        )
    
    async def create_new_session(
        self,
        user_id: str
    ) -> StateInfoResponse:
        """Create a new coaching session."""
        # Generate new session ID
        session_id = str(uuid4())
        
        # Initialize state machine with initial state
        await self.state_machine.initialize_session(user_id, session_id)
        
        # Initialize context
        await self.context_manager.initialize_context(user_id, session_id)
        
        # Return state info
        return await self.get_state_info(user_id, session_id)
    
    async def reset_session(
        self,
        session_id: str
    ) -> StateInfoResponse:
        """Reset a coaching session to initial state."""
        # Get user ID from session
        user_id = await self.context_manager.get_user_id_for_session(session_id)
        
        # Reset state machine
        await self.state_machine.reset_session(user_id, session_id)
        
        # Reset context (but keep user profile)
        await self.context_manager.reset_context(user_id, session_id)
        
        # Return state info
        return await self.get_state_info(user_id, session_id)
