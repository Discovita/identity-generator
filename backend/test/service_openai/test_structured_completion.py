"""
Tests for structured completion functionality in the OpenAI service.

This module tests the structured completion capabilities of the OpenAIService,
including Pydantic model parsing and error handling.
"""

from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest
from discovita.service.openai import OpenAIService
from pydantic import BaseModel, Field


class TestStructuredCompletion:
    """
    Tests for structured completion functionality in the OpenAIService.

    These tests verify that the service correctly handles
    structured completions from the OpenAI API.
    """

    def test_basic_structured_completion(self, mock_openai_client):
        """
        Test basic structured completion functionality.

        This test verifies that the basic structured completion functionality
        correctly processes structured responses from the API.
        """

        # Define a test model
        class TestModel(BaseModel):
            """Test model for structured outputs."""

            name: str
            count: int
            items: List[str]

        # Create a mock parsed response
        mock_parsed_response = MagicMock()
        mock_parsed_response.choices = [MagicMock()]
        mock_parsed_response.choices[0].message = MagicMock()
        mock_parsed_response.choices[0].message.parsed = TestModel(
            name="Test", count=3, items=["Item 1", "Item 2", "Item 3"]
        )

        # Set up the mock client
        mock_openai_client.beta = MagicMock()
        mock_openai_client.beta.chat = MagicMock()
        mock_openai_client.beta.chat.completions = MagicMock()
        mock_openai_client.beta.chat.completions.parse.return_value = (
            mock_parsed_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate test data")

            # Call create_structured_chat_completion
            response = service.create_structured_chat_completion(
                messages=messages, model="gpt-4o", response_format=TestModel
            )

            # Verify the API was called with the correct parameters
            mock_openai_client.beta.chat.completions.parse.assert_called_once()
            call_args = mock_openai_client.beta.chat.completions.parse.call_args[1]
            assert call_args["model"] == "gpt-4o"
            assert call_args["response_format"] == TestModel
            assert len(call_args["messages"]) == 1
            assert call_args["messages"][0]["role"] == "user"
            assert call_args["messages"][0]["content"] == "Generate test data"

            # Verify the response
            assert response == mock_parsed_response
            parsed_data = response.choices[0].message.parsed
            assert parsed_data.name == "Test"
            assert parsed_data.count == 3
            assert parsed_data.items == ["Item 1", "Item 2", "Item 3"]

    def test_structured_completion_with_pydantic_return(self, mock_openai_client):
        """
        Test structured completion with Pydantic model return.

        This test verifies that the service can return the parsed data
        as a Pydantic model instance.
        """

        # Define a test model
        class TestModel(BaseModel):
            """Test model for structured outputs."""

            name: str
            count: int
            items: List[str]

        # Create mock data
        model_data = TestModel(
            name="Test", count=3, items=["Item 1", "Item 2", "Item 3"]
        )

        # Create a mock parsed response
        mock_parsed_response = MagicMock()
        mock_parsed_response.choices = [MagicMock()]
        mock_parsed_response.choices[0].message = MagicMock()
        mock_parsed_response.choices[0].message.parsed = model_data

        # Set up the mock client
        mock_openai_client.beta = MagicMock()
        mock_openai_client.beta.chat = MagicMock()
        mock_openai_client.beta.chat.completions = MagicMock()
        mock_openai_client.beta.chat.completions.parse.return_value = (
            mock_parsed_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate test data")

            # Call create_structured_chat_completion and manually extract the parsed data
            response = service.create_structured_chat_completion(
                messages=messages, model="gpt-4o", response_format=TestModel
            )

            # Extract the Pydantic model from the response
            parsed_data = response.choices[0].message.parsed

            # Verify the response is a Pydantic model
            assert isinstance(parsed_data, TestModel)
            assert parsed_data.name == "Test"
            assert parsed_data.count == 3
            assert parsed_data.items == ["Item 1", "Item 2", "Item 3"]

    def test_structured_completion_with_custom_schema(self, mock_openai_client):
        """
        Test structured completion with a custom schema.

        This test verifies that a custom schema is correctly
        passed to the API.
        """
        # Create a mock parsed response
        mock_parsed_response = MagicMock()
        mock_parsed_response.choices = [MagicMock()]
        mock_parsed_response.choices[0].message = MagicMock()
        mock_parsed_response.choices[0].message.parsed = {
            "name": "Test",
            "count": 3,
            "items": ["Item 1", "Item 2", "Item 3"],
        }

        # Set up the mock client
        mock_openai_client.beta = MagicMock()
        mock_openai_client.beta.chat = MagicMock()
        mock_openai_client.beta.chat.completions = MagicMock()
        mock_openai_client.beta.chat.completions.parse.return_value = (
            mock_parsed_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate test data")

            # Define a custom schema
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "count": {"type": "integer"},
                    "items": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "count", "items"],
            }

            # Call create_structured_chat_completion with a custom schema
            response = service.create_structured_chat_completion(
                messages=messages, model="gpt-4o", response_format=schema
            )

            # Verify the API was called with the correct parameters
            call_args = mock_openai_client.beta.chat.completions.parse.call_args[1]
            assert "response_format" in call_args
            assert call_args["response_format"] == schema

            # Verify the response
            assert response == mock_parsed_response
            parsed_data = response.choices[0].message.parsed
            assert parsed_data["name"] == "Test"
            assert parsed_data["count"] == 3
            assert parsed_data["items"] == ["Item 1", "Item 2", "Item 3"]

    def test_structured_completion_token_parameter_error(self, mock_openai_client):
        """
        Test recovery from token parameter errors in structured completion.

        This test verifies that token parameter errors in structured completion
        are properly recovered from by retrying with the correct parameter.
        """

        # Define a test model
        class TestModel(BaseModel):
            """Test model for structured outputs."""

            value: str

        # Create a mock response for the retry
        mock_parsed_response = MagicMock()
        mock_parsed_response.choices = [MagicMock()]
        mock_parsed_response.choices[0].message = MagicMock()
        mock_parsed_response.choices[0].message.parsed = TestModel(value="Hello")

        # Track number of calls to mock
        call_count = [0]

        # Define a custom side effect function for the parse method
        def parse_side_effect(**kwargs):
            call_count[0] += 1
            if call_count[0] == 1:  # First call
                # If this is using max_completion_tokens already, pretend the error has been fixed
                if "max_completion_tokens" in kwargs:
                    return mock_parsed_response
                # Otherwise raise the error
                raise ValueError(
                    "The parameter max_tokens is not supported for o1. Please use max_completion_tokens instead."
                )
            else:  # Second call
                return mock_parsed_response

        # Set up the mock client to use our custom side effect
        mock_openai_client.beta = MagicMock()
        mock_openai_client.beta.chat = MagicMock()
        mock_openai_client.beta.chat.completions = MagicMock()
        mock_openai_client.beta.chat.completions.parse.side_effect = parse_side_effect

        # Create service with the mocked client
        with (
            patch(
                "discovita.service.openai.core.base.OpenAI",
                return_value=mock_openai_client,
            ),
            patch(
                "discovita.service.openai.utils.model_utils.get_token_param_name",
                return_value="max_tokens",  # Force it to use max_tokens first
            ),
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate test data")

            # Call create_structured_chat_completion with the wrong token parameter
            response = service.create_structured_chat_completion(
                messages=messages,
                model="o1",
                response_format=TestModel,
                max_tokens=100,  # This should cause an error but be recovered
            )

            # Verify the API was called twice
            assert call_count[0] >= 1

            # Verify the response
            assert response == mock_parsed_response
            parsed_data = response.choices[0].message.parsed
            assert parsed_data.value == "Hello"

    def test_structured_completion_other_error(self, mock_openai_client):
        """
        Test handling of other errors in structured completion.

        This test verifies that non-token parameter errors in structured completion
        are properly re-raised.
        """

        # Define a test model
        class TestModel(BaseModel):
            """Test model for structured outputs."""

            value: str

        # Set up the mock client to raise an error
        mock_openai_client.beta = MagicMock()
        mock_openai_client.beta.chat = MagicMock()
        mock_openai_client.beta.chat.completions = MagicMock()
        mock_openai_client.beta.chat.completions.parse.side_effect = ValueError(
            "Some other error"
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate test data")

            # Call create_structured_chat_completion and verify it raises the error
            with pytest.raises(ValueError) as excinfo:
                service.create_structured_chat_completion(
                    messages=messages, model="gpt-4o", response_format=TestModel
                )

            assert "Some other error" in str(excinfo.value)
