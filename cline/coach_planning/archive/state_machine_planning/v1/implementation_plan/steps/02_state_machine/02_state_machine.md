# Step 2: Implement State Machine

This document details the implementation of the state machine component for the coaching system.

## Overview

The state machine is the core component that manages the coaching process flow. It:

1. Defines the possible states in the coaching process
2. Manages transitions between states based on conditions
3. Maintains the current state for each user session
4. Provides an interface for evaluating and executing transitions

## Implementation Details

### 1. Create State Machine Directory Structure

First, create the directory structure for the state machine components:

```
backend/src/discovita/service/coach/state/
├── __init__.py
├── machine.py        # State machine implementation
├── transitions.py    # State transition definitions
└── persistence.py    # State persistence
```

### 2. Implement State Machine Class

Create `state/machine.py` with the `CoachStateMachine` class:

```python
from typing import Dict, Any, List, Optional, Callable, Set
from discovita.service.coach.models import CoachingState, StateTransition, CoachContext

class CoachStateMachine:
    """State machine for managing the coaching process flow."""
    
    def __init__(self):
        self.transitions: List[StateTransition] = []
        self.condition_registry: Dict[str, Callable[[CoachContext], bool]] = {}
    
    def register_condition(self, name: str, condition_func: Callable[[CoachContext], bool]) -> None:
        """Register a condition function for state transitions."""
        self.condition_registry[name] = condition_func
    
    def add_transition(
        self, 
        from_state: CoachingState, 
        to_state: CoachingState,
        condition_name: str,
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
        prompt_manager = PromptManager()
        return set(prompt_manager.get_allowed_actions(state))
```

### 3. Define Standard Transition Conditions

Create `state/transitions.py` with standard transition conditions:

```python
from typing import Dict, Any, Callable
from discovita.service.coach.models import CoachingState, CoachContext

def register_standard_conditions(state_machine) -> None:
    """Register standard condition functions with the state machine."""
    state_machine.register_condition(
        "introduction_completed",
        lambda ctx: ctx.metadata.get("introduction_completed", False)
    )
    
    state_machine.register_condition(
        "has_draft_identities",
        lambda ctx: len(ctx.metadata.get("draft_identities", [])) > 0
    )
    
    state_machine.register_condition(
        "has_minimum_identities",
        lambda ctx: len(ctx.metadata.get("draft_identities", [])) >= 3
    )
    
    state_machine.register_condition(
        "has_refined_identity",
        lambda ctx: ctx.metadata.get("current_identity_refined", False)
    )
    
    state_machine.register_condition(
        "has_visualization",
        lambda ctx: ctx.metadata.get("current_identity_visualized", False)
    )
    
    state_machine.register_condition(
        "has_action_plan",
        lambda ctx: len(ctx.metadata.get("action_items", [])) > 0
    )
    
    state_machine.register_condition(
        "always",
        lambda ctx: True
    )

def setup_standard_transitions(state_machine) -> None:
    """Set up standard transitions in the state machine."""
    # Introduction to Identity Brainstorming
    state_machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        "introduction_completed",
        priority=1
    )
    
    # Identity Brainstorming to Identity Refinement
    state_machine.add_transition(
        CoachingState.IDENTITY_BRAINSTORMING,
        CoachingState.IDENTITY_REFINEMENT,
        "has_minimum_identities",
        priority=1
    )
    
    # Identity Refinement to Identity Visualization
    state_machine.add_transition(
        CoachingState.IDENTITY_REFINEMENT,
        CoachingState.IDENTITY_VISUALIZATION,
        "has_refined_identity",
        priority=1
    )
    
    # Identity Visualization to Action Planning
    state_machine.add_transition(
        CoachingState.IDENTITY_VISUALIZATION,
        CoachingState.ACTION_PLANNING,
        "has_visualization",
        priority=1
    )
    
    # Action Planning to Accountability
    state_machine.add_transition(
        CoachingState.ACTION_PLANNING,
        CoachingState.ACCOUNTABILITY,
        "has_action_plan",
        priority=1
    )
    
    # Allow returning to Identity Brainstorming from any state
    # (lower priority than forward progression)
    for state in [
        CoachingState.IDENTITY_REFINEMENT,
        CoachingState.IDENTITY_VISUALIZATION,
        CoachingState.ACTION_PLANNING,
        CoachingState.ACCOUNTABILITY
    ]:
        state_machine.add_transition(
            state,
            CoachingState.IDENTITY_BRAINSTORMING,
            "always",
            priority=0  # Lower priority
        )
```

### 4. Implement State Persistence

Create `state/persistence.py` for state persistence:

```python
from typing import Optional, Dict, Any
from discovita.service.coach.models import CoachContext, CoachingState

class StateStore:
    """Interface for state persistence."""
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user."""
        raise NotImplementedError
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user."""
        raise NotImplementedError

class InMemoryStateStore(StateStore):
    """In-memory implementation of state persistence."""
    
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user from memory."""
        if user_id not in self.contexts:
            return None
            
        context_data = self.contexts[user_id]
        return CoachContext.model_validate(context_data)
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user to memory."""
        self.contexts[context.user_id] = context.model_dump()

# This will be replaced with a database implementation later
```

### 5. Create State Machine Factory

Create `state/__init__.py` with a factory function:

```python
from .machine import CoachStateMachine
from .transitions import register_standard_conditions, setup_standard_transitions
from .persistence import StateStore, InMemoryStateStore

def create_state_machine() -> CoachStateMachine:
    """Create and configure a state machine with standard transitions."""
    machine = CoachStateMachine()
    register_standard_conditions(machine)
    setup_standard_transitions(machine)
    return machine

__all__ = [
    'CoachStateMachine',
    'StateStore',
    'InMemoryStateStore',
    'create_state_machine'
]
```

## Next Steps

After implementing the state machine:

1. Proceed to implementing the prompt manager in Step 3
2. Ensure the state machine integrates well with the context manager
