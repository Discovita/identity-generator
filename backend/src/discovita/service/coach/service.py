"""Coaching service implementation."""

from .models import CoachRequest, CoachResponse, CoachStructuredResponse
from .context_builder import ContextBuilder
from ..openai.client.client import OpenAIClient

class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
        self.context_builder = ContextBuilder()
    
    async def get_response(
        self,
        request: CoachRequest
    ) -> CoachResponse:
        """Get a response from the coach."""
        # Build messages with system prompt
        messages = []
        
        # Add system prompt
        messages.append({"role": "system", "content": self.context_builder.get_system_prompt()})
        
        # Add sample dialogue if available
        sample_dialogue = self.context_builder.get_sample_dialogue()
        if sample_dialogue:
            messages.append({
                "role": "system", 
                "content": f"Reference this sample dialogue style: {sample_dialogue}"
            })
        
        # Add profile information if available
        if request.profile:
            identities_str = "\n".join(
                f"- {i.category.name}: {i.name}" for i in request.profile.identities
            )
            profile_context = (
                "Current user profile:\n"
                f"Identities:\n{identities_str}\n"
                f"Current focus: {request.profile.current_focus.name if request.profile.current_focus else 'None'}"
            )
            messages.append({"role": "system", "content": profile_context})
        
        # Add conversation context
        messages.extend([msg.model_dump() for msg in request.context])
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        # Get structured completion from OpenAI
        structured_response = await self.client.get_structured_completion(
            messages=messages,
            response_model=CoachStructuredResponse
        )
        
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
            visualization_prompt=visualization_prompt
        )
