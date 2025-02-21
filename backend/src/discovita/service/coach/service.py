"""Coaching service implementation."""

from .models import CoachRequest, CoachResponse
from .context_builder import ContextBuilder
from .structured_response import CoachStructuredResponse
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
        
        # Extract visualization prompt if identities were suggested
        visualization_prompt = None
        if structured_response.identities:
            # Use the visualization from the first identity as the prompt
            visualization_prompt = next(
                (identity.visualization for identity in structured_response.identities 
                 if identity.visualization is not None),
                None
            )
        
        return CoachResponse(
            message=structured_response.message,
            suggested_identities=structured_response.identities,
            visualization_prompt=visualization_prompt
        )
