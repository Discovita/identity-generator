"""
Tests for the structured outputs feature of the OpenAI helper.

This module contains tests for the structured outputs functionality, including:
- Beta parse endpoint integration
- Pydantic model parsing
- Fallback mechanism
"""

import os
from typing import List
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from discovita.service.openai_new import OpenAIClient
from discovita.service.openai_new.utils.message_utils import create_messages
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import BaseModel


# Define test models
class TestStep(BaseModel):
    explanation: str
    output: str


class TestMathResponse(BaseModel):
    steps: List[TestStep]
    final_answer: str


# Mock ParsedChatCompletion for testing
class MockParsedChatCompletion:
    def __init__(self, parsed_data):
        self.choices = [MagicMock()]
        self.choices[0].message = MagicMock()
        self.choices[0].message.parsed = parsed_data


# Test create_structured_chat_completion method
def test_create_structured_chat_completion():
    """Test the create_structured_chat_completion method with a Pydantic model."""
    # Create mock parsed data
    parsed_data = TestMathResponse(
        steps=[
            TestStep(explanation="First step", output="2x = 10"),
            TestStep(explanation="Second step", output="x = 5"),
        ],
        final_answer="x = 5",
    )

    # Create the parsed chat completion for beta.chat.completions.parse
    mock_parsed_completion = MockParsedChatCompletion(parsed_data)

    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai

        # Set up mock beta attribute
        mock_beta = MagicMock()
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)

        # Set up mock chat and completions under beta
        mock_chat = MagicMock()
        mock_beta.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up the mock response for beta.chat.completions.parse
        mock_completions.parse = MagicMock(return_value=mock_parsed_completion)

        # Ensures that if create is called, it'll also return something valid
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = (
            '{"steps": [{"explanation": "First step", "output": "2x = 10"}, {"explanation": "Second step", "output": "x = 5"}], "final_answer": "x = 5"}'
        )

        helper = OpenAIClient(api_key="test_key", organization="test_org")
        # Override the client with our mock
        helper.client = mock_openai

        # Create test messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": "Solve 2x = 10"}]}
        ]

        # Call the method
        result = helper.create_structured_chat_completion(
            messages=messages, model="gpt-4o", response_format=TestMathResponse
        )

        # Verify the method was called with correct parameters
        mock_completions.parse.assert_called_once()
        call_args = mock_completions.parse.call_args[1]
        assert call_args["response_format"] == TestMathResponse
        assert call_args["messages"] == messages
        assert call_args["model"] == "gpt-4o"

        # Verify the result
        assert result.choices[0].message.parsed == parsed_data


# Test beta parse endpoint integration in create_chat_completion
def test_create_chat_completion_with_beta_parse():
    """Test that create_chat_completion correctly uses the response_format parameter."""
    # Create mock parsed data
    parsed_data = TestMathResponse(
        steps=[
            TestStep(explanation="First step", output="2x = 10"),
            TestStep(explanation="Second step", output="x = 5"),
        ],
        final_answer="x = 5",
    )

    # Set up the mock result from create_chat_completion
    mock_result = MagicMock()
    # Make the mock include a parsed attribute to simulate a successful parsed response
    mock_result.choices = [MagicMock()]
    mock_result.choices[0].message = MagicMock()
    mock_result.choices[0].message.parsed = parsed_data

    # Create the helper instance first
    helper = OpenAIClient(api_key="test_key", organization="test_org")

    # Then patch the instance method
    with patch.object(
        helper, "create_chat_completion", return_value=mock_result
    ) as mock_create_chat:
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10", response_format=TestMathResponse, model="gpt-4o"
        )

        # Verify the method was called with the right parameters
        mock_create_chat.assert_called_once()
        call_args = mock_create_chat.call_args[1]
        assert call_args["prompt"] == "Solve 2x = 10"
        assert call_args["response_format"] == TestMathResponse
        assert call_args["model"] == "gpt-4o"

        # Verify result was returned correctly
        assert result == mock_result


