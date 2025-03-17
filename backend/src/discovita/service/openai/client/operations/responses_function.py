"""OpenAI Responses API function calling operations.

This module contains operations for function calling with the OpenAI Responses API,
including calling functions and handling function call responses.
"""

from typing import Union, List, Dict, Any, Callable, Awaitable
from openai import AsyncOpenAI
from openai.types.responses import Response, FunctionTool
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
import json
from discovita.service.openai.models import (
    ResponsesMessage,
)

from .responses_basic import create_response

async def call_function(
    client: AsyncOpenAI,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    functions: List[Union[Dict[str, Any], FunctionTool]],
    model: str = "gpt-4o",
    tool_choice: Union[str, Dict[str, Any]] = "auto",
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Call a function using the OpenAI Responses API.
    
    This function sends a request to the OpenAI Responses API with function
    definitions and returns the response, which may include function calls.
    
    Args:
        client: OpenAI client instance
        input_data: Input data, which can be a string or a list of messages
        functions: List of function definitions
        model: The model to use (default: "gpt-4o")
        tool_choice: Control which tool the model uses (default: "auto")
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The response from the OpenAI Responses API
    """
    # Convert function definitions to the format expected by the API
    tools = []
    for func in functions:
        if isinstance(func, FunctionTool):
            tools.append(func.model_dump())
        else:
            tools.append(func)
    
    # Create the response
    return await create_response(
        client=client,
        input_data=input_data,
        model=model,
        tools=tools,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )

async def handle_function_call_response(
    response: Response,
    function_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]]
) -> List[Dict[str, str]]:
    """Handle a function call response from the OpenAI Responses API.
    
    This function processes a response from the OpenAI Responses API that
    contains function calls, executes the functions, and returns the results
    as a list of dictionaries with tool_call_id and output fields.
    
    Args:
        response: Response from the OpenAI Responses API
        function_handlers: Dictionary mapping function names to handler functions
        
    Returns:
        List[Dict[str, str]]: The results of the function calls as dictionaries
                             with tool_call_id and output fields
    """
    outputs = []
    
    # Check if there are function calls in the response
    for output_item in response.output:
        if isinstance(output_item, ResponseFunctionToolCall):
            # Get the function name and arguments
            function_name = output_item.name
            arguments = json.loads(output_item.arguments)
            call_id = output_item.call_id
            
            # Check if we have a handler for this function
            if function_name in function_handlers:
                # Call the function handler
                result = await function_handlers[function_name](arguments)
                
                # Create a function call output as a dictionary
                output = {
                    "tool_call_id": call_id,
                    "output": str(result)
                }
                
                outputs.append(output)
            else:
                raise ValueError(f"No handler found for function '{function_name}'")
    
    return outputs 