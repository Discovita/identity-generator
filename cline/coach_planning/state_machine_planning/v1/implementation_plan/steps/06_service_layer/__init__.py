"""Service layer implementation for the coach state machine."""

from .service import CoachService
from .factory import create_coach_service
from .error_handling import (
    ServiceError,
    StateError,
    ContextError,
    ActionError,
    handle_service_error
)
from .backward_compatibility import BackwardCompatibilityMixin

__all__ = [
    'CoachService',
    'create_coach_service',
    'ServiceError',
    'StateError',
    'ContextError',
    'ActionError',
    'handle_service_error',
    'BackwardCompatibilityMixin'
]