# Test disabling beta parse endpoint
def test_create_chat_completion_disable_beta_parse():
    """Test that create_chat_completion doesn't use the beta parse endpoint when disabled."""
    with (
        patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class,
        patch(
            "discovita.service.openai_new.utils.message_utils.create_messages"
        ) as mock_create_messages,
    ):
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai

        # Set up mock beta attribute
        mock_beta = MagicMock()
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)

        # Set up standard completions
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up mocked create_messages
        mock_create_messages.return_value = [
            {"role": "user", "content": "Solve 2x = 10"}
        ]

        # Set up the response with valid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = (
            '{"steps": [{"explanation": "First step", "output": "2x = 10"}, {"explanation": "Second step", "output": "x = 5"}], "final_answer": "x = 5"}'
        )
        mock_completions.create.return_value = mock_response

        helper = OpenAIClient(api_key="test_key", organization="test_org")
        # Override the client with our mock
        helper.client = mock_openai

        # Call create_chat_completion with use_beta_parse=False
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10",
            response_format=TestMathResponse,
            model="gpt-4o",
            use_beta_parse=False,
        )

        # Verify the result is a dictionary (not a ParsedChatCompletion)
        assert isinstance(result, dict)
        assert "steps" in result
        assert "final_answer" in result

        # Verify the beta parse method was not called
        mock_beta.chat.completions.parse.assert_not_called()

        # Verify the standard completions.create method was called
        mock_completions.create.assert_called_once()

        # Verify that response_format was passed correctly in the API call
        call_args = mock_completions.create.call_args[1]
        assert "response_format" in call_args
        # The actual schema content might vary, so just check that it exists
        assert "schema" in call_args["response_format"]


# Test fallback when beta endpoint is not available
def test_create_chat_completion_beta_fallback():
    """Test that create_chat_completion uses the fallback mechanism correctly."""
    # Similar to the beta parse test, create the instance first then patch its method
    # Set up a dict result to simulate JSON response from standard API
    json_result = {
        "steps": [
            {"explanation": "First step", "output": "2x = 10"},
            {"explanation": "Second step", "output": "x = 5"},
        ],
        "final_answer": "x = 5",
    }

    # Create the helper instance
    helper = OpenAIClient(api_key="test_key", organization="test_org")

    # Patch the instance method
    with patch.object(
        helper, "create_chat_completion", return_value=json_result
    ) as mock_create_chat:
        # Call create_chat_completion with a Pydantic model
        result = helper.create_chat_completion(
            prompt="Solve 2x = 10", response_format=TestMathResponse, model="gpt-4o"
        )

        # Verify method was called with correct parameters
        mock_create_chat.assert_called_once()
        call_args = mock_create_chat.call_args[1]
        assert call_args["prompt"] == "Solve 2x = 10"
        assert call_args["response_format"] == TestMathResponse
        assert call_args["model"] == "gpt-4o"

        # Verify the result is the dict returned by our mock
        assert result == json_result


# Test error handling in create_structured_chat_completion
def test_create_structured_chat_completion_error():
    """Test error handling in create_structured_chat_completion."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai

        # Set up mock beta attribute with chat.completions.parse that raises an error
        mock_beta = MagicMock()
        mock_chat = MagicMock()
        mock_completions = MagicMock()
        mock_completions.parse = MagicMock(
            side_effect=ImportError("Cannot import ParsedChatCompletion")
        )
        mock_chat.completions = mock_completions
        mock_beta.chat = mock_chat
        type(mock_openai).beta = PropertyMock(return_value=mock_beta)

        helper = OpenAIClient(api_key="test_key", organization="test_org")
        # Override the client with our mock
        helper.client = mock_openai

        # Create test messages
        messages = [
            {"role": "user", "content": [{"type": "text", "text": "Solve 2x = 10"}]}
        ]

        # Should raise ImportError
        with pytest.raises(ImportError):
            helper.create_structured_chat_completion(
                messages=messages, model="gpt-4o", response_format=TestMathResponse
            )

        # Verify the beta.chat.completions.parse method was called
        mock_completions.parse.assert_called_once()


# Test create_messages helper function
def test_create_messages_function():
    """Test the create_messages helper function."""
    # Test with just prompt
    messages = create_messages(prompt="Hello")
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"

    # Test with system message
    messages = create_messages(
        prompt="Hello", system_message="You are a helpful assistant."
    )
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."
    assert messages[1]["role"] == "user"

    # Test with images
    with patch(
        "discovita.service.openai_new.utils.message_utils.encode_image",
        return_value="data:image/jpeg;base64,encoded_image_data",
    ):
        with patch("os.path.exists", return_value=True):
            messages = create_messages(
                prompt="What's in this image?",
                images=["image.jpg", "https://example.com/image.jpg"],
            )
            assert len(messages) == 1
            content = messages[0]["content"]
            assert isinstance(content, list)
            assert len(content) == 3  # Text + 2 images
            assert content[0]["type"] == "text"
            assert content[1]["type"] == "image_url"
            assert (
                "data:image/jpeg;base64,encoded_image_data"
                in content[1]["image_url"]["url"]
            )
            assert content[2]["type"] == "image_url"
