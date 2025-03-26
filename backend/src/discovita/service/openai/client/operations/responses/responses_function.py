"""OpenAI Responses API function calling operations."""

import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion as Response, ChatCompletionToolParam as FunctionTool
from openai.types.chat import ChatCompletionMessageToolCall as ResponseFunctionToolCall

from discovita.service.openai.models import ToolChoice
from discovita.service.openai.client import logging
from .responses_basic import create_response
from .responses import (
    ResponseInput,
    ResponseTools,
    ResponseFunctionDefs,
    ResponseFunctionHandlers,
    ResponseFunctionOutputs
)

async def call_function(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    functions: ResponseFunctionDefs,
    model: str = "gpt-4o",
    store: bool = True,
    previous_response_id: Optional[str] = None
) -> Response:
    """Call a function using the OpenAI Responses API."""
    # Convert function definitions to tools format
    tools_list = []
    for func in functions.functions:
        # Add the function to the tools list
        tools_list.append(func)
    
    tools_config = ResponseTools(
        tools=tools_list,
        tool_choice=ToolChoice.auto()  # Default to auto for function calling
    )
    
    # Create request parameters
    request_params = {
        "model": model,
        "messages": input_data.messages,
        "store": store,
    }
    
    if previous_response_id:
        request_params["previous_response_id"] = previous_response_id
    
    # Add tools configuration
    request_params["tools"] = tools_config.tools
    if tools_config.tool_choice:
        request_params["tool_choice"] = tools_config.tool_choice
    
    # Log and send request
    logging.log_request("chat.completions.create", **request_params)
    response = await client.chat.completions.create(**request_params)
    logging.log_response("chat.completions.create", response)
    
    return response

async def handle_function_call_response(
    response: Response,
    function_handlers: ResponseFunctionHandlers
) -> List[Dict[str, str]]:
    """Handle a function call response from the OpenAI Responses API."""
    outputs = []
    
    # Extract tool calls from the response
    tool_calls = []
    for choice in response.choices:
        if choice.message and choice.message.tool_calls:
            tool_calls.extend(choice.message.tool_calls)
    
    for tool_call in tool_calls:
        if isinstance(tool_call, ResponseFunctionToolCall):
            # Extract function details from the tool call
            # Access the function object directly
            function = tool_call.function
            assert hasattr(function, 'name'), "Function must have a name attribute"
            function_name = function.name
            
            # Get arguments and parse them
            assert hasattr(function, 'arguments'), "Function must have an arguments attribute"
            arguments = json.loads(function.arguments)
            call_id = tool_call.id
            
            handler = function_handlers.handlers.get(function_name)
            if not handler:
                raise ValueError(f"No handler found for function '{function_name}'")
            
            result = await handler(arguments)
            outputs.append({
                "tool_call_id": call_id,
                "output": str(result)
            })
    
    return outputs

async def call_functions(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    functions: ResponseFunctionDefs,
    function_handlers: ResponseFunctionHandlers,
    model: str = "gpt-4o",
    store: bool = True,
    previous_response_id: Optional[str] = None
) -> Response:
    """Call functions and handle responses automatically."""
    # Call the functions
    response = await call_function(
        client=client,
        input_data=input_data,
        functions=functions,
        model=model,
        store=store,
        previous_response_id=previous_response_id
    )
    
    # Check if there are function calls in the response
    has_function_calls = False
    for choice in response.choices:
        if choice.message and choice.message.tool_calls:
            has_function_calls = True
            break
    
    if not has_function_calls:
        return response
    
    # Handle the function calls
    outputs = await handle_function_call_response(
        response=response,
        function_handlers=function_handlers
    )
    
    # Import here to avoid circular dependency
    from .responses_function_results import submit_results
    
    # Submit the function results
    tools_list = []
    for func in functions.functions:
        # Add the function to the tools list
        tools_list.append(func)
    
    return await submit_results(
        client=client,
        input_data=input_data,
        function_outputs=ResponseFunctionOutputs(outputs=outputs),
        tools=ResponseTools(tools=tools_list),
        model=model,
        store=store,
        previous_response_id=response.id
    )
