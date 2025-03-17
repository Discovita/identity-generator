"""State machine for coaching service."""

from .machine import CoachStateMachine
from .transitions import register_standard_conditions, setup_standard_transitions
from discovita.db.state_store import StateStore, InMemoryStateStore

def create_state_machine() -> CoachStateMachine:
    """Create and configure a state machine with standard transitions."""
    machine = CoachStateMachine()
    register_standard_conditions(machine)
    setup_standard_transitions(machine)
    return machine

__all__ = [
    'CoachStateMachine',
    'create_state_machine'
]
