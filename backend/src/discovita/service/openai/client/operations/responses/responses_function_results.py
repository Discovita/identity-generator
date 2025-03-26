"""OpenAI Responses API function results operations."""

from typing import Optional
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion as Response
from discovita.service.openai.client import logging
from discovita.service.openai.models import ResponsesMessage
from .responses import ResponseInput, ResponseTools, ResponseFunctionOutputs

async def submit_results(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    function_outputs: ResponseFunctionOutputs,
    tools: Optional[ResponseTools] = None,
    model: str = "gpt-4o",
    store: bool = True,
    previous_response_id: Optional[str] = None
) -> Response:
    """Submit function results to the OpenAI Responses API."""
    messages = input_data.messages.copy()
    
    # Add function outputs as messages
    outputs = (
        [function_outputs.outputs] 
        if isinstance(function_outputs.outputs, dict) 
        else function_outputs.outputs
    )
    
    for output in outputs:
        messages.append(ResponsesMessage(
            role="assistant",
            content=[{
                "type": "function_call_output",
                "call_id": output["tool_call_id"],
                "output": output["output"]
            }]
        ))
    
    # Create request parameters
    request_params = {
        "model": model,
        "input": messages,
        "tools": tools.tools if tools else None,
        "tool_choice": tools.tool_choice if tools else None,
        "store": store,
        "previous_response_id": previous_response_id
    }
    
    # Remove None values
    request_params = {k: v for k, v in request_params.items() if v is not None}
    
    # Log and send request
    logging.log_request("chat.completions.create", **request_params)
    response = await client.chat.completions.create(**request_params)
    logging.log_response("chat.completions.create", response)
    
    return response
