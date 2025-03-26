"""OpenAI Responses API operations.

This module provides a unified interface for working with the OpenAI Responses API,
including basic response generation, structured outputs, and function calling.
"""

import json
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    LLMResponseModel,
    ResponseInput,
    ResponsesMessage,
    ResponsesRequest,
    ToolChoice,
)
from openai import AsyncOpenAI
from openai.types.responses import Response, Tool
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from pydantic import BaseModel

# Response result types
T = TypeVar("T", bound=LLMResponseModel)


class StructuredResponseResult(BaseModel, Generic[T]):
    """Result of a structured response operation."""

    response: Response
    parsed: Optional[T] = None
    is_valid: bool = False
    error: Optional[str] = None


# Main unified response function
async def get_response(
    client: AsyncOpenAI,
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

    This unified function handles basic responses, structured outputs, and function calling
    all in one place. The behavior changes based on which parameters you provide:

    - Basic response: Provide only input_data (and optionally tools/tool_choice)
    - Structured output: Provide response_model
    - Function calling: Provide tools and handlers

    Args:
        client: OpenAI client instance
        input_data: Input data as a ResponseInput object
        model: The model to use (default: "gpt-4o")
        response_model: Optional Pydantic model to parse the response into
        schema_name: Optional name for the schema (defaults to model name)
        tools: Optional list of tools to use (must be explicitly provided)
        tool_choice: Optional specification for which tool to use
        handlers: Optional dictionary mapping function names to handler functions
        auto_handle_functions: Whether to automatically handle function calls (default: True)
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation

    Returns:
        If response_model is provided: StructuredResponseResult with parsed model
        Otherwise: Raw Response object from OpenAI
    """
    # Create and send the request
    request = ResponsesRequest(
        model=model,
        input=input_data.messages,
        tools=tools,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id,
    )

    logging.log_request("responses_create", **request.model_dump())
    response = await client.responses.create(**request.model_dump())
    logging.log_response("responses_create", response)

    # Handle function calls if handlers are provided and auto_handle_functions is True
    if (
        auto_handle_functions
        and handlers
        and any(
            isinstance(output_item, ResponseFunctionToolCall)
            for output_item in response.output
        )
    ):
        # Process function calls
        outputs = []
        for output_item in response.output:
            if isinstance(output_item, ResponseFunctionToolCall):
                function_name = output_item.name
                arguments = json.loads(output_item.arguments)
                call_id = output_item.call_id

                handler = handlers.get(function_name)
                if not handler:
                    raise ValueError(f"No handler found for function '{function_name}'")

                result = await handler(arguments)
                outputs.append({"tool_call_id": call_id, "output": str(result)})

        if outputs:
            # If we have outputs, submit them back to continue the conversation
            messages = input_data.messages.copy()
            for output in outputs:
                messages.append(
                    ResponsesMessage(
                        role="assistant",
                        content=[
                            {
                                "type": "function_call_output",
                                "call_id": output["tool_call_id"],
                                "output": output["output"],
                            }
                        ],
                    )
                )

            # Create new request with function outputs
            request_params = {
                "model": model,
                "input": messages,
                "tools": tools,
                "tool_choice": tool_choice,
                "store": store,
                "previous_response_id": response.id,
            }
            request_params = {k: v for k, v in request_params.items() if v is not None}

            logging.log_request("responses_create", **request_params)
            response = await client.responses.create(**request_params)
            logging.log_response("responses_create", response)

    # If response_model is provided, parse the response
    if response_model:
        result = StructuredResponseResult(response=response)
        try:
            # Check if the response is a function call first
            if any(
                isinstance(output_item, ResponseFunctionToolCall)
                for output_item in response.output
            ):
                # For function calls, extract the arguments as the data
                func_call = next(
                    (
                        o
                        for o in response.output
                        if isinstance(o, ResponseFunctionToolCall)
                    ),
                    None,
                )
                if func_call:
                    # Parse the arguments and create data structure
                    arguments = (
                        json.loads(func_call.arguments) if func_call.arguments else {}
                    )
                    # Create response data with default message and arguments as actions
                    data = {"message": "I'm thinking about this...", "actions": []}
                    # Merge any provided arguments
                    data.update(arguments)

                    # If message is still empty after merging, provide a fallback message
                    if not data.get("message"):
                        data["message"] = (
                            "I need more information to proceed. Could you provide additional details?"
                        )

                    # Parse into model
                    result.parsed = response_model.model_validate(data)
                    result.is_valid = True
                    return result

            # Otherwise, handle text response as before
            assert response.output, "Response must have output"
            assert len(response.output) > 0, "Response output cannot be empty"
            assert hasattr(
                response.output[0], "content"
            ), "Response output must have content"
            assert (
                len(response.output[0].content) > 0
            ), "Response content cannot be empty"
            assert hasattr(
                response.output[0].content[0], "text"
            ), "Response content must have text"

            # Extract message
            message = response.output[0].content[0].text

            # Create response data
            data = {"message": message, "actions": []}

            # Parse into model
            result.parsed = response_model.model_validate(data)
            result.is_valid = True
        except Exception as e:
            result.error = str(e)

        return result

    # Return raw response for basic usage
    return response
