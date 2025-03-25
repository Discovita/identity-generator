"""State domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from discovita.service.coach.models.state import CoachingState

@dataclass
class State:
    """Pure domain model for state information.
    
    This class represents the business object for state, independent of any
    persistence mechanism. It contains only the core business data and logic.
    """
    user_id: str
    session_id: str
    state: CoachingState
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @property
    def key(self) -> tuple[str, str]:
        """Get the unique key for this state.
        
        Returns:
            Tuple of (user_id, session_id) that uniquely identifies this state
        """
        return (self.user_id, self.session_id)
