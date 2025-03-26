# Identity Note Feature Context

This document provides context for implementing the identity note feature in the coach system. The feature will allow the coach to add notes to identities during the brainstorming and refinement stages.

## Current Codebase Structure

### Core Models

The identity model is defined in:
- `backend/src/discovita/service/coach/models/state.py`

Current Identity model:
```python
class IdentityState(str, Enum):
    """Represents the possible states of an identity."""
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REFINEMENT_COMPLETE = "refinement_complete"

class Identity(BaseModel):
    """Represents a single identity with its state."""
    id: str = Field(..., description="Unique identifier for the identity")
    description: str = Field(..., description="Description of the identity")
    state: IdentityState = Field(IdentityState.PROPOSED, description="Current state of the identity")
```

### Action Types and Parameters

Action types are defined in:
- `backend/src/discovita/service/coach/models/action.py`

Current action types:
```python
class ActionType(str, Enum):
    """Types of actions that can be performed on the coaching state."""
    CREATE_IDENTITY = "create_identity"  # Create a new identity during brainstorming
    UPDATE_IDENTITY = "update_identity"  # Update an identity during refinement
    ACCEPT_IDENTITY = "accept_identity"  # Mark an identity as accepted (from PROPOSED to ACCEPTED)
    ACCEPT_IDENTITY_REFINEMENT = "accept_identity_refinement"  # Mark an identity as refinement complete (from ACCEPTED to REFINEMENT_COMPLETE)
    TRANSITION_STATE = "transition_state"  # Request state transition
```

Action parameters are defined in:
- `backend/src/discovita/service/coach/actions/models.py`

Current action parameters:
```python
class CreateIdentityParams(BaseModel):
    """Parameters for creating a new identity."""
    description: str = Field(..., description="Description of the identity")

class UpdateIdentityParams(BaseModel):
    """Parameters for updating an identity."""
    id: str = Field(..., description="ID of identity to update")
    description: str = Field(..., description="Updated description")

class AcceptIdentityParams(BaseModel):
    """Parameters for accepting an identity (changing state from PROPOSED to ACCEPTED)."""
    id: str = Field(..., description="ID of identity to accept")

class AcceptIdentityRefinementParams(BaseModel):
    """Parameters for marking an identity as refinement complete (changing state from ACCEPTED to REFINEMENT_COMPLETE)."""
    id: str = Field(..., description="ID of identity to mark as refinement complete")
```

### Action Handler

The action handler is defined in:
- `backend/src/discovita/service/coach/actions/handler.py`

Current action handler for creating identities:
```python
def apply_actions(state: CoachState, actions: List[Action]) -> CoachState:
    """Apply actions to modify the coaching state."""
    new_state = state.model_copy(deep=True)
    
    for action in actions:
        if action.type == ActionType.CREATE_IDENTITY:
            params = CreateIdentityParams(**action.params)
            new_state.identities.append(Identity(
                id=str(uuid4()),
                description=params.description,
                state=IdentityState.PROPOSED
            ))
```

### Prompt Templates

The prompt templates are defined in:
- `backend/src/discovita/service/coach/prompts/states/identity_brainstorming.md`
- `backend/src/discovita/service/coach/prompts/states/identity_refinement.md`

The action instructions are defined in:
- `backend/src/discovita/service/coach/prompts/shared/action_instructions.md`

## Changes Needed for Identity Note Feature

1. **Update Identity Model**:
   - Add a `notes` field to the `Identity` model in `state.py`

2. **Add New Action Type**:
   - Add `ADD_IDENTITY_NOTE` to `ActionType` enum in `action.py`

3. **Add New Action Parameters**:
   - Create `AddIdentityNoteParams` in `actions/models.py`
   - Update `CreateIdentityParams` to include a required `note` field

4. **Update Action Handler**:
   - Update `apply_actions` in `handler.py` to handle the new `ADD_IDENTITY_NOTE` action
   - Update the `CREATE_IDENTITY` handler to include the initial note

5. **Update Prompt Templates**:
   - Update `action_instructions.md` to include the new action
   - Update `identity_brainstorming.md` and `identity_refinement.md` to instruct the LLM about using the new action

## Implementation Strategy

1. Start by updating the core models to include the notes field
2. Add the new action type and parameters
3. Update the action handler to handle the new action
4. Update the prompt templates to instruct the LLM about the new action
5. Test the changes to ensure they work correctly

## Testing

The changes can be tested using the existing test framework:
- `backend/test/service_coach/test_models.py` for model changes
- `backend/test/service_coach/test_service.py` for service changes
