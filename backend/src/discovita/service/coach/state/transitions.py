"""Standard transition conditions for the coaching state machine."""

from typing import Dict, Any, Callable
from discovita.service.coach.models import CoachingState, CoachContext, TransitionCondition, ContextMetadataKey

def register_standard_conditions(state_machine) -> None:
    """Register standard condition functions with the state machine."""
    state_machine.register_condition(
        TransitionCondition.INTRODUCTION_COMPLETED,
        lambda ctx: ctx.metadata.get(ContextMetadataKey.INTRODUCTION_COMPLETED, False)
    )
    
    state_machine.register_condition(
        TransitionCondition.HAS_DRAFT_IDENTITIES,
        lambda ctx: len(ctx.metadata.get(ContextMetadataKey.DRAFT_IDENTITIES, [])) > 0
    )
    
    state_machine.register_condition(
        TransitionCondition.HAS_MINIMUM_IDENTITIES,
        lambda ctx: len(ctx.metadata.get(ContextMetadataKey.DRAFT_IDENTITIES, [])) >= 3
    )
    
    state_machine.register_condition(
        TransitionCondition.HAS_REFINED_IDENTITY,
        lambda ctx: ctx.metadata.get(ContextMetadataKey.CURRENT_IDENTITY_REFINED, False)
    )
    
    state_machine.register_condition(
        TransitionCondition.HAS_VISUALIZATION,
        lambda ctx: ctx.metadata.get(ContextMetadataKey.CURRENT_IDENTITY_VISUALIZED, False)
    )
    
    state_machine.register_condition(
        TransitionCondition.HAS_ACTION_PLAN,
        lambda ctx: len(ctx.metadata.get(ContextMetadataKey.ACTION_ITEMS, [])) > 0
    )
    
    state_machine.register_condition(
        TransitionCondition.ALWAYS,
        lambda ctx: True
    )

def setup_standard_transitions(state_machine) -> None:
    """Set up standard transitions in the state machine."""
    # Introduction to Identity Brainstorming
    state_machine.add_transition(
        CoachingState.INTRODUCTION,
        CoachingState.IDENTITY_BRAINSTORMING,
        TransitionCondition.INTRODUCTION_COMPLETED,
        priority=1
    )
    
    # Identity Brainstorming to Identity Refinement
    state_machine.add_transition(
        CoachingState.IDENTITY_BRAINSTORMING,
        CoachingState.IDENTITY_REFINEMENT,
        TransitionCondition.HAS_MINIMUM_IDENTITIES,
        priority=1
    )
    
    # Identity Refinement to Identity Visualization
    state_machine.add_transition(
        CoachingState.IDENTITY_REFINEMENT,
        CoachingState.IDENTITY_VISUALIZATION,
        TransitionCondition.HAS_REFINED_IDENTITY,
        priority=1
    )
    
    # Identity Visualization to Action Planning
    state_machine.add_transition(
        CoachingState.IDENTITY_VISUALIZATION,
        CoachingState.ACTION_PLANNING,
        TransitionCondition.HAS_VISUALIZATION,
        priority=1
    )
    
    # Action Planning to Accountability
    state_machine.add_transition(
        CoachingState.ACTION_PLANNING,
        CoachingState.ACCOUNTABILITY,
        TransitionCondition.HAS_ACTION_PLAN,
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
            TransitionCondition.ALWAYS,
            priority=0  # Lower priority
        )
