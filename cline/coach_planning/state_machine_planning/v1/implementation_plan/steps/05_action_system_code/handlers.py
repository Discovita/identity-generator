from typing import Dict, Any, Protocol, Optional
from abc import ABC, abstractmethod

from .models.action import Action, ActionResult
from .models.state import CoachingState

class ActionHandler(ABC):
    """Base class for action handlers."""
    
    @property
    @abstractmethod
    def action_name(self) -> str:
        """Get the name of the action this handler handles."""
        pass
    
    @abstractmethod
    async def handle(
        self,
        params: Dict[str, Any],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> ActionResult:
        """Handle the action."""
        pass

class SaveUserInfoHandler(ActionHandler):
    """Handler for saving user information."""
    
    def __init__(self, context_manager, db_service):
        self.context_manager = context_manager
        self.db_service = db_service
    
    @property
    def action_name(self) -> str:
        return "SAVE_USER_INFO"
    
    async def handle(
        self,
        params: Dict[str, Any],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> ActionResult:
        """Handle saving user information."""
        key = params.get("key")
        value = params.get("value")
        
        if not key or not value:
            return ActionResult(
                action=Action(name=self.action_name, params=params),
                success=False,
                message="Missing required parameters: key and value"
            )
        
        # Update context
        await self.context_manager.update_user_data(user_id, session_id, key, value)
        
        # Update database
        await self.db_service.update_user_data(user_id, key, value)
        
        return ActionResult(
            action=Action(name=self.action_name, params=params),
            success=True,
            message=f"User info updated: {key}"
        )

class SaveIdentityHandler(ActionHandler):
    """Handler for saving a new identity."""
    
    def __init__(self, context_manager, db_service):
        self.context_manager = context_manager
        self.db_service = db_service
    
    @property
    def action_name(self) -> str:
        return "SAVE_IDENTITY"
    
    async def handle(
        self,
        params: Dict[str, Any],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> ActionResult:
        """Handle saving a new identity."""
        identity = params.get("identity")
        category = params.get("category")
        description = params.get("description", "")
        
        if not identity or not category:
            return ActionResult(
                action=Action(name=self.action_name, params=params),
                success=False,
                message="Missing required parameters: identity and category"
            )
        
        # Update context
        context = await self.context_manager.get_context(user_id, session_id)
        identities = context.user_data.get("identities", [])
        
        new_identity = {
            "name": identity,
            "category": category,
            "description": description,
            "created_at": "current_timestamp"  # Would use actual timestamp
        }
        
        identities.append(new_identity)
        await self.context_manager.update_user_data(user_id, session_id, "identities", identities)
        
        # Update database
        await self.db_service.save_identity(user_id, identity, category, description)
        
        return ActionResult(
            action=Action(name=self.action_name, params=params),
            success=True,
            message=f"Identity saved: {identity}"
        )

class MarkIntroductionCompleteHandler(ActionHandler):
    """Handler for marking the introduction as complete."""
    
    def __init__(self, context_manager, db_service):
        self.context_manager = context_manager
        self.db_service = db_service
    
    @property
    def action_name(self) -> str:
        return "MARK_INTRODUCTION_COMPLETE"
    
    async def handle(
        self,
        params: Dict[str, Any],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> ActionResult:
        """Handle marking the introduction as complete."""
        # Update context
        await self.context_manager.update_user_data(
            user_id, session_id, "introduction_completed", True
        )
        
        # Update database
        await self.db_service.update_user_data(user_id, "introduction_completed", True)
        
        return ActionResult(
            action=Action(name=self.action_name, params=params),
            success=True,
            message="Introduction marked as complete"
        )

class TransitionStateHandler(ActionHandler):
    """Handler for requesting a state transition."""
    
    def __init__(self, context_manager, state_machine):
        self.context_manager = context_manager
        self.state_machine = state_machine
    
    @property
    def action_name(self) -> str:
        return "TRANSITION_STATE"
    
    async def handle(
        self,
        params: Dict[str, Any],
        user_id: str,
        session_id: str,
        state: CoachingState
    ) -> ActionResult:
        """Handle requesting a state transition."""
        target_state = params.get("target_state")
        
        if not target_state:
            return ActionResult(
                action=Action(name=self.action_name, params=params),
                success=False,
                message="Missing required parameter: target_state"
            )
        
        # Get context for transition
        context = await self.context_manager.get_context(user_id, session_id)
        
        # Request transition
        success = await self.state_machine.transition_to(
            user_id=user_id,
            session_id=session_id,
            target_state=target_state,
            context=context
        )
        
        if success:
            return ActionResult(
                action=Action(name=self.action_name, params=params),
                success=True,
                message=f"Transitioned to state: {target_state}"
            )
        else:
            return ActionResult(
                action=Action(name=self.action_name, params=params),
                success=False,
                message=f"Could not transition to state: {target_state}"
            )
