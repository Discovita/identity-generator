"""OpenAI API operations package."""

from discovita.service.openai.client.operations.chat import (
    get_completion,
    get_structured_completion
)
from discovita.service.openai.client.operations.image_generation import generate_image
from discovita.service.openai.client.operations.safe_image_generation import safe_generate_image
from discovita.service.openai.client.operations.vision import describe_image_with_vision
from discovita.service.openai.client.operations.responses.responses_basic import create_response
from discovita.service.openai.client.operations.responses.responses_function import (
    call_function,
    handle_function_call_response
)
from discovita.service.openai.client.operations.responses.responses_function_results import submit_results
from discovita.service.openai.client.operations.responses.responses_structured import (
    get_response as get_structured_response,
    StructuredResponseResult
)

__all__ = [
    'get_completion',
    'get_structured_completion',
    'generate_image',
    'safe_generate_image',
    'describe_image_with_vision',
    'create_response',
    'call_function',
    'handle_function_call_response',
    'submit_results',
    'get_structured_response',
    'StructuredResponseResult'
]
