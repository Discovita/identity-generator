"""OpenAI function definitions for coach actions."""

from typing import List

def get_available_actions() -> List[dict]:
    """Get available actions as OpenAI function definitions."""
    return [
        {
            "name": "create_identity",
            "description": "Create a new identity during brainstorming",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the identity"
                    }
                },
                "required": ["description"]
            }
        },
        {
            "name": "update_identity",
            "description": "Update an identity during refinement",
            "parameters": {
                "type": "object", 
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "ID of identity to update"
                    },
                    "description": {
                        "type": "string",
                        "description": "Updated description"
                    }
                },
                "required": ["id", "description"]
            }
        },
        {
            "name": "accept_identity",
            "description": "Mark an identity as accepted",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "ID of identity to accept"
                    }
                },
                "required": ["id"]
            }
        },
        {
            "name": "complete_introduction",
            "description": "Mark the introduction phase as complete",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "transition_state",
            "description": "Request a state transition",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_state": {
                        "type": "string",
                        "enum": ["introduction", "identity_brainstorming", "identity_refinement"],
                        "description": "State to transition to"
                    }
                },
                "required": ["to_state"]
            }
        }
    ]
