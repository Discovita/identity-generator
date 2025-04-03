"""Handler for executing coach actions."""

from typing import List
from uuid import uuid4

from ..models.action import Action, ActionType
from ..models.state import CoachState, Identity, IdentityState
from .models import (
    AcceptIdentityParams,
    AcceptIdentityRefinementParams,
    AddIdentityNoteParams,
    CreateIdentityParams,
    SelectIdentityFocusParams,
    TransitionStateParams,
    UpdateIdentityParams,
)


def apply_actions(state: CoachState, actions: List[Action] = None) -> CoachState:
    """Apply actions to modify the coaching state."""
    new_state = state.model_copy(deep=True)
    if not actions:
        return new_state

    for action in actions:
        if action.type == ActionType.CREATE_IDENTITY:
            params = CreateIdentityParams(**action.params)
            identity_id = str(uuid4())
            new_state.identities.append(
                Identity(
                    id=identity_id,
                    description=params.description,
                    state=IdentityState.PROPOSED,
                    notes=[params.note],
                    category=params.category,
                )
            )

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
                    identity.state = IdentityState.ACCEPTED
                    break

        elif action.type == ActionType.ACCEPT_IDENTITY_REFINEMENT:
            params = AcceptIdentityRefinementParams(**action.params)
            for identity in new_state.identities:
                if identity.id == params.id:
                    identity.state = IdentityState.REFINEMENT_COMPLETE
                    break

        elif action.type == ActionType.ADD_IDENTITY_NOTE:
            params = AddIdentityNoteParams(**action.params)
            for identity in new_state.identities:
                if identity.id == params.id:
                    identity.notes.append(params.note)
                    break

        elif action.type == ActionType.TRANSITION_STATE:
            params = TransitionStateParams(**action.params)
            new_state.current_state = params.to_state

        elif action.type == ActionType.SELECT_IDENTITY_FOCUS:
            params = SelectIdentityFocusParams(**action.params)
            # Set the current identity ID directly
            new_state.current_identity_id = params.id

    return new_state
