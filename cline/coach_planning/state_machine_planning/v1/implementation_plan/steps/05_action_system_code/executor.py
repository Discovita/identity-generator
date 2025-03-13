from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import json
import re
from uuid import UUID

from .models.action import Action, ActionResult
from .models.state import CoachingState
from .handlers import ActionHandler

class ActionExecutor:
    """Executes actions determined by the coach."""
    
    def __init__(self, context_manager, state_machine, db_service):
        self.context_manager = context_manager
        self.state_machine = state_machine
        self.db_service = db_service
        self.handlers: Dict[str, ActionHandler] = {}
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register all available action handlers."""
        from .handlers import (
            SaveUserInfoHandler,
            SaveIdentityHandler,
            MarkIntroductionCompleteHandler,
            TransitionStateHandler
        )
        
        self.register_handler(SaveUserInfoHandler(self.context_manager, self.db_service))
        self.register_handler(SaveIdentityHandler(self.context_manager, self.db_service))
        self.register_handler(MarkIntroductionCompleteHandler(self.context_manager, self.db_service))
        self.register_handler(TransitionStateHandler(self.context_manager, self.state_machine))
    
    def register_handler(self, handler: ActionHandler) -> None:
        """Register a new action handler."""
        self.handlers[handler.action_name] = handler
    
    def parse_actions_from_response(self, response: str) -> List[Action]:
        """Parse actions from the LLM response."""
        # Look for actions in a structured format like:
        # [ACTION:SAVE_USER_INFO]{"key": "goals", "value": "User wants to improve work-life balance"}[/ACTION]
        action_pattern = r'\[ACTION:([A-Z_]+)\](.*?)\[/ACTION\]'
        matches = re.findall(action_pattern, response, re.DOTALL)
        
        parsed_actions = []
        for action_name, action_params in matches:
            try:
                params = json.loads(action_params)
                parsed_actions.append(Action(
                    name=action_name,
                    params=params
                ))
            except json.JSONDecodeError:
                # Log error but continue with other actions
                print(f"Error parsing action parameters: {action_params}")
        
        return parsed_actions
    
    async def execute_actions(
        self,
        actions: List[Action],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> List[ActionResult]:
        """Execute a list of parsed actions."""
        results = []
        
        for action in actions:
            # Check if action is allowed in current state
            if not self._is_action_allowed(action.name, state):
                results.append(ActionResult(
                    action=action,
                    success=False,
                    message=f"Action {action.name} not allowed in state {state.value}"
                ))
                continue
            
            # Execute action if handler exists
            if action.name in self.handlers:
                try:
                    result = await self.handlers[action.name].handle(
                        params=action.params,
                        user_id=user_id,
                        session_id=session_id,
                        state=state
                    )
                    results.append(result)
                except Exception as e:
                    # Log error but continue with other actions
                    results.append(ActionResult(
                        action=action,
                        success=False,
                        message=f"Error executing action: {str(e)}"
                    ))
            else:
                results.append(ActionResult(
                    action=action,
                    success=False,
                    message=f"Unknown action: {action.name}"
                ))
        
        return results
    
    def _is_action_allowed(self, action_name: str, state: CoachingState) -> bool:
        """Check if an action is allowed in the current state."""
        allowed_actions = self.state_machine.get_available_actions(state)
        return action_name in [action.name for action in allowed_actions]
