"""In-memory implementation of state repository."""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from copy import deepcopy

from discovita.db.repository.base import Repository
from discovita.db.domain.state import State

class InMemoryStateRepository(Repository[State, Tuple[str, str]]):
    """In-memory implementation of state repository."""
    
    def __init__(self):
        # Store states by (user_id, session_id)
        self.states: Dict[Tuple[str, str], State] = {}
    
    async def get(self, key: Tuple[str, str]) -> Optional[State]:
        """Get a state by user_id and session_id."""
        return deepcopy(self.states.get(key))
    
    async def get_all(self, **filters: Dict[str, Any]) -> List[State]:
        """Get all states matching the filters."""
        result = []
        for state in self.states.values():
            match = True
            for key, value in filters.items():
                if getattr(state, key, None) != value:
                    match = False
                    break
            if match:
                result.append(deepcopy(state))
        return result
    
    async def save(self, state: State) -> State:
        """Save a state."""
        # Set timestamps
        now = datetime.utcnow()
        if not state.created_at:
            state.created_at = now
        state.updated_at = now
        
        # Store a copy
        self.states[state.key] = deepcopy(state)
        return deepcopy(state)
    
    async def delete(self, key: Tuple[str, str]) -> None:
        """Delete a state by user_id and session_id."""
        if key in self.states:
            del self.states[key]
    
    async def update(self, key: Tuple[str, str], values: Dict[str, Any]) -> None:
        """Update specific fields in a state."""
        if key in self.states:
            state = self.states[key]
            for field, value in values.items():
                setattr(state, field, value)
            state.updated_at = datetime.utcnow()
