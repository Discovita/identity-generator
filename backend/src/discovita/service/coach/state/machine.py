"""State machine for managing the coaching process flow."""

from typing import Dict, Any, Optional
from ..models.state import CoachState, CoachingState, IdentityState

class StateMachine:
    """State machine for managing the coaching process flow."""
    
    def check_transitions(self, state: CoachState) -> CoachState:
        """Check and apply any state transitions based on current state."""
        new_state = state.model_copy(deep=True)
        
        # Check for explicit transition request
        if "requested_state" in new_state.metadata:
            requested = new_state.metadata["requested_state"]
            del new_state.metadata["requested_state"]
            new_state.current_state = CoachingState(requested)
            return new_state
            
        # Check for automatic transitions based on state
        if new_state.current_state == CoachingState.IDENTITY_BRAINSTORMING:
            # Transition to refinement when we have 5 identities
            if len(new_state.identities) >= 5:
                new_state.current_state = CoachingState.IDENTITY_REFINEMENT
                new_state.current_identity_index = 0
                
        elif new_state.current_state == CoachingState.IDENTITY_REFINEMENT:
            # Check if all identities are in REFINEMENT_COMPLETE state
            if all(i.state == IdentityState.REFINEMENT_COMPLETE for i in new_state.identities):
                # We stay in refinement state but mark completion in metadata
                new_state.metadata["refinement_completed"] = True
        
        return new_state
