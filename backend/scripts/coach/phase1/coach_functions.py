"""Function definitions for the coach LLM to update conversation state.

This module provides function definitions that allow the LLM to:
1. Add or update identities in the brainstorming and refinement stages
2. Control the state progression through the coaching flow
3. Monitor current state and progress
4. Update various metadata flags that influence state transitions

These functions act as a bridge between the natural language understanding 
of the LLM and the state manipulation capabilities of the TerminalCoach.
"""

from typing import Any, Dict, List, Literal, Optional

from openai.types.responses import FunctionTool
from pydantic import BaseModel, Field

# Define types for function parameters
IdentityCategory = Literal[
    "passions_and_talents",
    "maker_of_money",
    "keeper_of_money",
    "spiritual",
    "personal_appearance", 
    "physical_expression",
    "familial_relations",
    "romantic_relation",
    "doer_of_things"
]

CoachState = Literal[
    "introduction",
    "identity_brainstorming",
    "identity_refinement", 
    "identity_visualization"
]

# Function definitions for the LLM

add_draft_identity_function: FunctionTool = {
    "type": "function",
    "name": "add_draft_identity",
    "function": {
        "name": "add_draft_identity",
        "description": "Add a new identity to the draft list during the brainstorming phase. This should be used when proposing new identity concepts to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the identity (e.g., 'Creative Visionary')"
                },
                "category": {
                    "type": "string",
                    "description": "The category this identity belongs to",
                    "enum": [
                        "passions_and_talents",
                        "maker_of_money",
                        "keeper_of_money",
                        "spiritual",
                        "personal_appearance", 
                        "physical_expression",
                        "familial_relations",
                        "romantic_relation",
                        "doer_of_things"
                    ]
                },
                "affirmation": {
                    "type": "string",
                    "description": "'I am' statement and description of this identity"
                }
            },
            "required": ["name", "category", "affirmation"],
            "additionalProperties": False,
        }
    }
}

add_refined_identity_function: FunctionTool = {
    "type": "function",
    "name": "add_refined_identity",
    "function": {
        "name": "add_refined_identity",
        "description": "Add a confirmed identity to the refined list during the refinement phase. This should be used when the user confirms interest in a specific identity that will be one of their final three.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the identity (e.g., 'Creative Visionary')"
                },
                "category": {
                    "type": "string",
                    "description": "The category this identity belongs to",
                    "enum": [
                        "passions_and_talents",
                        "maker_of_money",
                        "keeper_of_money",
                        "spiritual",
                        "personal_appearance", 
                        "physical_expression",
                        "familial_relations",
                        "romantic_relation",
                        "doer_of_things"
                    ]
                },
                "affirmation": {
                    "type": "string",
                    "description": "'I am' statement and description of this identity"
                },
                "visualization": {
                    "type": "object",
                    "description": "Optional visualization details for this identity",
                    "properties": {
                        "setting": {
                            "type": "string",
                            "description": "The setting or environment for visualization"
                        },
                        "appearance": {
                            "type": "string",
                            "description": "How the person appears in this identity"
                        },
                        "energy": {
                            "type": "string",
                            "description": "The energy or feeling of this identity"
                        }
                    }
                }
            },
            "required": ["name", "category", "affirmation"],
            "additionalProperties": False,
        }
    }
}

set_focus_identity_function: FunctionTool = {
    "type": "function",
    "name": "set_focus_identity",
    "function": {
        "name": "set_focus_identity",
        "description": "Set a specific identity as the current focus for visualization. This should be used during the visualization phase to decide which identity to visualize next.",
        "parameters": {
            "type": "object",
            "properties": {
                "identity_name": {
                    "type": "string",
                    "description": "The name of the identity to set as focus"
                }
            },
            "required": ["identity_name"],
            "additionalProperties": False,
        }
    }
}

mark_identity_visualized_function: FunctionTool = {
    "type": "function",
    "name": "mark_identity_visualized",
    "function": {
        "name": "mark_identity_visualized",
        "description": "Mark the current focus identity as visualized. This should be used after completing a visualization exercise for an identity.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }
    }
}

mark_introduction_completed_function: FunctionTool = {
    "type": "function",
    "name": "mark_introduction_completed",
    "function": {
        "name": "mark_introduction_completed",
        "description": "Mark the introduction phase as completed to progress to identity brainstorming. This should be used when you've built sufficient rapport and are ready to start exploring identities.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }
    }
}

transition_to_next_state_function: FunctionTool = {
    "type": "function",
    "name": "transition_to_next_state",
    "function": {
        "name": "transition_to_next_state",
        "description": "Force a transition to the next state in the coaching flow. Use this only when all conditions for state transition are met.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_state": {
                    "type": "string",
                    "description": "The target state to transition to",
                    "enum": [
                        "introduction",
                        "identity_brainstorming",
                        "identity_refinement", 
                        "identity_visualization"
                    ]
                }
            },
            "required": ["target_state"],
            "additionalProperties": False,
        }
    }
}

get_coaching_state_function: FunctionTool = {
    "type": "function",
    "name": "get_coaching_state",
    "function": {
        "name": "get_coaching_state",
        "description": "Get the current coaching state and relevant metrics. Use this to check progress and guide the conversation appropriately.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }
    }
}

# Combined list of all function tools
coach_functions = [
    add_draft_identity_function,
    add_refined_identity_function,
    set_focus_identity_function,
    mark_identity_visualized_function,
    mark_introduction_completed_function,
    transition_to_next_state_function,
    get_coaching_state_function
] ] 