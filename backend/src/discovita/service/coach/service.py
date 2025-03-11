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
        # Build complete context
        context = self.context_builder.build_context(
            request.context,
            request.profile
        )
        
        # Get structured completion from OpenAI
        structured_response = await self.client.get_structured_completion(
            messages=[
                *[msg.model_dump() for msg in request.context],
                {"role": "user", "content": request.message}
            ],
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
