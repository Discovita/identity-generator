"""OpenAI API operations package."""

from discovita.service.openai.client.operations.chat import (
    get_completion,
    get_structured_completion,
)
from discovita.service.openai.client.operations.image_generation import generate_image
from discovita.service.openai.client.operations.responses.responses import (
    StructuredResponseResult,
    get_response,
)
from discovita.service.openai.client.operations.safe_image_generation import (
    safe_generate_image,
)
from discovita.service.openai.client.operations.vision import describe_image_with_vision

__all__ = [
    "get_completion",
    "get_structured_completion",
    "generate_image",
    "safe_generate_image",
    "describe_image_with_vision",
    "get_response",
    "StructuredResponseResult",
]
