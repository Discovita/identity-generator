"""State persistence for the coaching state machine."""

from typing import Optional, Dict, Any, List
import json
import uuid
from datetime import datetime

from discovita.service.coach.models import CoachContext, CoachingState, ChatMessage, UserProfile, Identity, IdentityCategory
from discovita.db.interface import DatabaseInterface
from discovita.db.models.context import ContextRecord
from discovita.db.models.state import StateRecord
from discovita.db.models.identity import IdentityRecord

class StateStore:
    """Interface for state persistence."""
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user."""
        raise NotImplementedError("Subclasses must implement load_context")
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user."""
        raise NotImplementedError("Subclasses must implement save_context")

class DatabaseStateStore(StateStore):
    """Database implementation of state persistence."""
    
    def __init__(self, db: DatabaseInterface):
        """Initialize with a database implementation."""
        self.db = db
    
    async def load_context(self, user_id: str, session_id: str = "default") -> Optional[CoachContext]:
        """Load context for a user from the database."""
        # Get state record
        state_record = await self.db.get_state(user_id, session_id)
        if not state_record:
            return None
        
        # Get context record
        context_record = await self.db.get_context(user_id, session_id)
        if not context_record:
            return None
        
        # Get identities
        identity_records = await self.db.get_identities(user_id)
        
        # Convert to CoachContext
        identities = []
        for record in identity_records:
            try:
                category = IdentityCategory(record.category)
                identities.append(Identity(
                    category=category,
                    name=record.name,
                    affirmation=record.description,
                    visualization=None
                ))
            except ValueError:
                # Skip invalid identity categories
                pass
        
        # Create user profile
        user_profile = UserProfile(
            user_id=user_id,
            identities=identities,
            current_focus=None  # Will be set from metadata if available
        )
        
        # Convert messages
        messages = []
        for msg_data in context_record.messages:
            messages.append(ChatMessage(
                role=msg_data["role"],
                content=msg_data["content"]
            ))
        
        # Create context
        context = CoachContext(
            user_id=user_id,
            current_state=CoachingState(state_record.state),
            conversation_history=messages,
            consolidated_summary=context_record.user_data.get("consolidated_summary", ""),
            user_profile=user_profile,
            metadata=context_record.user_data.get("metadata", {})
        )
        
        # Set current focus if available
        if "current_focus" in context_record.user_data:
            try:
                focus = IdentityCategory(context_record.user_data["current_focus"])
                context.user_profile.current_focus = focus
            except (ValueError, KeyError):
                pass
        
        return context
    
    async def save_context(self, context: CoachContext, session_id: str = "default") -> None:
        """Save context for a user to the database."""
        # Save state
        state_record = StateRecord(
            user_id=context.user_id,
            session_id=session_id,
            state=context.current_state.value
        )
        await self.db.save_state(state_record)
        
        # Prepare messages
        messages = []
        for msg in context.conversation_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Prepare user data
        user_data = {
            "consolidated_summary": context.consolidated_summary,
            "metadata": context.metadata
        }
        
        # Add current focus if available
        if context.user_profile and context.user_profile.current_focus:
            user_data["current_focus"] = context.user_profile.current_focus.value
        
        # Save context
        context_record = ContextRecord(
            user_id=context.user_id,
            session_id=session_id,
            messages=messages,
            user_data=user_data
        )
        await self.db.save_context(context_record)
        
        # Save identities
        if context.user_profile and context.user_profile.identities:
            # Get existing identities
            existing_identities = await self.db.get_identities(context.user_id)
            existing_names = {record.name for record in existing_identities}
            
            # Save new identities
            for identity in context.user_profile.identities:
                if identity.name not in existing_names:
                    await self.db.save_identity(
                        user_id=context.user_id,
                        identity=identity.name,
                        category=identity.category.value,
                        description=identity.affirmation
                    )

class InMemoryStateStore(StateStore):
    """In-memory implementation of state persistence."""
    
    def __init__(self, db: Optional[DatabaseInterface] = None):
        """Initialize with an optional database for persistence."""
        self.db_store = DatabaseStateStore(db) if db else None
        self.contexts: Dict[str, CoachContext] = {}
    
    async def load_context(self, user_id: str, session_id: str = "default") -> Optional[CoachContext]:
        """Load context for a user from memory."""
        # Try memory first
        if user_id in self.contexts:
            return self.contexts[user_id]
        
        # Try database if available
        if self.db_store:
            context = await self.db_store.load_context(user_id, session_id)
            if context:
                self.contexts[user_id] = context
                return context
        
        return None
    
    async def save_context(self, context: CoachContext, session_id: str = "default") -> None:
        """Save context for a user to memory."""
        self.contexts[context.user_id] = context
        
        # Save to database if available
        if self.db_store:
            await self.db_store.save_context(context, session_id)
