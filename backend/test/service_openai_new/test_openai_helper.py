"""
Tests for the OpenAI client module.

This module contains tests for the OpenAIClient class, including:
- Initialization
- Basic chat completion
- JSON mode
- Image encoding
- Error handling
"""

import base64
import json
import os
from unittest.mock import ANY, MagicMock, PropertyMock, patch

import pytest
from discovita.service.openai_new import AIModel, OpenAIClient
from openai._types import NOT_GIVEN


# Mock OpenAI API responses
@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response for testing."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    return mock_response


# Test initialization
def test_init():
    """Test that the OpenAIClient initializes correctly."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai:
        client = OpenAIClient(api_key="test_key", organization="test_org")
        mock_openai.assert_called_once_with(api_key="test_key", organization="test_org")


# Test version check
def test_version_check():
    """Test that the version check works correctly."""
    # First, import the actual OPENAI_VERSION constant to ensure we mock a different version
    from discovita.service.openai_new.utils.model_utils import OPENAI_VERSION

    # Create a custom version function for mocking
    def mock_version_func(package_name):
        if package_name == "openai":
            return "0.0.1"  # Return a version different from OPENAI_VERSION
        return "1.0.0"  # Default for other packages

    with (
        patch("discovita.service.openai_new.core.base.OpenAI"),
        patch(
            "discovita.service.openai_new.utils.model_utils.version",
            side_effect=mock_version_func,
        ),
        patch("discovita.service.openai_new.utils.model_utils.log") as mock_log,
        patch.dict(os.environ, {"MUTE_OPENAI_SERVICE_WARNING": "False"}),
    ):

        # Initialize the client, which should trigger the version check
        client = OpenAIClient(api_key="test_key", organization="test_org")

        # Verify that a warning was logged
        mock_log.warning.assert_called_once()

        # Test with muted warnings
        mock_log.reset_mock()
        with patch.dict(os.environ, {"MUTE_OPENAI_SERVICE_WARNING": "True"}):
            client = OpenAIClient(api_key="test_key", organization="test_org")
            mock_log.warning.assert_not_called()


# Test basic chat completion
def test_create_chat_completion(mock_openai_response):
    """Test basic chat completion functionality."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response

        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(prompt="Hello")

        assert response == "Test response"
        mock_completions.create.assert_called_once()

        # Verify the parameters passed to the API
        call_args = mock_completions.create.call_args[1]
        assert call_args["model"] == "gpt-4-turbo-preview"
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == "Hello"


# Test with system message
def test_create_chat_completion_with_system_message(mock_openai_response):
    """Test chat completion with a system message."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response

        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(
            prompt="Hello", system_message="You are a helpful assistant."
        )

        assert response == "Test response"

        # Verify the system message was included
        call_args = mock_completions.create.call_args[1]
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][0]["content"] == "You are a helpful assistant."


# Test JSON mode
def test_json_mode(mock_openai_response):
    """Test chat completion with JSON mode enabled."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"result": "success"}'
        mock_completions.create.return_value = mock_response

        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(prompt="Hello", json_mode=True)

        # Verify that response is parsed JSON
        assert isinstance(response, dict)
        assert response["result"] == "success"

        # Verify response_format was set correctly
        call_args = mock_completions.create.call_args[1]
        assert call_args["response_format"] == {"type": "json_object"}


# Test Pydantic model schema
def test_pydantic_model_schema(mock_openai_response):
    """Test chat completion with a Pydantic model schema."""
    from pydantic import BaseModel

    class TestModel(BaseModel):
        name: str
        age: int

    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up the response with valid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = '{"name": "Test", "age": 30}'
        mock_completions.create.return_value = mock_response

        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(
            prompt="Generate a person",
            response_format=TestModel,
            use_beta_parse=False,  # Disable beta parse endpoint to use legacy approach
        )

        # Verify the response was parsed as JSON
        assert isinstance(response, dict)
        assert response["name"] == "Test"
        assert response["age"] == 30


# Test streaming
def test_streaming(mock_openai_response):
    """Test streaming responses."""
    with patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class:
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions
        mock_completions.create.return_value = mock_openai_response

        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(prompt="Hello", stream=True)

        assert response == mock_openai_response

        # Verify stream parameter was True
        call_args = mock_completions.create.call_args[1]
        assert call_args["stream"] is True


# Test image encoding
def test_encode_image(tmp_path):
    """Test encoding images to base64."""
    # Create a temporary test image
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"test image content")

    # Mock base64 encoding
    with patch("base64.b64encode", return_value=b"encoded_data"):
        from discovita.service.openai_new.utils.image import encode_image

        result = encode_image(str(test_image))

        assert result == "data:image/jpeg;base64,encoded_data"


