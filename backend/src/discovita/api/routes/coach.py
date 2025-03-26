"""Coach route handlers."""

from fastapi import APIRouter, Depends
from ...service.coach.models import CoachRequest, CoachResponse, CoachState
from ...service.coach.service import CoachService
from ..dependencies import get_coach_service

router = APIRouter()

@router.post("/user_input", response_model=CoachResponse)
async def handle_user_input(
    request: CoachRequest,
    service: CoachService = Depends(get_coach_service)
) -> CoachResponse:
    """Handle user input and get coach response."""
    result = await service.process_message(request.message, request.coach_state)
    return CoachResponse(
        message=result.message,
        coach_state=result.state,
        visualization_prompt=None  # We'll implement this later
    )
