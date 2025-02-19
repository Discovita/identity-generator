"""Unit tests for safe chat completion."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from openai import AsyncOpenAI
from discovita.service.openai.models import ChatMessage, ChatResponse
from discovita.service.openai.client.safe_chat import safe_chat_completion
from fixtures.openai import MockMessage, MockChoice, MockChatResponse, MockContentFilter


def create_mock_response(content: str, is_violating: bool = False) -> MockChatResponse:
    content_filter = None
    if is_violating:
        content_filter = MockContentFilter(
            is_violating=True,
            category="policy",
            explanation_if_violating="Content violates OpenAI's usage policies"
        )
    return MockChatResponse(
        choices=[MockChoice(message=MockMessage(content=content))],
        content_filter=content_filter
    )


def setup_mock_client() -> AsyncMock:
    mock_client = AsyncMock(spec=AsyncOpenAI)
    mock_completions = AsyncMock()
    mock_chat = MagicMock()
    mock_chat.completions = mock_completions
    mock_client.chat = mock_chat
    return mock_client


@pytest.mark.asyncio
async def test_safe_chat_completion_success():
    mock_client = setup_mock_client()
    mock_response = create_mock_response("Safe response")
    mock_client.chat.completions.create.return_value = mock_response

    response = await safe_chat_completion(mock_client, "Hello")
    assert response.content == "Safe response"
    assert response.content_filter is None
    assert mock_client.chat.completions.create.call_count == 1


@pytest.mark.asyncio
async def test_safe_chat_completion_policy_violation():
    mock_client = setup_mock_client()
    mock_client.chat.completions.create.side_effect = [
        create_mock_response("Unsafe response", is_violating=True),
        create_mock_response("Safe version of prompt"),
        create_mock_response("Final safe response")
    ]

    response = await safe_chat_completion(mock_client, "Unsafe prompt")
    assert response.content == "Final safe response"
    assert response.content_filter is None
    assert mock_client.chat.completions.create.call_count == 3
