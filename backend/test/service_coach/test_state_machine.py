"""Tests for the coach state machine."""

import pytest
from unittest.mock import patch, MagicMock
from discovita.service.coach.models import (
    CoachingState,
    TransitionCondition,
    ContextMetadataKey,
    CoachContext,
    ActionType
)
from discovita.service.coach.state import CoachStateMachine, create_state_machine

def test_state_machine_creation():
    """Test that the state machine can be created."""
    machine = create_state_machine()
    assert isinstance(machine, CoachStateMachine)
    assert len(machine.transitions) > 0
    assert len(machine.condition_registry) > 0

def test_condition_registration():
    """Test that conditions can be registered with the state machine."""
    machine = CoachStateMachine()
    machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )
    assert TransitionCondition.ALWAYS in machine.condition_registry
    assert machine.condition_registry[TransitionCondition.ALWAYS](None) is True

def test_transition_addition():
    """Test that transitions can be added to the state machine."""
    machine = CoachStateMachine()
    machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        TransitionCondition.ALWAYS,
        priority=1
    )
    assert len(machine.transitions) == 1
    transition = machine.transitions[0]
    assert transition.from_state == CoachingState.INTRODUCTION
    assert transition.to_state == CoachingState.IDENTITY_BRAINSTORMING
    assert transition.condition_name == TransitionCondition.ALWAYS
    assert transition.priority == 1

def test_get_available_transitions():
    """Test that available transitions can be retrieved."""
    machine = CoachStateMachine()
    machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        TransitionCondition.ALWAYS
    )
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_REFINEMENT,
        TransitionCondition.ALWAYS
    )
    machine.add_transition(
        CoachingState.IDENTITY_BRAINSTORMING,
        CoachingState.IDENTITY_REFINEMENT,
        TransitionCondition.ALWAYS
    )
    
    context = CoachContext(user_id="test_user", current_state=CoachingState.INTRODUCTION)
    transitions = machine.get_available_transitions(context)
    assert len(transitions) == 2
    
    context.current_state = CoachingState.IDENTITY_BRAINSTORMING
    transitions = machine.get_available_transitions(context)
    assert len(transitions) == 1
    assert transitions[0].to_state == CoachingState.IDENTITY_REFINEMENT

def test_evaluate_transitions():
    """Test that transitions can be evaluated based on conditions and priorities."""
    machine = CoachStateMachine()
    
    # Register two conditions: one that's always true and one that depends on metadata
    machine.register_condition(
        TransitionCondition.INTRODUCTION_COMPLETED,
        lambda ctx: ctx.metadata.get(ContextMetadataKey.INTRODUCTION_COMPLETED, False)
    )
    machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )
    
    # Add two transitions from INTRODUCTION state with different priorities
    # Higher priority (2) transition requires INTRODUCTION_COMPLETED to be true
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        TransitionCondition.INTRODUCTION_COMPLETED,
        priority=2  # Higher priority
    )
    
    # Lower priority (1) transition is always eligible
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_REFINEMENT,
        TransitionCondition.ALWAYS,
        priority=1  # Lower priority
    )
    
    # Test case 1: Context without introduction_completed
    # Only the ALWAYS condition is true, so only the transition to IDENTITY_REFINEMENT is eligible
    context = CoachContext(user_id="test_user", current_state=CoachingState.INTRODUCTION)
    next_state = machine.evaluate_transitions(context)
    assert next_state == CoachingState.IDENTITY_REFINEMENT
    
    # Test case 2: Context with introduction_completed
    # Both conditions are true, but the transition to IDENTITY_BRAINSTORMING has higher priority
    context.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True
    next_state = machine.evaluate_transitions(context)
    assert next_state == CoachingState.IDENTITY_BRAINSTORMING

def test_transition():
    """Test that the state machine can transition states."""
    machine = CoachStateMachine()
    machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )
    machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        TransitionCondition.ALWAYS
    )
    
    context = CoachContext(user_id="test_user", current_state=CoachingState.INTRODUCTION)
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.IDENTITY_BRAINSTORMING
    
    # No transitions available from IDENTITY_BRAINSTORMING
    result = machine.transition(context)
    assert result is False
    assert context.current_state == CoachingState.IDENTITY_BRAINSTORMING

def test_standard_transitions():
    """Test that the standard transitions work as expected."""
    machine = create_state_machine()
    
    # Test introduction to identity brainstorming
    context = CoachContext(user_id="test_user", current_state=CoachingState.INTRODUCTION)
    context.metadata[ContextMetadataKey.INTRODUCTION_COMPLETED] = True
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.IDENTITY_BRAINSTORMING
    
    # Test identity brainstorming to identity refinement
    context.metadata[ContextMetadataKey.DRAFT_IDENTITIES] = ["Identity 1", "Identity 2", "Identity 3"]
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.IDENTITY_REFINEMENT
    
    # Test identity refinement to identity visualization
    context.metadata[ContextMetadataKey.CURRENT_IDENTITY_REFINED] = True
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.IDENTITY_VISUALIZATION
    
    # Test identity visualization to action planning
    context.metadata[ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED] = True
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.ACTION_PLANNING
    
    # Test action planning to accountability
    context.metadata[ContextMetadataKey.ACTION_ITEMS] = ["Action 1", "Action 2"]
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.ACCOUNTABILITY
    
    # Test returning to identity brainstorming from accountability
    result = machine.transition(context)
    assert result is True
    assert context.current_state == CoachingState.IDENTITY_BRAINSTORMING

@patch('discovita.service.coach.prompt.manager.PromptManager')
def test_get_allowed_actions(mock_prompt_manager_class):
    """Test that allowed actions can be retrieved for a state."""
    # Set up the mock
    mock_prompt_manager = MagicMock()
    mock_prompt_manager.get_allowed_actions.return_value = {
        ActionType.SAVE_USER_INFO.value,
        ActionType.MARK_INTRODUCTION_COMPLETE.value
    }
    mock_prompt_manager_class.return_value = mock_prompt_manager
    
    # Create the state machine and call get_allowed_actions
    machine = CoachStateMachine()
    allowed_actions = machine.get_allowed_actions(CoachingState.INTRODUCTION)
    
    # Verify the result
    assert ActionType.SAVE_USER_INFO.value in allowed_actions
    assert ActionType.MARK_INTRODUCTION_COMPLETE.value in allowed_actions
    assert len(allowed_actions) == 2
    
    # Verify the mock was called correctly
    mock_prompt_manager.get_allowed_actions.assert_called_once_with(CoachingState.INTRODUCTION)
