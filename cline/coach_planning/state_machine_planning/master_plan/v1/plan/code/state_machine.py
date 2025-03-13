from typing import List, Dict, Any, Optional, Callable
from enum import Enum, auto
from dataclasses import dataclass

class CoachingState(Enum):
    INTRODUCTION = auto()
    IDENTITY_BRAINSTORMING = auto()
    IDENTITY_REFINEMENT = auto()
    IDENTITY_VISUALIZATION = auto()
    ACTION_PLANNING = auto()
    ACCOUNTABILITY = auto()
    # Add more states as needed

@dataclass
class StateTransition:
    from_state: CoachingState
    to_state: CoachingState
    condition: Callable[[Dict[str, Any]], bool]
    priority: int = 0

class CoachStateMachine:
    def __init__(self, initial_state: CoachingState = CoachingState.INTRODUCTION):
        self.current_state = initial_state
        self.transitions: List[StateTransition] = []
        self._setup_transitions()
    
    def _setup_transitions(self) -> None:
        """Define all possible state transitions and their conditions."""
        # Example transitions
        self.add_transition(
            CoachingState.INTRODUCTION,
            CoachingState.IDENTITY_BRAINSTORMING,
            lambda ctx: ctx.get("introduction_completed", False)
        )
        self.add_transition(
            CoachingState.IDENTITY_BRAINSTORMING,
            CoachingState.IDENTITY_REFINEMENT,
            lambda ctx: len(ctx.get("draft_identities", [])) >= 3
        )
        # Add more transitions as needed
    
    def add_transition(self, from_state: CoachingState, to_state: CoachingState, 
                      condition: Callable[[Dict[str, Any]], bool], priority: int = 0) -> None:
        """Add a new transition to the state machine."""
        self.transitions.append(StateTransition(from_state, to_state, condition, priority))
    
    def evaluate_transitions(self, context: Dict[str, Any]) -> Optional[CoachingState]:
        """Evaluate if any transitions should occur based on the current context."""
        eligible_transitions = [
            t for t in self.transitions 
            if t.from_state == self.current_state and t.condition(context)
        ]
        
        if not eligible_transitions:
            return None
            
        # Select transition with highest priority
        next_transition = max(eligible_transitions, key=lambda t: t.priority)
        return next_transition.to_state
    
    def transition(self, context: Dict[str, Any]) -> bool:
        """Attempt to transition to a new state based on context."""
        next_state = self.evaluate_transitions(context)
        if next_state:
            self.current_state = next_state
            return True
        return False
