"""
Tests for the chat completion capabilities of OpenAIService.

This module tests the chat completion functionality of the OpenAIService,
including basic text completions, parameter handling, and error handling.
"""

from unittest.mock import ANY, MagicMock, patch

import pytest
from discovita.service.openai import AIModel, OpenAIService
from openai._types import NOT_GIVEN


class TestChatCompletion:
    """
    Tests for the chat completion functionality in OpenAIService.

    These tests verify that the service correctly sends requests
    to the OpenAI API and processes the responses.
    """

    def test_basic_chat_completion(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test basic chat completion functionality.

        This test verifies that a simple chat completion request is
        sent to the API with the correct parameters and that the
        response is correctly processed.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion
            response = service.create_chat_completion(messages=messages)

            # Verify the response
            assert response == "Test response content"

            # Verify the API was called with the correct parameters
            mock_openai_client.chat.completions.create.assert_called_once()
            call_args = mock_openai_client.chat.completions.create.call_args[1]

            # Check that the model is correct (without asserting exact model, which might change)
            assert "model" in call_args
            assert isinstance(call_args["model"], str)

            # Check message structure
            assert len(call_args["messages"]) == 1
            assert call_args["messages"][0]["role"] == "user"
            assert call_args["messages"][0]["content"] == "Hello"

    def test_chat_completion_with_model_param(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test chat completion with a specific model.

        This test verifies that the specified model is correctly
        passed to the API.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with a specific model
            response = service.create_chat_completion(
                messages=messages, model="gpt-3.5-turbo"
            )

            # Verify the response
            assert response == "Test response content"

            # Verify the API was called with the correct model
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["model"] == "gpt-3.5-turbo"

    def test_chat_completion_with_temperature(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test chat completion with a temperature parameter.

        This test verifies that the specified temperature is correctly
        passed to the API.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with a specific temperature
            response = service.create_chat_completion(
                messages=messages, temperature=0.7
            )

            # Verify the API was called with the correct temperature
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["temperature"] == 0.7

    def test_chat_completion_with_max_tokens(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test chat completion with a max_tokens parameter.

        This test verifies that the max_tokens parameter is correctly
        mapped to the appropriate parameter name for the model and
        passed to the API.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with GPT-4 and max_tokens
            response = service.create_chat_completion(
                messages=messages, model="gpt-4", max_tokens=100
            )

            # Verify the API was called with max_tokens
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["max_tokens"] == 100

            # Reset the mock
            mock_openai_client.chat.completions.create.reset_mock()

            # Call create_chat_completion with o3-mini (which uses max_completion_tokens)
            response = service.create_chat_completion(
                messages=messages, model="o3-mini", max_tokens=100
            )

            # Verify the API was called with max_completion_tokens
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["max_completion_tokens"] == 100

    def test_chat_completion_with_stream(
        self, mock_openai_client, mock_streaming_response
    ):
        """
        Test chat completion with streaming enabled.

        This test verifies that the stream parameter is correctly
        passed to the API and that the streamed response is returned.
        """
        # Set up the mock to return a test streaming response
        mock_openai_client.chat.completions.create.return_value = (
            mock_streaming_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with streaming enabled
            response = service.create_chat_completion(messages=messages, stream=True)

            # Verify the API was called with stream=True
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["stream"] is True

            # Verify the raw streaming response is returned
            assert response == mock_streaming_response

    def test_filter_unsupported_parameters(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test that unsupported parameters are filtered out for specific models.

        This test verifies that parameters not supported by a specific model
        are filtered out before the API call.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with o3-mini (which doesn't support temperature)
            response = service.create_chat_completion(
                messages=messages,
                model="o3-mini",
                temperature=0.7,  # This should be removed
                max_tokens=100,
                top_p=0.9,  # This should also be removed
            )

            # Verify the API call doesn't include temperature or top_p
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert "temperature" not in call_args
            assert "top_p" not in call_args
            assert "max_completion_tokens" in call_args

    def test_error_handling(self, mock_openai_client):
        """
        Test error handling in chat completion.

        This test verifies that errors from the OpenAI API are
        properly caught and re-raised.
        """
        # Set up the mock to raise an exception
        mock_openai_client.chat.completions.create.side_effect = Exception("API error")

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion and verify it raises the exception
            with pytest.raises(Exception) as excinfo:
                service.create_chat_completion(messages=messages)

            assert "API error" in str(excinfo.value)

    def test_handle_deprecated_parameters(
        self, mock_openai_client, mock_chat_completion_response
    ):
        """
        Test handling of deprecated parameters.

        This test verifies that deprecated parameters (like max_tokens)
        are correctly mapped to the appropriate parameter name for the model.
        """
        # Set up the mock to return a test response
        mock_openai_client.chat.completions.create.return_value = (
            mock_chat_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Hello")

            # Call create_chat_completion with max_tokens (should be mapped to max_completion_tokens for o3-mini)
            with patch(
                "discovita.service.openai.utils.model_utils.AIModel.get_token_param_name",
                return_value="max_completion_tokens",
            ):
                response = service.create_chat_completion(
                    messages=messages, model="o3-mini", max_tokens=100
                )

                # Verify the API was called with max_completion_tokens, not max_tokens
                call_args = mock_openai_client.chat.completions.create.call_args[1]
                assert "max_tokens" not in call_args
                assert call_args["max_completion_tokens"] == 100
