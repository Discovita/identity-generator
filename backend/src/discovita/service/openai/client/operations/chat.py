"""OpenAI Chat API operations."""

from openai import AsyncOpenAI
from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    CompletionRequest,
    ChatMessage,
    ChatResponse
)

async def get_completion(
    client: AsyncOpenAI,
    prompt: str
) -> str:
    """Get a completion from GPT-4."""
    request = CompletionRequest(
        messages=[ChatMessage(
            role="user",
            content=prompt
        )]
    )
    
    logging.log_request("completion", **request.model_dump())
    response = await client.chat.completions.create(**request.model_dump())
    logging.log_response("completion", response)
    return ChatResponse.from_openai_response(response).content
