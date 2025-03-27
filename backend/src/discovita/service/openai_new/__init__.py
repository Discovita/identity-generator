"""
OpenAI Helper module for interacting with OpenAI's API.

This module provides a simplified interface for making requests to OpenAI's API,
with support for text completions, image inputs, JSON mode, structured outputs,
and streaming responses.

Usage:
    from discovita.service.openai_new import OpenAIClient

    helper = OpenAIClient(api_key="your_api_key", organization="your_org_id")
    response = helper.create_chat_completion(prompt="Hello, world!")

    # You can also access the AIModel enum for model-specific logic
    from discovita.service.openai_new import AIModel

    # Check if a model supports structured outputs
    supports_structured = AIModel.supports_structured_outputs("gpt-4o")

    # Get the appropriate token parameter name for a model
    token_param = AIModel.get_token_param_name("o3-mini")  # Returns "max_completion_tokens"
"""

# Import the main class and enums for backward compatibility
from .core.base import OpenAIClient

# Add the methods to the OpenAIClient class
from .core.chat_completion import create_chat_completion
from .core.structured_completion import create_structured_chat_completion
from .enums import AIModel, AIProvider

# Monkey-patch the methods into the class
OpenAIClient.create_chat_completion = create_chat_completion
OpenAIClient.create_structured_chat_completion = create_structured_chat_completion

__all__ = ["OpenAIClient", "AIModel", "AIProvider"]