# Test chat completion with images
def test_create_chat_completion_with_images(mock_openai_response, tmp_path):
    """Test chat completion with image inputs."""
    # Create a temporary test image
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"test image content")

    # We need to patch at the module level where it's imported, not where it's defined
    with patch(
        "discovita.service.openai_new.utils.message_utils.encode_image"
    ) as mock_encode_image:
        mock_encode_image.return_value = "data:image/jpeg;base64,encoded_image_data"

        with patch(
            "discovita.service.openai_new.core.base.OpenAI"
        ) as mock_openai_class:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions
            mock_completions.create.return_value = mock_openai_response

            client = OpenAIClient(api_key="test_key", organization="test_org")
            response = client.create_chat_completion(
                prompt="What's in this image?", images=[str(test_image)], model="gpt-4o"
            )

            assert response == "Test response"

            # Verify the parameters passed to the API
            call_args = mock_completions.create.call_args[1]
            assert call_args["model"] == "gpt-4o"

            # Verify the message format is correct
            messages = call_args["messages"]
            assert len(messages) == 1
            assert messages[0]["role"] == "user"
            assert isinstance(messages[0]["content"], list)

            # Verify first part is text
            assert messages[0]["content"][0]["type"] == "text"
            assert messages[0]["content"][0]["text"] == "What's in this image?"

            # Verify second part is image
            assert messages[0]["content"][1]["type"] == "image_url"
            assert (
                messages[0]["content"][1]["image_url"]["url"]
                == "data:image/jpeg;base64,encoded_image_data"
            )

            # Verify mock was called with the image path
            mock_encode_image.assert_called_with(str(test_image))


# Test chat completion with URL images
def test_create_chat_completion_with_url_images(mock_openai_response):
    """Test chat completion with image URL inputs."""
    # Use a URL instead of a local file
    image_url = "https://example.com/image.jpg"

    # We need to patch at the module level where it's imported, not where it's defined
    with patch(
        "discovita.service.openai_new.utils.message_utils.encode_image"
    ) as mock_encode_image:
        mock_encode_image.return_value = "data:image/jpeg;base64,encoded_url_image"

        with patch(
            "discovita.service.openai_new.core.base.OpenAI"
        ) as mock_openai_class:
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions
            mock_completions.create.return_value = mock_openai_response

            client = OpenAIClient(api_key="test_key", organization="test_org")
            response = client.create_chat_completion(
                prompt="What's in this image?", images=[image_url], model="gpt-4o"
            )

            assert response == "Test response"

            # Verify the parameters passed to the API
            call_args = mock_completions.create.call_args[1]

            # Verify the message format is correct
            messages = call_args["messages"]
            assert len(messages) == 1
            assert messages[0]["role"] == "user"
            assert isinstance(messages[0]["content"], list)

            # Verify first part is text
            assert messages[0]["content"][0]["type"] == "text"
            assert messages[0]["content"][0]["text"] == "What's in this image?"

            # Verify second part is image
            assert messages[0]["content"][1]["type"] == "image_url"
            assert (
                messages[0]["content"][1]["image_url"]["url"]
                == "data:image/jpeg;base64,encoded_url_image"
            )

            # Verify mock was called with the image URL
            mock_encode_image.assert_called_with(image_url)


# Test error handling for missing images
def test_missing_image_error_handling():
    """Test error handling for missing image files."""
    with patch(
        "discovita.service.openai_new.utils.image.os.path.exists", return_value=False
    ):
        from discovita.service.openai_new.utils.image import encode_image

        # Should raise FileNotFoundError for non-existent image
        with pytest.raises(FileNotFoundError):
            encode_image("nonexistent_image.jpg")


# Test error handling for JSON parsing
def test_json_parsing_error():
    """Test error handling for JSON parsing errors."""
    with (
        patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class,
        patch("discovita.service.openai_new.core.completion_handlers.log") as mock_log,
    ):
        # Set up the mock chain
        mock_openai = MagicMock()
        mock_openai_class.return_value = mock_openai
        mock_chat = MagicMock()
        mock_openai.chat = mock_chat
        mock_completions = MagicMock()
        mock_chat.completions = mock_completions

        # Set up a mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "{invalid json"
        mock_completions.create.return_value = mock_response

        # Initialize client and make request with JSON mode
        client = OpenAIClient(api_key="test_key", organization="test_org")
        response = client.create_chat_completion(prompt="Hello", json_mode=True)

        # Verify that the original string is returned on JSON parse error
        assert response == "{invalid json"

        # Verify the error was logged
        mock_log.error.assert_called_once()


