"""Coaching service implementation."""

from .models import CoachRequest, CoachResponse
from .context_builder import ContextBuilder
from .identity_processor import IdentityProcessor
from ..openai.client.client import OpenAIClient

class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
        self.context_builder = ContextBuilder()
        self.identity_processor = IdentityProcessor()
    
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
        
        # Get completion from OpenAI
        response = await self.client.get_completion(
            f"{context}\nuser: {request.message}"
        )
        
        # Process identities and visualizations
        suggested_identities = self.identity_processor.extract_identities(response)
        visualization_prompt = self.identity_processor.generate_visualization(
            suggested_identities
        )
        
        return CoachResponse(
            message=response,
            suggested_identities=suggested_identities,
            visualization_prompt=visualization_prompt
        )
