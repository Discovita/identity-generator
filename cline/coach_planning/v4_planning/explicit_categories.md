# Identity Categories Implementation Plan

This document outlines the changes needed to explicitly associate identities with identity categories in the coach service.

## Current State

Currently, the `Identity` model in `backend/src/discovita/service/coach/models/identity.py` already has a `category` field of type `IdentityCategory`, but the `CREATE_IDENTITY` action in `backend/src/discovita/service/coach/actions/models.py` does not include this parameter. The `Identity` model in `backend/src/discovita/service/coach/models/state.py` also doesn't include the category field.

## Required Changes

### 1. Update CreateIdentityParams in actions/models.py

```python
# backend/src/discovita/service/coach/actions/models.py
class CreateIdentityParams(BaseModel):
    """Parameters for creating a new identity."""
    description: str = Field(..., description="Description of the identity")
    note: str = Field(..., description="Initial note about why this identity was created")
    category: IdentityCategory = Field(..., description="Category this identity belongs to")
```

### 2. Update apply_actions in actions/handler.py

```python
# backend/src/discovita/service/coach/actions/handler.py
if action.type == ActionType.CREATE_IDENTITY:
    params = CreateIdentityParams(**action.params)
    identity_id = str(uuid4())
    new_state.identities.append(Identity(
        id=identity_id,
        description=params.description,
        state=IdentityState.PROPOSED,
        notes=[params.note],
        category=params.category  # Add category parameter
    ))
```

### 3. Update Identity model in models/state.py

```python
# backend/src/discovita/service/coach/models/state.py
class Identity(BaseModel):
    """Represents a single identity with its state."""
    id: str = Field(..., description="Unique identifier for the identity")
    description: str = Field(..., description="Description of the identity")
    state: IdentityState = Field(IdentityState.PROPOSED, description="Current state of the identity")
    notes: List[str] = Field(default_factory=list, description="Notes about the identity")
    category: IdentityCategory = Field(..., description="Category this identity belongs to")
```

### 4. Update prompts to include category parameter

Update the identity brainstorming prompt to instruct the LLM to include the category parameter when creating identities:

```markdown
# backend/src/discovita/service/coach/prompts/states/identity_brainstorming.md
- Use create_identity action ONLY when:
  - The user expresses a completely new identity that doesn't exist in any form in the "Current identities" list
  - You've helped refine their thoughts into an "I am" statement
  - Include the full identity description as a single "description" parameter
  - Include the appropriate identity category from the IdentityCategory enum (PASSIONS, MONEY_MAKER, MONEY_KEEPER, SPIRITUAL, APPEARANCE, HEALTH, FAMILY, ROMANTIC, ACTION)
  - Example: "Innovative Engineer and Entrepreneur"
  - Note: This will create the identity in the PROPOSED state
  - Note: Identities are capitalized descriptions, not complete sentences. Not "I am a skilled engineer", for example.
```

### 5. Import IdentityCategory in actions/models.py

```python
# backend/src/discovita/service/coach/actions/models.py
from ..models.identity import IdentityCategory
```

### 6. Import IdentityCategory in actions/handler.py

```python
# backend/src/discovita/service/coach/actions/handler.py
from ..models.identity import IdentityCategory
```

## Additional Considerations

1. We need to ensure that any existing code that creates or updates identities is updated to include the category parameter.
2. We should update tests to include the category parameter when creating identities.
3. We should verify that the LLM response parser correctly handles the category parameter.
