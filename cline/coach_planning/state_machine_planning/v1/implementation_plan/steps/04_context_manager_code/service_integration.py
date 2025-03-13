from typing import Dict, Any, List, Optional
from discovita.service.coach.models import (
    CoachRequest, 
    CoachResponse, 
    CoachStructuredResponse,
    CoachContext,
    ActionType,
    Action
)
from discovita.service.coach.state import CoachStateMachine, create_state_machine
from discovita.service.coach.prompt import PromptManager, create_prompt_manager
from discovita.service.coach.context.manager import ContextManager
from discovita.service.coach.context.persistence import ContextPersistence, FileContextPersistence
from discovita.service.openai.client.client import OpenAIClient

class CoachService:
    """Service for handling coaching interactions with state management."""
    
    def __init__(
        self, 
        llm_client: OpenAIClient,
        context_persistence: Optional[ContextPersistence] = None
    ):
        """Initialize the coach service."""
        self.llm_client = llm_client
        
        # Create the state machine
        self.state_machine = create_state_machine()
        
        # Create the prompt manager
        self.prompt_manager = create_prompt_manager()
        
        # Create the context manager
        if context_persistence is None:
            context_persistence = FileContextPersistence()
        
        self.context_manager = ContextManager(
            llm_client=llm_client
        )
        
        self.context_persistence = context_persistence
    
    async def get_response(self, request: CoachRequest) -> CoachResponse:
        """Get a response from the coach."""
        # Load or create context for this user
        context = await self.context_manager.load_context(request.user_id)
        
        # Update context with user profile if provided
        if request.profile:
            context = await self.context_manager.update_user_profile(
                context, 
                request.profile
            )
        
        # Add the user's message to the context
        context = await self.context_manager.add_message(
            context, 
            "user", 
            request.message
        )
        
        # Get the current state
        current_state = context.current_state
        
        # Get the prompt for the current state
        prompt = self.prompt_manager.get_prompt(current_state, context)
        
        # Get structured completion from OpenAI
        structured_response = await self.llm_client.get_structured_completion(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": request.message}
            ],
            response_model=CoachStructuredResponse
        )
        
        # Extract actions from the response
        actions = self._extract_actions(structured_response)
        
        # Execute actions
        for action in actions:
            await self._execute_action(context, action)
        
        # Check for state transitions
        self.state_machine.transition(context)
        
        # Add the assistant's response to the context
        context = await self.context_manager.add_message(
            context, 
            "assistant", 
            structured_response.message
        )
        
        # Save the updated context
        await self.context_persistence.save_context(context)
        
        # Extract visualization prompt if an identity was proposed or confirmed
        visualization_prompt = None
        
        # Check proposed identity first
        if structured_response.proposed_identity and structured_response.proposed_identity.visualization:
            visualization_prompt = structured_response.proposed_identity.visualization
        # If no proposed identity with visualization, check confirmed identity
        elif structured_response.confirmed_identity and structured_response.confirmed_identity.visualization:
            visualization_prompt = structured_response.confirmed_identity.visualization
        
        return CoachResponse(
            message=structured_response.message,
            proposed_identity=structured_response.proposed_identity,
            confirmed_identity=structured_response.confirmed_identity,
            visualization_prompt=visualization_prompt,
            current_state=context.current_state.value
        )
    
    def _extract_actions(self, response: CoachStructuredResponse) -> List[Action]:
        """Extract actions from the structured response."""
        actions = []
        
        # Check for identity actions
        if response.proposed_identity:
            actions.append(Action(
                type=ActionType.SAVE_IDENTITY,
                params={"identity": response.proposed_identity.model_dump(), "status": "proposed"}
            ))
        
        if response.confirmed_identity:
            actions.append(Action(
                type=ActionType.SAVE_IDENTITY,
                params={"identity": response.confirmed_identity.model_dump(), "status": "confirmed"}
            ))
        
        # Additional actions could be extracted from the message content
        # using a parser that looks for action markers
        
        return actions
    
    async def _execute_action(self, context: CoachContext, action: Action) -> None:
        """Execute an action on the context."""
        if action.type == ActionType.SAVE_IDENTITY:
            # Save identity to the user profile
            identity_data = action.params.get("identity", {})
            status = action.params.get("status", "")
            
            # Update metadata based on the action
            if status == "proposed":
                await self.context_manager.update_metadata(
                    context, 
                    "proposed_identity", 
                    identity_data
                )
            elif status == "confirmed":
                await self.context_manager.update_metadata(
                    context, 
                    "confirmed_identity", 
                    identity_data
                )
                
                # Also add to draft identities for state transitions
                draft_identities = context.metadata.get("draft_identities", [])
                draft_identities.append(identity_data)
                await self.context_manager.update_metadata(
                    context, 
                    "draft_identities", 
                    draft_identities
                )
        
        elif action.type == ActionType.MARK_INTRODUCTION_COMPLETE:
            # Mark the introduction as complete
            await self.context_manager.update_metadata(
                context, 
                "introduction_completed", 
                True
            )
        
        elif action.type == ActionType.TRANSITION_STATE:
            # Force a state transition
            target_state = action.params.get("target_state")
            if target_state:
                context.current_state = target_state
        
        # Additional action types would be handled here
