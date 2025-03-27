"""
Core functionality for the OpenAI Helper module.

This module contains the main OpenAIClient class and related core components.
"""

from .base import OpenAIClient
from .chat_completion import create_chat_completion
from .completion_handlers import (
    handle_chat_completion,
    process_chat_completion_response,
)
from .error_handlers import handle_token_parameter_error
from .structured_completion import create_structured_chat_completion

__all__ = [
    "OpenAIClient",
    "create_chat_completion",
    "create_structured_chat_completion",
    "handle_chat_completion",
    "process_chat_completion_response",
    "handle_token_parameter_error",
]
