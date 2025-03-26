"""OpenAI chat completions with structured output."""

from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from discovita.service.openai.client import logging
from .responses import ResponseInput

async def create_response(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    model: str = "gpt-4o",
    response_format: Optional[Dict[str, Any]] = None,
    store: bool = True,
    previous_response_id: Optional[str] = None
) -> ChatCompletion:
    """Create a chat completion with structured output.
    
    Args:
        client: OpenAI client instance
        input_data: Input data as a ResponseInput object
        model: The model to use (default: "gpt-4o")
        response_format: Optional response format (e.g. {"type": "json_object"})
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        ChatCompletion: The response from the OpenAI Chat API
    """
    request = {
        "model": model,
        "messages": input_data.messages,
        "response_format": response_format or {"type": "json_object"},
    }
    
    # Log the request
    logging.log_request("chat.completions.create", **request)
    
    # Send the request to the API
    response = await client.chat.completions.create(**request)
    
    # Log the response
    logging.log_response("chat.completions.create", response)
    
    return response
