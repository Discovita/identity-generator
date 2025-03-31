from typing import Optional
from .models.request_response import CoachRequest, CoachResponse
from .models.request_response import CoachStateRequest, CoachStateResponse

class BackwardCompatibilityMixin:
    """Mixin to provide backward compatibility with the old API."""
    
    async def get_response(
        self,
        request: CoachRequest
    ) -> CoachResponse:
        """Legacy method for backward compatibility with the old API."""
        # Convert legacy request to new format
        state_request = CoachStateRequest(
            user_id=request.user_id,
            message=request.message,
            session_id=None  # Will create new session
        )
        
        # Process with new method
        state_response = await self.process_message(state_request)
        
        # Convert to legacy response format
        return CoachResponse(
            message=state_response.message,
            proposed_identity=state_response.proposed_identity,
            confirmed_identity=state_response.confirmed_identity,
            visualization_prompt=state_response.visualization_prompt
        )

# Example usage in service.py:
"""
class CoachService(BackwardCompatibilityMixin):
    # ... implementation ...
"""
