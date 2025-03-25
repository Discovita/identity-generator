"""State record model for persistence layer."""

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from discovita.db.models.base import Base, TimestampMixin
from discovita.db.models.constants import (
    ID, USER_ID, SESSION_ID, STATE_DATA,
    STATES_TABLE, USERS_TABLE, USER
)
from discovita.service.coach.models.state import CoachingState

class StateRecord(Base, TimestampMixin):
    """Model for storing state information."""
    __tablename__ = STATES_TABLE
    
    id = Column(ID, Integer, primary_key=True, autoincrement=True)
    user_id = Column(USER_ID, String(36), ForeignKey(f"{USERS_TABLE}.{ID}"), nullable=False)
    session_id = Column(SESSION_ID, String(36), nullable=False)
    state_data = Column(STATE_DATA, JSON, nullable=False)  # Serialized CoachingState
    
    # Ensure user_id + session_id is unique
    __table_args__ = (
        UniqueConstraint(USER_ID, SESSION_ID, name="uq_state_user_session"),
    )
    
    # Relationship to user
    user = relationship(USER, back_populates=STATES_TABLE)
    
    def get_state(self) -> CoachingState:
        """Get the deserialized state object."""
        return CoachingState.model_validate(self.state_data)
    
    def set_state(self, state: CoachingState) -> None:
        """Set the state from a CoachingState object."""
        self.state_data = state.model_dump()
