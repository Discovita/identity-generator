"""Tool choice models for OpenAI API."""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolChoiceMode(str, Enum):
    """Enum for tool choice modes."""
    NONE = "none"
    AUTO = "auto"

class SpecificToolChoice(BaseModel):
    """Model for specifying a particular tool to use."""
    type: str = "function"  # Currently OpenAI only supports "function" type
    function: Dict[str, Any]  # Function name and arguments

class ToolChoice(BaseModel):
    """Model for tool choice configuration."""
    mode: ToolChoiceMode = ToolChoiceMode.AUTO
    specific_tool: Optional[SpecificToolChoice] = None

    @classmethod
    def none(cls) -> "ToolChoice":
        """Create a ToolChoice that disables tool usage."""
        return cls(mode=ToolChoiceMode.NONE)

    @classmethod
    def auto(cls) -> "ToolChoice":
        """Create a ToolChoice that allows automatic tool selection."""
        return cls(mode=ToolChoiceMode.AUTO)

    @classmethod
    def specific(cls, function_name: str, **function_args) -> "ToolChoice":
        """Create a ToolChoice that specifies a particular tool to use."""
        return cls(
            mode=ToolChoiceMode.AUTO,  # OpenAI requires "auto" when specifying a tool
            specific_tool=SpecificToolChoice(
                function={"name": function_name, **function_args}
            )
        )
