"""OpenAI Chat API operations."""

from typing import TypeVar, Type, List, Dict, Any
from openai import AsyncOpenAI
from pydantic import BaseModel
from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    CompletionRequest,
    ChatMessage,
    ChatResponse
)

T = TypeVar('T', bound=BaseModel)

async def get_completion(client: AsyncOpenAI, prompt: str) -> str:
    """Get a completion from GPT-4."""
    request = CompletionRequest(
        messages=[ChatMessage(role="user", content=prompt)]
    )
    
    logging.log_request("completion", **request.model_dump())
    response = await client.chat.completions.create(**request.model_dump())
    logging.log_response("completion", response)
    return ChatResponse.from_openai_response(response).content

async def get_structured_completion(
    client: AsyncOpenAI,
    messages: List[Dict[str, Any]],
    response_model: Type[T]
) -> T:
    """Get a structured completion from GPT-4.
    
    Args:
        client: OpenAI client instance
        messages: List of message dictionaries with role and content
        response_model: Pydantic model class for response validation
    """
    request = CompletionRequest(
        messages=[ChatMessage(**msg) for msg in messages],
        response_format={"type": "json_object"}
    )
    
    logging.log_request("structured_completion", **request.model_dump())
    response = await client.chat.completions.create(**request.model_dump())
    logging.log_response("structured_completion", response)
    
    return response_model.model_validate_json(
        response.choices[0].message.content
    )
