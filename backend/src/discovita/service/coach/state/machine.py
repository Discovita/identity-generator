"""State machine for managing the coaching process flow."""

from typing import Dict, Any, List, Optional, Callable, Set
from discovita.service.coach.models import CoachingState, StateTransition, CoachContext, TransitionCondition

class CoachStateMachine:
    """State machine for managing the coaching process flow."""
    
    def __init__(self):
        self.transitions: List[StateTransition] = []
        self.condition_registry: Dict[TransitionCondition, Callable[[CoachContext], bool]] = {}
    
    def register_condition(self, name: TransitionCondition, condition_func: Callable[[CoachContext], bool]) -> None:
        """Register a condition function for state transitions."""
        self.condition_registry[name] = condition_func
    
    def add_transition(
        self, 
        from_state: CoachingState, 
        to_state: CoachingState,
        condition_name: TransitionCondition,
        priority: int = 0
    ) -> None:
        """Add a transition to the state machine."""
        if condition_name not in self.condition_registry:
            raise ValueError(f"Condition '{condition_name}' not registered")
            
        transition = StateTransition(
            from_state=from_state,
            to_state=to_state,
            condition_name=condition_name,
            priority=priority
        )
        self.transitions.append(transition)
    
    def get_available_transitions(self, context: CoachContext) -> List[StateTransition]:
        """Get all transitions available from the current state."""
        return [
            t for t in self.transitions 
            if t.from_state == context.current_state
        ]
    
    def evaluate_transitions(self, context: CoachContext) -> Optional[CoachingState]:
        """Evaluate if any transitions should occur based on the current context."""
        current_state = context.current_state
        eligible_transitions = []
        
        for transition in self.transitions:
            if transition.from_state != current_state:
                continue
                
            condition_func = self.condition_registry.get(transition.condition_name)
            if not condition_func:
                continue
                
            if condition_func(context):
                eligible_transitions.append(transition)
        
        if not eligible_transitions:
            return None
            
        # Select transition with highest priority
        next_transition = max(eligible_transitions, key=lambda t: t.priority)
        return next_transition.to_state
    
    def transition(self, context: CoachContext) -> bool:
        """Attempt to transition to a new state based on context."""
        next_state = self.evaluate_transitions(context)
        if next_state:
            context.current_state = next_state
            return True
        return False
    
    def get_allowed_actions(self, state: CoachingState) -> Set[str]:
        """Get the set of allowed actions for a given state."""
        from discovita.service.coach.prompt.manager import PromptManager
        
        # Create a PromptManager instance and delegate to it
        # Note: PromptManager.__init__ will raise NotImplementedError in Step 2,
        # but this shows how it will be used in Step 3
        prompt_manager = PromptManager()
        return prompt_manager.get_allowed_actions(state)
