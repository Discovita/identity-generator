# SELECT_IDENTITY_FOCUS Action Implementation Context

## Problem Statement

The coach currently has a clunky transition to the identity refinement phase:

1. The coach explicitly mentions "identity refinement phase" which breaks immersion
2. The initial message in refinement phase doesn't provide clear guidance or ask a question
3. The `current_identity_index` is not being set properly
4. There's no action for the coach to select which identity to focus on for refinement

## Solution Overview

1. Add a new `SELECT_IDENTITY_FOCUS` action to allow the coach to select an identity for refinement
2. Update the action handler to process this new action
3. Update the prompt templates to make transitions more natural and conversational
4. Ensure the coach asks clear questions during transitions

## Implementation Details

### 1. Add SELECT_IDENTITY_FOCUS Action Type

Update `backend/src/discovita/service/coach/models/action.py`:

```python
class ActionType(str, Enum):
    """Types of actions that can be performed on the coaching state."""
    CREATE_IDENTITY = "create_identity"  # Create a new identity during brainstorming
    UPDATE_IDENTITY = "update_identity"  # Update an identity during refinement
    ACCEPT_IDENTITY = "accept_identity"  # Mark an identity as accepted (from PROPOSED to ACCEPTED)
    ACCEPT_IDENTITY_REFINEMENT = "accept_identity_refinement"  # Mark an identity as refinement complete (from ACCEPTED to REFINEMENT_COMPLETE)
    ADD_IDENTITY_NOTE = "add_identity_note"  # Add a note to an identity
    TRANSITION_STATE = "transition_state"  # Request state transition
    SELECT_IDENTITY_FOCUS = "select_identity_focus"  # Select an identity to focus on during refinement
```

### 2. Add SelectIdentityFocusParams Model

Update `backend/src/discovita/service/coach/actions/models.py`:

```python
class SelectIdentityFocusParams(BaseModel):
    """Parameters for selecting an identity to focus on during refinement."""
    id: str = Field(..., description="ID of identity to focus on")
```

### 3. Update Action Handler

Update `backend/src/discovita/service/coach/actions/handler.py`:

```python
from .models import (
    CreateIdentityParams,
    UpdateIdentityParams,
    AcceptIdentityParams,
    AcceptIdentityRefinementParams,
    TransitionStateParams,
    AddIdentityNoteParams,
    SelectIdentityFocusParams  # Add this import
)

def apply_actions(state: CoachState, actions: List[Action]) -> CoachState:
    """Apply actions to modify the coaching state."""
    new_state = state.model_copy(deep=True)
    
    for action in actions:
        # ... existing action handling ...
        
        elif action.type == ActionType.SELECT_IDENTITY_FOCUS:
            params = SelectIdentityFocusParams(**action.params)
            # Find the index of the identity with the given ID
            for i, identity in enumerate(new_state.identities):
                if identity.id == params.id:
                    new_state.current_identity_index = i
                    break
    
    return new_state
```

### 4. Update ActionDefinitionService

Update `backend/src/discovita/service/coach/actions/service.py` to include the new action:

```python
from .models import (
    FunctionDefinition,
    CreateIdentityParams,
    UpdateIdentityParams,
    AcceptIdentityParams,
    TransitionStateParams,
    SelectIdentityFocusParams  # Add this import
)

class ActionDefinitionService:
    """Service for managing OpenAI function definitions."""
    
    def get_function_definitions(self) -> List[FunctionDefinition]:
        """Get all available function definitions."""
        return [
            # ... existing function definitions ...
            
            FunctionDefinition(
                name="select_identity_focus",
                description="Select an identity to focus on during the refinement process",
                parameters=SelectIdentityFocusParams.model_json_schema()
            ),
        ]
```

### 5. Update Identity Refinement Prompt

Update `backend/src/discovita/service/coach/prompts/states/identity_refinement.md`:

