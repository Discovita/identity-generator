"""OpenAI models package."""

from typing import Union

# Import directly from OpenAI instead of our custom implementation
from openai.types.responses import (
    ToolChoiceFunction,
    ToolChoiceOptions,
    ToolChoiceTypes,
)

from .chat_models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompletionRequest,
    ContentFilter,
    SafeChatRequest,
    VisionRequest,
)
from .errors import OpenAIError
from .image_models import (
    GeneratedImage,
    ImageGenerationRequest,
    ImageResponse,
    OpenAIMode,
    SafeImageResponse,
)
from .llm_response import LLMResponseModel
from .responses import (
    FunctionParameter,
    FunctionParameters,
    FunctionTool,
    OutputText,
    ResponseFunctionToolCall,
    ResponseInput,
    ResponsesMessage,
    ResponsesOutput,
    ResponsesRequest,
    ResponsesResponse,
    parse_function_call_arguments,
)

# Define ToolChoice as OpenAI's type
ToolChoice = Union[str, dict, ToolChoiceOptions, ToolChoiceTypes, ToolChoiceFunction]

__all__ = [
    # LLM Response
    "LLMResponseModel",
    # Image Models
    "ImageResponse",
    "SafeImageResponse",
    "OpenAIMode",
    "ImageGenerationRequest",
    "GeneratedImage",
    # Chat Models
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ContentFilter",
    "VisionRequest",
    "CompletionRequest",
    "SafeChatRequest",
    # Error Models
    "OpenAIError",
    # Responses API Models
    "ResponsesMessage",
    "ResponsesRequest",
    "ResponsesResponse",
    "ResponseFunctionToolCall",
    "FunctionTool",
    "FunctionParameter",
    "FunctionParameters",
    "OutputText",
    "ResponsesInput",
    "ResponsesOutput",
    "parse_function_call_arguments",
    # Tool Choice Models from OpenAI
    "ToolChoice",
    "ToolChoiceOptions",
    "ToolChoiceTypes",
    "ToolChoiceFunction",
]
