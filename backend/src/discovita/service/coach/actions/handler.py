"""Handler for executing coach actions."""

from typing import List
from uuid import uuid4
from ..models.state import CoachState, Identity
from ..models.action import Action, ActionType

def apply_actions(state: CoachState, actions: List[Action]) -> CoachState:
    """Apply actions to modify the coaching state."""
    new_state = state.model_copy(deep=True)
    
    for action in actions:
        if action.type == ActionType.CREATE_IDENTITY:
            new_state.identities.append(Identity(
                id=str(uuid4()),
                description=action.params["description"],
                is_accepted=False
            ))
            
        elif action.type == ActionType.UPDATE_IDENTITY:
            for identity in new_state.identities:
                if identity.id == action.params["id"]:
                    identity.description = action.params["description"]
                    break
                    
        elif action.type == ActionType.ACCEPT_IDENTITY:
            for identity in new_state.identities:
                if identity.id == action.params["id"]:
                    identity.is_accepted = True
                    break
                    
        elif action.type == ActionType.COMPLETE_INTRODUCTION:
            new_state.metadata["introduction_completed"] = True
            
        elif action.type == ActionType.TRANSITION_STATE:
            # State machine will handle actual transition after action processing
            new_state.metadata["requested_state"] = action.params["to_state"]
    
    return new_state
