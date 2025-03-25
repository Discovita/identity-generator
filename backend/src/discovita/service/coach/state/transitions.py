"""State transition definitions for coaching service."""

from typing import Dict, Any, List, Callable
from ..models import CoachState, CoachingState

def check_introduction_complete(state: CoachState) -> bool:
    """Check if introduction phase is complete."""
    return state.metadata.get("introduction_completed", False)

def check_has_minimum_identities(state: CoachState) -> bool:
    """Check if we have the minimum required identities."""
    return len(state.identities) >= 5

def check_all_identities_accepted(state: CoachState) -> bool:
    """Check if all identities have been accepted."""
    return all(i.is_accepted for i in state.identities)

# Map of condition functions
CONDITION_FUNCTIONS: Dict[str, Callable[[CoachState], bool]] = {
    "introduction_completed": check_introduction_complete,
    "has_minimum_identities": check_has_minimum_identities,
    "all_identities_accepted": check_all_identities_accepted
}

# Define valid transitions
VALID_TRANSITIONS = [
    # Introduction -> Brainstorming
    {
        "from_state": CoachingState.INTRODUCTION,
        "to_state": CoachingState.IDENTITY_BRAINSTORMING,
        "condition": "introduction_completed"
    },
    
    # Brainstorming -> Refinement
    {
        "from_state": CoachingState.IDENTITY_BRAINSTORMING,
        "to_state": CoachingState.IDENTITY_REFINEMENT,
        "condition": "has_minimum_identities"
    }
]
