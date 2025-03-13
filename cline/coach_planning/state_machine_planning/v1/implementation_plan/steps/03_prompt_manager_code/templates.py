from typing import Dict, Any, List, Set, Optional
from pydantic import BaseModel, Field
from discovita.service.coach.models import CoachingState, ActionType

class Example(BaseModel):
    """Example conversation for a prompt."""
    user: str = Field(..., description="User message")
    coach: str = Field(..., description="Coach response")
    description: Optional[str] = Field(None, description="Description of the example")

class PromptTemplate(BaseModel):
    """Template for state-specific prompts."""
    state: CoachingState = Field(..., description="The coaching state this template is for")
    template: str = Field(..., description="Prompt template with placeholders")
    required_context_keys: List[str] = Field(..., description="Required keys in the context")
    examples: List[Example] = Field(default_factory=list, description="Example conversations")
    counter_examples: List[Example] = Field(default_factory=list, description="Counter-examples")
    allowed_actions: Set[ActionType] = Field(default_factory=set, description="Allowed actions in this state")
