"""OpenAI Responses API client methods."""

from typing import TypeVar, Type, Optional
from openai.types.chat import ChatCompletion as Response
from discovita.service.openai.models.llm_response import LLMResponseModel
from discovita.service.openai.client.operations.responses.responses import (
    ResponseInput,
    ResponseTools,
    ResponseFunctionDefs,
    ResponseFunctionHandlers,
    ResponseFunctionOutputs
)
from discovita.service.openai.client.operations.responses import (
    responses_basic,
    responses_function,
    responses_function_results,
    responses_structured
)
from discovita.service.openai.client.operations.responses.responses_structured import (
    StructuredResponseResult
)

T = TypeVar('T', bound=LLMResponseModel)

# These methods will be mixed into the OpenAIClient class
async def create_response_with_responses(self, input_data: ResponseInput, **kwargs) -> Response:
    """Create a response using the OpenAI Responses API."""
    return await responses_basic.create_response(self.client, input_data, **kwargs)

async def call_function_with_responses(
    self, 
    input_data: ResponseInput,
    functions: ResponseFunctionDefs,
    **kwargs
) -> Response:
    """Call a function using the OpenAI Responses API."""
    return await responses_function.call_function(self.client, input_data, functions, **kwargs)

async def call_functions_with_responses(
    self,
    input_data: ResponseInput,
    functions: ResponseFunctionDefs,
    function_handlers: ResponseFunctionHandlers,
    **kwargs
) -> Response:
    """Call functions with the model and handle the responses automatically."""
    return await responses_function.call_functions(
        self.client, input_data, functions, function_handlers, **kwargs
    )

async def submit_function_results_with_responses(
    self,
    input_data: ResponseInput,
    function_outputs: ResponseFunctionOutputs,
    tools: Optional[ResponseTools] = None,
    **kwargs
) -> Response:
    """Submit function results to the OpenAI Responses API."""
    return await responses_function_results.submit_results(
        self.client, input_data, function_outputs, tools, **kwargs
    )

async def get_structured_response_with_responses(
    self,
    input_data: ResponseInput,
    response_model: Type[T],
    **kwargs
) -> StructuredResponseResult[T]:
    """Get a structured response using the OpenAI Responses API."""
    return await responses_structured.get_response(
        self.client, input_data, response_model, **kwargs
    )
