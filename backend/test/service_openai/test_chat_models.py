"""Tests for chat models in the OpenAI service."""

from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock

import pytest
from discovita.service.openai.models.chat_models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CompletionRequest,
    ContentFilter,
    SafeChatRequest,
    VisionRequest,
)


class TestChatModels:
    """Test cases for chat models used with OpenAI API."""

    def test_chat_message_creation(self):
        """Test ChatMessage model initialization and validation."""
        # Test with string content
        message = ChatMessage(role="user", content="Hello world")
        assert message.role == "user"
        assert message.content == "Hello world"

        # Test with list content (for vision API)
        content_list = [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/image.jpg"},
            },
        ]
        message = ChatMessage(role="user", content=content_list)
        assert message.role == "user"
        assert isinstance(message.content, list)
        assert len(message.content) == 2
        assert message.content[0]["type"] == "text"
        assert message.content[1]["type"] == "image_url"

    def test_chat_request_creation(self):
        """Test ChatRequest model initialization and validation."""
        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content="Hello"),
        ]
        request = ChatRequest(model="gpt-4", messages=messages)

        assert request.model == "gpt-4"
        assert len(request.messages) == 2
        assert request.max_tokens == 300  # Default value

        # Test with custom max_tokens
        request = ChatRequest(model="gpt-4", messages=messages, max_tokens=500)
        assert request.max_tokens == 500

    def test_content_filter(self):
        """Test ContentFilter model."""
        # Test with no violation
        filter_ok = ContentFilter(is_violating=False)
        assert filter_ok.is_violating is False
        assert filter_ok.category is None
        assert filter_ok.explanation_if_violating is None

        # Test with violation
        filter_violation = ContentFilter(
            is_violating=True,
            category="violence",
            explanation_if_violating="Contains violent content",
        )
        assert filter_violation.is_violating is True
        assert filter_violation.category == "violence"
        assert filter_violation.explanation_if_violating == "Contains violent content"

    def test_chat_response_creation(self):
        """Test ChatResponse model initialization."""
        response = ChatResponse(content="Hello, how can I help you?")
        assert response.content == "Hello, how can I help you?"
        assert response.content_filter is None

        # Test with content filter
        filter_data = ContentFilter(
            is_violating=False, category=None, explanation_if_violating=None
        )
        response = ChatResponse(content="Hello", content_filter=filter_data)
        assert response.content == "Hello"
        assert response.content_filter is not None
        assert response.content_filter.is_violating is False

    def test_from_openai_response(self):
        """Test creating ChatResponse from OpenAI API response."""
        # Create a mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"

        # Test without content filter
        mock_response.content_filter = None
        response = ChatResponse.from_openai_response(mock_response)
        assert response.content == "This is a test response"
        assert response.content_filter is None

        # Test with content filter
        mock_content_filter = MagicMock()
        mock_content_filter.is_violating = False
        mock_content_filter.category = None
        mock_content_filter.explanation_if_violating = None
        mock_response.content_filter = mock_content_filter

        response = ChatResponse.from_openai_response(mock_response)
        assert response.content == "This is a test response"
        assert response.content_filter is not None
        assert response.content_filter.is_violating is False

    def test_vision_request(self):
        """Test VisionRequest model initialization."""
        messages = [
            ChatMessage(
                role="user",
                content=[
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": "https://example.com/image.jpg"},
                    },
                ],
            )
        ]
        request = VisionRequest(messages=messages)

        # Check default model
        assert request.model == "gpt-4o-mini"
        assert len(request.messages) == 1
        assert isinstance(request.messages[0].content, list)

        # Test with custom model
        request = VisionRequest(model="gpt-4o", messages=messages)
        assert request.model == "gpt-4o"

    def test_completion_request(self):
        """Test CompletionRequest model initialization."""
        messages = [ChatMessage(role="user", content="Generate a JSON response")]
        request = CompletionRequest(messages=messages)

        # Check defaults
        assert request.model == "gpt-4o"
        assert request.max_tokens == 1000
        assert request.response_format is None

        # Test with JSON response format
        json_format = {"type": "json_object"}
        request = CompletionRequest(messages=messages, response_format=json_format)
        assert request.response_format == json_format

    def test_safe_chat_request(self):
        """Test SafeChatRequest model initialization."""
        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content="Hello"),
        ]
        request = SafeChatRequest(messages=messages)

        # Check defaults
        assert request.model == "gpt-4"
        assert request.temperature == 0.7
        assert len(request.messages) == 2

        # Test with custom values
        request = SafeChatRequest(
            model="gpt-3.5-turbo", messages=messages, temperature=0.2, max_tokens=200
        )
        assert request.model == "gpt-3.5-turbo"
        assert request.temperature == 0.2
        assert request.max_tokens == 200
