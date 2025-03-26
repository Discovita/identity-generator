"""Handler for executing coach actions."""

from typing import List
from uuid import uuid4
from ..models.state import CoachState, Identity
from ..models.action import Action, ActionType
from .models import (
    CreateIdentityParams,
    UpdateIdentityParams,
    AcceptIdentityParams,
    TransitionStateParams
)

def apply_actions(state: CoachState, actions: List[Action]) -> CoachState:
    """Apply actions to modify the coaching state."""
    new_state = state.model_copy(deep=True)
    
    for action in actions:
        if action.type == ActionType.CREATE_IDENTITY:
            params = CreateIdentityParams(**action.params)
            new_state.identities.append(Identity(
                id=str(uuid4()),
                description=params.description,
                is_accepted=False
            ))
            
        elif action.type == ActionType.UPDATE_IDENTITY:
            params = UpdateIdentityParams(**action.params)
            for identity in new_state.identities:
                if identity.id == params.id:
                    identity.description = params.description
                    break
                    
        elif action.type == ActionType.ACCEPT_IDENTITY:
            params = AcceptIdentityParams(**action.params)
            for identity in new_state.identities:
                if identity.id == params.id:
                    identity.is_accepted = True
                    break
                    
        elif action.type == ActionType.TRANSITION_STATE:
            params = TransitionStateParams(**action.params)
            new_state.current_state = params.to_state
    
    return new_state
