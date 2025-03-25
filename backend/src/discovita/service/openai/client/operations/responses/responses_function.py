"""OpenAI Responses API function calling operations."""

import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from openai.types.responses import Response, FunctionTool
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall

from discovita.service.openai.models import ToolChoice
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
    tools = [
        func.model_dump() if isinstance(func, FunctionTool) else func 
        for func in functions.functions
    ]
    
    tools_config = ResponseTools(
        tools=tools,
        tool_choice=ToolChoice.auto()  # Default to auto for function calling
    )
    
    return await create_response(
        client=client,
        input_data=input_data,
        model=model,
        tools=tools_config,
        store=store,
        previous_response_id=previous_response_id
    )

async def handle_function_call_response(
    response: Response,
    function_handlers: ResponseFunctionHandlers
) -> List[Dict[str, str]]:
    """Handle a function call response from the OpenAI Responses API."""
    outputs = []
    
    for output_item in response.output:
        if isinstance(output_item, ResponseFunctionToolCall):
            function_name = output_item.name
            arguments = json.loads(output_item.arguments)
            call_id = output_item.call_id
            
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
    has_function_calls = any(
        isinstance(output_item, ResponseFunctionToolCall) 
        for output_item in response.output
    )
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
    return await submit_results(
        client=client,
        input_data=input_data,
        function_outputs=ResponseFunctionOutputs(outputs=outputs),
        tools=ResponseTools(tools=[
            func.model_dump() if isinstance(func, FunctionTool) else func 
            for func in functions.functions
        ]),
        model=model,
        store=store,
        previous_response_id=response.id
    )
