"""Safe chat completion implementation."""

from openai import AsyncOpenAI
from ..models import SafeChatRequest, ChatMessage, ChatResponse
from . import logging

async def create_safe_prompt_request(prompt: str) -> SafeChatRequest:
    return SafeChatRequest(
        model="gpt-4o",
        messages=[
            ChatMessage(
                role="system",
                content="Please rewrite the following prompt to make it appropriate and safe, removing any content that might violate content policies:"
            ),
            ChatMessage(role="user", content=prompt)
        ],
        temperature=0.7
    )

async def create_chat_request(prompt: str) -> SafeChatRequest:
    return SafeChatRequest(
        model="gpt-4o",
        messages=[ChatMessage(role="user", content=prompt)],
        temperature=0.7
    )

async def execute_chat_completion(
    client: AsyncOpenAI,
    request: SafeChatRequest
) -> ChatResponse:
    logging.log_request("safe_chat", **request.model_dump(exclude_none=True))
    response = await client.chat.completions.create(**request.model_dump(exclude_none=True))
    logging.log_response("safe_chat", response)
    return ChatResponse.from_openai_response(response)

async def safe_chat_completion(
    client: AsyncOpenAI,
    prompt: str
) -> ChatResponse:
    request = await create_chat_request(prompt)
    response = await execute_chat_completion(client, request)

    if response.content_filter and response.content_filter.is_violating:
        safe_request = await create_safe_prompt_request(prompt)
        safe_prompt_response = await execute_chat_completion(client, safe_request)
        final_request = await create_chat_request(safe_prompt_response.content)
        return await execute_chat_completion(client, final_request)

    return response
