"""Common types and utilities for OpenAI Responses API operations."""

from typing import Dict, Any, List, Callable, Awaitable, Union, Optional
from pydantic import BaseModel
from openai.types.responses import FunctionTool
from discovita.service.openai.models import ResponsesMessage, ToolChoice

class ResponseInput(BaseModel):
    """Input for response operations."""
    messages: List[ResponsesMessage]

    @classmethod
    def from_str(cls, text: str) -> "ResponseInput":
        """Create input from a string."""
        return cls(messages=[ResponsesMessage(role="user", content=text)])

    @classmethod
    def from_messages(cls, messages: List[ResponsesMessage]) -> "ResponseInput":
        """Create input from a list of ResponsesMessage objects."""
        return cls(messages=messages)

    @classmethod
    def from_dict_list(cls, messages: List[Dict[str, Any]]) -> "ResponseInput":
        """Create input from a list of message dictionaries."""
        return cls(messages=[ResponsesMessage(**msg) for msg in messages])

class ResponseTools(BaseModel):
    """Tools configuration for response operations."""
    tools: List[Dict[str, Any]]
    tool_choice: Optional[ToolChoice] = None

class ResponseFunctionDefs(BaseModel):
    """Function definitions for function calling operations."""
    functions: List[Union[Dict[str, Any], FunctionTool]]

class ResponseFunctionHandlers(BaseModel):
    """Function handlers for function calling operations."""
    handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]]

class ResponseFunctionOutputs(BaseModel):
    """Function outputs for function result operations."""
    outputs: Union[Dict[str, Any], List[Dict[str, Any]]]