class TestOpenAIClient:
    """Tests for the OpenAIClient class methods."""

    def test_filter_unsupported_parameters(self):
        """Test filtering out unsupported parameters based on the model."""

        # Initialize client
        with patch("discovita.service.openai_new.core.base.OpenAI"):
            client = OpenAIClient(api_key="test_key", organization="test_org")

            # Test with O-series model
            with patch(
                "discovita.service.openai_new.utils.model_utils.AIModel.get_unsupported_parameters"
            ) as mock_get_unsupported:
                # Set up mock to return unsupported parameters for o-series models
                mock_get_unsupported.return_value = {"temperature", "top_p"}

                # Create params dict with unsupported parameters
                params = {
                    "model": "o3-mini",
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_completion_tokens": 100,
                    "messages": [{"role": "user", "content": "Hello"}],
                }

                # Filter parameters
                from discovita.service.openai_new.utils.model_utils import (
                    filter_unsupported_parameters,
                )

                filtered_params = filter_unsupported_parameters(params, "o3-mini")

                # Verify unsupported parameters were removed
                assert "temperature" not in filtered_params
                assert "top_p" not in filtered_params
                assert "max_completion_tokens" in filtered_params
                assert "messages" in filtered_params

                # Verify original dict was not modified
                assert "temperature" in params

            # Test with standard model (no unsupported parameters)
            with patch(
                "discovita.service.openai_new.utils.model_utils.AIModel.get_unsupported_parameters"
            ) as mock_get_unsupported:
                # Set up mock to return empty set for standard models
                mock_get_unsupported.return_value = set()

                # Create params dict
                params = {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 100,
                    "messages": [{"role": "user", "content": "Hello"}],
                }

                # Filter parameters
                from discovita.service.openai_new.utils.model_utils import (
                    filter_unsupported_parameters,
                )

                filtered_params = filter_unsupported_parameters(params, "gpt-4")

                # Verify no parameters were removed
                assert "temperature" in filtered_params
                assert "top_p" in filtered_params
                assert "max_tokens" in filtered_params
                assert "messages" in filtered_params

    def test_create_chat_completion_with_unsupported_parameters(self):
        """Test that unsupported parameters are automatically filtered out when making API calls."""
        with (
            patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class,
            patch(
                "discovita.service.openai_new.utils.model_utils.AIModel.get_unsupported_parameters"
            ) as mock_get_unsupported,
            patch("discovita.service.openai_new.utils.model_utils.log") as mock_log,
        ):
            # Set up the mock chain
            mock_openai = MagicMock()
            mock_openai_class.return_value = mock_openai
            mock_chat = MagicMock()
            mock_openai.chat = mock_chat
            mock_completions = MagicMock()
            mock_chat.completions = mock_completions

            # Set up mock to return unsupported parameters for o-series models
            mock_get_unsupported.return_value = {"temperature", "top_p"}

            # Set up a mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "Test response"
            mock_completions.create.return_value = mock_response

            # Initialize client and make request with unsupported parameters
            client = OpenAIClient(api_key="test_key", organization="test_org")
            response = client.create_chat_completion(
                prompt="Hello",
                model="o3-mini",
                temperature=0.7,  # This should be filtered out
                top_p=0.9,  # This should be filtered out
                max_completion_tokens=100,
            )

            # Verify response was returned
            assert response == "Test response"

            # Verify parameters were filtered out before API call
            call_args = mock_completions.create.call_args[1]
            assert "temperature" not in call_args
            assert "top_p" not in call_args
            assert "max_completion_tokens" in call_args

            # Verify warnings were logged
            assert mock_log.warning.call_count >= 2

    def test_structured_chat_completion_with_unsupported_parameters(self):
        """Test that unsupported parameters are automatically filtered out when making structured API calls."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            result: str

        with (
            patch("discovita.service.openai_new.core.base.OpenAI") as mock_openai_class,
            patch(
                "discovita.service.openai_new.utils.model_utils.AIModel.get_unsupported_parameters"
            ) as mock_get_unsupported,
            patch("discovita.service.openai_new.utils.model_utils.log") as mock_log,
            patch(
                "discovita.service.openai_new.types.response_types.get_parsed_chat_completion"
            ) as mock_get_parsed,
        ):
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

            # Set up mock to return unsupported parameters for o-series models
            mock_get_unsupported.return_value = {"temperature", "top_p"}

            # Set up the mock response for beta.chat.completions.parse
            mock_response = MagicMock()
            mock_completions.parse.return_value = mock_response

            # Initialize helper and make structured request with unsupported parameters
            helper = OpenAIClient(api_key="test_key", organization="test_org")
            response = helper.create_structured_chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="o3-mini",
                response_format=TestModel,
                temperature=0.7,  # This should be filtered out
                top_p=0.9,  # This should be filtered out
                max_completion_tokens=100,
            )

            # Verify response was returned
            assert response == mock_response

            # Verify parameters were filtered out before API call
            call_args = mock_completions.parse.call_args[1]
            assert "temperature" not in call_args
            assert "top_p" not in call_args
            assert "max_completion_tokens" in call_args
            assert call_args["response_format"] == TestModel

            # Verify warnings were logged
            assert mock_log.warning.call_count >= 2