```markdown
---
required_context_keys:
  - user_summary
  - recent_messages
  - identities
  - current_focus
allowed_actions:
  - update_identity
  - accept_identity
  - accept_identity_refinement
  - add_identity_note
  - select_identity_focus  # Add this
  - transition_state
---

# Identity Refinement State

You are Leigh Ann, a professional life coach. Your goal is to help the client refine their chosen identities into powerful "I am" statements.

## Key Points to Cover

1. Focus on one identity at a time (the current focus identity)
2. Help the client refine their identity into a clear, powerful "I am" statement
3. Ensure the identity is specific, positive, and emotionally resonant
4. Explore how this identity will impact different areas of their life

## Transition Guidelines

When transitioning to the identity refinement phase:

1. **Use Natural Language**: Don't explicitly mention "identity refinement phase" - use conversational language.

2. **Provide Clear Guidance**: When beginning refinement, ask the user which identity they'd like to work on first. For example:
   - "Now that we've explored several identity possibilities, which one would you like to deepen first?"
   - "These identities are a great foundation. Which one feels most important to explore further right now?"

3. **Use SELECT_IDENTITY_FOCUS Action**: When the user chooses an identity to work on, use this action to set the current focus.

## Thoughtful Questions

For each identity, ask probing questions that help the user think deeply:
- "What does being a [identity] mean to you on a daily basis?"
- "How does this identity connect to your core values?"
- "What specific behaviors or habits would strengthen this identity?"
- "How would embracing this identity change how you see yourself?"
- "What's one small step you could take tomorrow to embody this identity more fully?"

## Refinement Process

Guide the client through:
- Clarifying what this identity means to them personally
- Making the identity statement specific and actionable
- Ensuring the identity feels authentic and aligned with their values
- Exploring how this identity will manifest in their daily life

## Current Context

Current user information: {user_summary}

Recent conversation: {recent_messages}

### Current Identities
{identities}

Current focus identity: {current_focus}

## Response Guidelines

- Focus exclusively on the current identity being refined
- Ask probing questions to help them clarify their thinking
- Suggest improvements to make their identity statement more powerful
- When the identity is well-refined, either:
  - Move on to refining another identity if there are more to refine
  - If all identities are refined, provide a positive concluding message that:
    1. Reviews all the identities they've created
    2. Acknowledges their work and progress
    3. Invites them to continue open dialogue until they're ready to end the session

## Identity State Management

- During refinement, all identities should be transitioned from ACCEPTED to REFINEMENT_COMPLETE
- For each identity, you should:
  1. Help the user refine the identity
  2. Use UPDATE_IDENTITY to improve the description if needed
  3. Probe the user to make sure they love the refined identity
  4. Use the ACCEPT_IDENTITY_REFINEMENT action to transition it to the REFINEMENT_COMPLETE state

## Action Guidelines

- IMPORTANT: Make sure you don't create duplicate identities.  
Review the Current Identities in context before creating a new one.

- Use select_identity_focus action when:
  - The user has chosen an identity to work on
  - You need to set the current focus to that identity
  - Include the identity_id to set as the current focus

- Use update_identity action when:
  - You've helped refine an identity statement
  - The user agrees with the refined version
  - Include the identity_id and updated description
  - You can combine this with accept_identity_refinement in the same response if the user clearly loves the identity

- Use accept_identity_refinement action when:
  - The user has confirmed they are satisfied with the refined identity
  - This transitions the identity from ACCEPTED to REFINEMENT_COMPLETE state
  - Include the identity_id to mark as refinement complete

- Use add_identity_note action when:
  - You learn valuable information about how the user perceives an identity
  - You want to capture insights about why this identity resonates with them
  - You notice patterns in how they talk about or relate to this identity
  - Include the identity_id and a detailed note capturing the insight

- Use transition_state action when:
  - All identities have been refined and marked as REFINEMENT_COMPLETE
  - The user is ready to move to the conclusion
  - Set to_state to "CONCLUSION"

Remember: Always follow the response format specified in the response format instructions, providing both a message to the user and any actions in the correct JSON structure.
```

## Example Conversation Flow

Here's an example of how the improved conversation flow should work:

1. **User**: "I'm ready to move on."

2. **Coach**: "Great! We've explored several interesting identity possibilities together. Now let's take some time to deepen our understanding of each one. Which identity would you like to start with - Fun-Loving Parent, Innovative Software Engineer, or Mindful Self-Stylist?"
   - *Coach uses natural language without mentioning "refinement phase"*
   - *Coach asks a clear question about which identity to focus on first*

3. **User**: "Let's start with Fun-Loving Parent."

4. **Coach**: "Let's explore your Fun-Loving Parent identity. What does being a fun-loving parent look like in your daily life? What activities or moments make you feel most connected to your children through fun and play?"
   - *Coach uses SELECT_IDENTITY_FOCUS action to set current_identity_index*
   - *Coach asks thoughtful, probing questions about the identity*

## Testing Considerations

1. Verify the `SELECT_IDENTITY_FOCUS` action correctly sets the `current_identity_index`
2. Ensure the coach's language is natural and doesn't reference internal states
3. Check that the coach consistently asks clear questions during transitions
4. Confirm the coach asks thoughtful questions that help users think deeply about their identities

## Implementation Steps

1. Add the new action type to `ActionType` enum
2. Create the `SelectIdentityFocusParams` model
3. Update the action handler to process the new action
4. Update the ActionDefinitionService to include the new action
5. Update the identity refinement prompt template to guide the coach on using the new action
6. Test the implementation with various conversation flows
