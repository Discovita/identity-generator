"""OpenAI Responses API client methods."""

from typing import Any, Awaitable, Callable, Dict, List, Optional, Type, TypeVar, Union

from discovita.service.openai.client.operations.responses.responses import (
    ResponseInput,
    StructuredResponseResult,
    get_response,
)
from discovita.service.openai.models import ToolChoice
from discovita.service.openai.models.llm_response import LLMResponseModel
from openai.types.responses import Response, Tool

T = TypeVar("T", bound=LLMResponseModel)


# This method will be mixed into the OpenAIClient class
async def get_response_with_responses(
    self,
    input_data: ResponseInput,
    model: str = "gpt-4o",
    response_model: Optional[Type[T]] = None,
    schema_name: Optional[str] = None,
    tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
    tool_choice: Optional[ToolChoice] = None,
    handlers: Optional[Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]]] = None,
    auto_handle_functions: bool = True,
    store: bool = True,
    previous_response_id: Optional[str] = None,
) -> Union[Response, StructuredResponseResult[T]]:
    """Get a response from the OpenAI Responses API.

    This unified method handles basic responses, structured outputs, and function calling
    all in one place. The behavior changes based on which parameters you provide:

    - Basic response: Provide only input_data (and optionally tools/tool_choice)
    - Structured output: Provide response_model (and optionally schema_name)
    - Function calling: Provide tools and handlers

    Args:
        input_data: Input data as a ResponseInput object
        model: The model to use (default: "gpt-4o")
        response_model: Optional Pydantic model to parse the response into
        schema_name: Optional name for the schema (defaults to model name)
        tools: Optional list of tools to use
        tool_choice: Optional specification for which tool to use
        handlers: Optional dictionary mapping function names to handler functions
        auto_handle_functions: Whether to automatically handle function calls (default: True)
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation

    Returns:
        If response_model is provided: StructuredResponseResult with parsed model
        Otherwise: Raw Response object from OpenAI
    """
    return await get_response(
        client=self.client,
        input_data=input_data,
        model=model,
        response_model=response_model,
        schema_name=schema_name,
        tools=tools,
        tool_choice=tool_choice,
        handlers=handlers,
        auto_handle_functions=auto_handle_functions,
        store=store,
        previous_response_id=previous_response_id,
    )
