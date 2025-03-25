"""OpenAI Responses API basic operations."""

from typing import Optional
from openai import AsyncOpenAI
from openai.types.responses import Response
from discovita.service.openai.client import logging
from discovita.service.openai.models import ResponsesRequest
from .responses import ResponseInput, ResponseTools

async def create_response(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    model: str = "gpt-4o",
    tools: Optional[ResponseTools] = None,
    store: bool = True,
    previous_response_id: Optional[str] = None
) -> Response:
    """Create a response using the OpenAI Responses API.
    
    Args:
        client: OpenAI client instance
        input_data: Input data as a ResponseInput object
        model: The model to use (default: "gpt-4o")
        tools: Optional tools configuration
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The raw response from the OpenAI Responses API
    """
    request = ResponsesRequest(
        model=model,
        input=input_data.messages,  # Already List[ResponsesMessage] from our earlier fix
        tools=tools.tools if tools else None,
        tool_choice=tools.tool_choice.model_dump() if tools and tools.tool_choice else None,
        store=store,
        previous_response_id=previous_response_id
    )
    
    # Log the request
    logging.log_request("responses_create", **request.model_dump())
    
    # Send the request to the API
    response = await client.responses.create(**request.model_dump())
    
    # Log the response
    logging.log_response("responses_create", response)
    
    return response
