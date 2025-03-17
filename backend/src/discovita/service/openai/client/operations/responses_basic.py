"""OpenAI Responses API basic operations.

This module contains basic operations for the OpenAI Responses API,
including creating responses and handling text outputs.
"""

from typing import Union, List, Dict, Any
from openai import AsyncOpenAI
from openai.types.responses import Response
from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    ResponsesMessage,
    ResponsesRequest
)

async def create_response(
    client: AsyncOpenAI,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    model: str = "gpt-4o",
    tools: List[Dict[str, Any]] = None,
    tool_choice: Union[str, Dict[str, Any]] = None,
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Create a response using the OpenAI Responses API.
    
    This function sends a request to the OpenAI Responses API and returns
    the response. It handles both text and message list inputs.
    
    Args:
        client: OpenAI client instance
        input_data: Input data, which can be a string or a list of messages
        model: The model to use (default: "gpt-4o")
        tools: Optional tools (including functions) available to the model
        tool_choice: Optional parameter to control which tool the model uses
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The raw response from the OpenAI Responses API
    """
    # Convert input to the format expected by the API
    if isinstance(input_data, str):
        # If input is a string, convert it to a single user message
        messages = [{"role": "user", "content": input_data}]
    elif isinstance(input_data, list):
        if all(isinstance(msg, ResponsesMessage) for msg in input_data):
            # If input is a list of ResponsesMessage objects, convert to dicts
            messages = [msg.model_dump() for msg in input_data]
        else:
            # Assume input is already a list of message dicts
            messages = input_data
    else:
        raise ValueError("Input must be a string or a list of messages")
    
    # Create the request
    request = ResponsesRequest(
        model=model,
        input=messages,
        tools=tools,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )
    
    # Log the request
    logging.log_request("responses_create", **request.model_dump())
    
    # Send the request to the API
    response = await client.responses.create(**request.model_dump())
    
    # Log the response
    logging.log_response("responses_create", response)
    
    # Return the raw response
    return response 