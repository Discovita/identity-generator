import logging
from typing import Optional
from .models.request_response import CoachStateResponse

# Configure logger
logger = logging.getLogger(__name__)

class ServiceError(Exception):
    """Base exception for service errors."""
    def __init__(self, message: str, code: str = "SERVICE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class StateError(ServiceError):
    """Exception for state-related errors."""
    def __init__(self, message: str):
        super().__init__(message, "STATE_ERROR")

class ContextError(ServiceError):
    """Exception for context-related errors."""
    def __init__(self, message: str):
        super().__init__(message, "CONTEXT_ERROR")

class ActionError(ServiceError):
    """Exception for action-related errors."""
    def __init__(self, message: str):
        super().__init__(message, "ACTION_ERROR")

def handle_service_error(
    error: Exception,
    session_id: str,
    state_value: Optional[str] = None
) -> CoachStateResponse:
    """Handle service errors and return appropriate response."""
    # Log the error
    logger.error(f"Service error: {str(error)}", exc_info=True)
    
    # Create error message based on error type
    if isinstance(error, StateError):
        message = "I'm sorry, there was an issue with the coaching process. Let's try again."
    elif isinstance(error, ContextError):
        message = "I'm sorry, I lost track of our conversation. Can we start again from here?"
    elif isinstance(error, ActionError):
        message = "I'm sorry, I couldn't complete the requested action. Let's continue our conversation."
    else:
        message = "I'm sorry, I encountered an unexpected error. Please try again."
    
    # Return error response
    return CoachStateResponse(
        message=message,
        current_state=state_value or "ERROR",
        session_id=session_id,
        error=str(error),
        error_code=getattr(error, "code", "UNKNOWN_ERROR") if hasattr(error, "code") else "UNKNOWN_ERROR"
    )

# Example usage in service.py:
"""
async def process_message(
    self,
    request: CoachStateRequest
) -> CoachStateResponse:
    try:
        # Implementation
        return response
    except Exception as e:
        return handle_service_error(e, session_id, state.value if state else None)
"""
