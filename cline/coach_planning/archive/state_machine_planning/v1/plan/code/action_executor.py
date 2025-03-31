from typing import Dict, Any, List, Callable
from dataclasses import dataclass
import json
import re

@dataclass
class Action:
    name: str
    handler: Callable[[Dict[str, Any]], None]
    description: str

class ActionExecutor:
    def __init__(self, context_manager, state_machine, db_service):
        self.context_manager = context_manager
        self.state_machine = state_machine
        self.db_service = db_service
        self.actions: Dict[str, Action] = {}
        self._register_actions()
    
    def _register_actions(self) -> None:
        """Register all available actions with their handlers."""
        self.register_action(
            "SAVE_USER_INFO",
            self._handle_save_user_info,
            "Save or update information about the user"
        )
        
        self.register_action(
            "SAVE_IDENTITY",
            self._handle_save_identity,
            "Save a new identity discovered during coaching"
        )
        
        self.register_action(
            "MARK_INTRODUCTION_COMPLETE",
            self._handle_mark_intro_complete,
            "Mark the introduction phase as complete"
        )
        
        self.register_action(
            "TRANSITION_STATE",
            self._handle_transition_state,
            "Request a state transition if conditions are met"
        )
        
        # Register more actions as needed
    
    def register_action(self, name: str, handler: Callable, description: str) -> None:
        """Register a new action."""
        self.actions[name] = Action(name, handler, description)
    
    def parse_actions_from_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse actions from the LLM response."""
        # Look for actions in a structured format like:
        # [ACTION:SAVE_USER_INFO]{"key": "goals", "value": "User wants to improve work-life balance"}[/ACTION]
        action_pattern = r'\[ACTION:([A-Z_]+)\](.*?)\[/ACTION\]'
        matches = re.findall(action_pattern, response, re.DOTALL)
        
        parsed_actions = []
        for action_name, action_params in matches:
            try:
                params = json.loads(action_params)
                parsed_actions.append({
                    "name": action_name,
                    "params": params
                })
            except json.JSONDecodeError:
                # Log error but continue with other actions
                print(f"Error parsing action parameters: {action_params}")
        
        return parsed_actions
    
    def execute_actions(self, actions: List[Dict[str, Any]]) -> None:
        """Execute a list of parsed actions."""
        for action in actions:
            action_name = action["name"]
            if action_name in self.actions:
                try:
                    self.actions[action_name].handler(action["params"])
                except Exception as e:
                    # Log error but continue with other actions
                    print(f"Error executing action {action_name}: {e}")
            else:
                print(f"Unknown action: {action_name}")
    
    def _handle_save_user_info(self, params: Dict[str, Any]) -> None:
        """Handle saving user information."""
        key = params.get("key")
        value = params.get("value")
        if key and value:
            self.context_manager.update_user_data(key, value)
            self.db_service.update_user_data(key, value)
    
    def _handle_save_identity(self, params: Dict[str, Any]) -> None:
        """Handle saving a new identity."""
        identity = params.get("identity")
        description = params.get("description", "")
        
        if identity:
            identities = self.context_manager.user_data.get("identities", [])
            identities.append({
                "name": identity,
                "description": description,
                "created_at": "current_timestamp"  # Would use actual timestamp
            })
            self.context_manager.update_user_data("identities", identities)
            self.db_service.save_identity(identity, description)
    
    def _handle_mark_intro_complete(self, params: Dict[str, Any]) -> None:
        """Mark the introduction as complete."""
        self.context_manager.update_user_data("introduction_completed", True)
        self.db_service.update_user_data("introduction_completed", True)
    
    def _handle_transition_state(self, params: Dict[str, Any]) -> None:
        """Request a state transition."""
        # The state machine will evaluate if conditions are met
        context = self.context_manager.get_context_for_prompt()
        self.state_machine.transition(context)
