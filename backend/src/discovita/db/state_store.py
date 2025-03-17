"""State persistence for the coaching state machine."""

from typing import Optional, Dict, Any
from discovita.service.coach.models import CoachContext, CoachingState

class StateStore:
    """Interface for state persistence."""
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user."""
        raise NotImplementedError("Subclasses must implement load_context")
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user."""
        raise NotImplementedError("Subclasses must implement save_context")

class InMemoryStateStore(StateStore):
    """In-memory implementation of state persistence."""
    
    def __init__(self):
        raise NotImplementedError("InMemoryStateStore will be implemented in Step 7: Persistence Layer")
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user from memory."""
        raise NotImplementedError("InMemoryStateStore will be implemented in Step 7: Persistence Layer")
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user to memory."""
        raise NotImplementedError("InMemoryStateStore will be implemented in Step 7: Persistence Layer")
