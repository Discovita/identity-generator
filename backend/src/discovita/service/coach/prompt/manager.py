"""Prompt manager for coaching service."""

from typing import List, Dict, Any, Set
from discovita.service.coach.models import CoachingState, ActionType

class PromptManager:
    """Manager for state-specific prompts and allowed actions."""
    
    def __init__(self):
        """Initialize the prompt manager."""
        # This is a stub that will be fully implemented in Step 3
        raise NotImplementedError("PromptManager will be implemented in Step 3: Prompt Manager")
    
    def get_prompt(self, state: CoachingState, context: Dict[str, Any]) -> str:
        """Get a prompt for the given state and context."""
        # This is a stub that will be fully implemented in Step 3
        raise NotImplementedError("PromptManager will be implemented in Step 3: Prompt Manager")
    
    def get_allowed_actions(self, state: CoachingState) -> Set[str]:
        """Get the set of allowed actions for a given state."""
        # This is a stub that will be fully implemented in Step 3
        # For now, return a placeholder mapping of states to allowed actions
        allowed_actions_map = {
            CoachingState.INTRODUCTION: {
                ActionType.SAVE_USER_INFO.value,
                ActionType.MARK_INTRODUCTION_COMPLETE.value,
                ActionType.TRANSITION_STATE.value
            },
            CoachingState.IDENTITY_BRAINSTORMING: {
                ActionType.SAVE_IDENTITY.value,
                ActionType.TRANSITION_STATE.value
            },
            CoachingState.IDENTITY_REFINEMENT: {
                ActionType.SAVE_IDENTITY.value,
                ActionType.SET_FOCUS_IDENTITY.value,
                ActionType.TRANSITION_STATE.value
            },
            CoachingState.IDENTITY_VISUALIZATION: {
                ActionType.SAVE_VISUALIZATION.value,
                ActionType.TRANSITION_STATE.value
            },
            CoachingState.ACTION_PLANNING: {
                ActionType.CREATE_ACTION_ITEM.value,
                ActionType.TRANSITION_STATE.value
            },
            CoachingState.ACCOUNTABILITY: {
                ActionType.MARK_ACTION_COMPLETE.value,
                ActionType.CREATE_ACTION_ITEM.value,
                ActionType.TRANSITION_STATE.value
            }
        }
        
        # Return the allowed actions for the given state, or an empty set if not defined
        return allowed_actions_map.get(state, set())
