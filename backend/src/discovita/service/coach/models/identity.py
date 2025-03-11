"""Identity models for coaching service."""

from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field

class IdentityCategory(str, Enum):
    """Categories of identity in the coaching system."""
    PASSIONS = "passions_and_talents"
    MONEY_MAKER = "maker_of_money" 
    MONEY_KEEPER = "keeper_of_money"
    SPIRITUAL = "spiritual"
    APPEARANCE = "personal_appearance"
    HEALTH = "physical_expression"
    FAMILY = "familial_relations"
    ROMANTIC = "romantic_relation"
    ACTION = "doer_of_things"

class Identity(BaseModel):
    """Identity model representing a client's chosen identity."""
    category: IdentityCategory = Field(..., description="Category this identity belongs to")
    name: str = Field(..., description="Name of the identity (e.g. 'Creative Visionary')")
    affirmation: str = Field(..., description="'I am' statement and description")
    visualization: Optional[Dict] = Field(None, description="Visual representation details")
