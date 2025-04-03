"""
Tests for structured outputs and JSON mode in OpenAIService.

This module tests the structured output capabilities of OpenAIService,
including JSON mode, Pydantic schema validation, and function calling.
"""

import json
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest
from discovita.service.openai import AIModel, OpenAIService
from pydantic import BaseModel, Field


class TestStructuredOutputs:
    """
    Tests for structured outputs in OpenAIService.

    These tests verify that the service correctly handles
    structured outputs, including JSON mode and schema validation.
    """

    def test_json_mode(self, mock_openai_client, mock_json_completion_response):
        """
        Test chat completion with JSON mode.

        This test verifies that JSON mode is correctly enabled
        and that the response is parsed as JSON.
        """
        # Set up the mock to return a JSON response
        mock_openai_client.chat.completions.create.return_value = (
            mock_json_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(
                prompt="List three colors as a JSON array"
            )

            # Call create_chat_completion with JSON mode
            response = service.create_chat_completion(messages=messages, json_mode=True)

            # Verify the response was parsed as JSON
            assert isinstance(response, dict)
            assert "result" in response
            assert response["result"] == "success"
            assert "data" in response
            assert response["data"] == [1, 2, 3]

            # Verify response_format was set correctly
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["response_format"]["type"] == "json_object"

    def test_response_format_with_schema(
        self, mock_openai_client, mock_json_completion_response
    ):
        """
        Test chat completion with response_format parameter and schema.

        This test verifies that a response_format parameter with a schema
        is correctly passed to the API.
        """
        # Set up the mock to return a JSON response
        mock_openai_client.chat.completions.create.return_value = (
            mock_json_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate data as JSON")

            # Define a schema
            schema = {
                "type": "object",
                "properties": {
                    "result": {"type": "string"},
                    "data": {"type": "array", "items": {"type": "integer"}},
                },
                "required": ["result", "data"],
            }

            # Create a response_format object with the schema
            response_format = {"type": "json_object", "schema": schema}

            # Call create_chat_completion with response_format
            response = service.create_chat_completion(
                messages=messages, response_format=response_format
            )

            # Verify the response was parsed as JSON
            assert isinstance(response, dict)
            assert "result" in response
            assert response["result"] == "success"

            # Verify response_format was set correctly
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert "response_format" in call_args
            assert call_args["response_format"]["type"] == "json_object"
            assert "schema" in call_args["response_format"]

    def test_pydantic_model_schema(
        self, mock_openai_client, mock_json_completion_response
    ):
        """
        Test chat completion with a Pydantic model schema.

        This test verifies that a Pydantic model is correctly
        converted to a JSON schema and passed to the API.
        """

        # Define a Pydantic model for testing
        class TestModel(BaseModel):
            """
            A test model for structured outputs.

            This model defines the structure of the expected response from the API,
            including a string result and a list of integer data.
            """

            result: str = Field(description="The result of the operation")
            data: List[int] = Field(description="The data returned by the operation")

        # Set up the mock to return a JSON response
        mock_json_completion_response.choices[0].message.content = (
            '{"result": "success", "data": [1, 2, 3]}'
        )
        mock_openai_client.chat.completions.create.return_value = (
            mock_json_completion_response
        )

        # Create service with the mocked client
        with patch(
            "discovita.service.openai.core.base.OpenAI",
            return_value=mock_openai_client,
        ):
            service = OpenAIService(api_key="test_api_key")

            # Create messages
            messages = service.create_messages(prompt="Generate model data")

            # Call create_chat_completion with the Pydantic model
            response = service.create_chat_completion(
                messages=messages, response_format=TestModel
            )

            # Verify the response was parsed as JSON
            assert isinstance(response, dict)
            assert "result" in response
            assert response["result"] == "success"
            assert "data" in response
            assert response["data"] == [1, 2, 3]

            # Verify response_format was set correctly
            call_args = mock_openai_client.chat.completions.create.call_args[1]
            assert call_args["response_format"]["type"] == "json_object"
            assert "schema" in call_args["response_format"]
            schema = call_args["response_format"]["schema"]
            assert schema["type"] == "object"
            assert schema["title"] == "TestModel"
            assert "result" in schema["properties"]
            assert "data" in schema["properties"]
            assert schema["properties"]["result"]["type"] == "string"
            assert schema["properties"]["data"]["type"] == "array"
            assert schema["properties"]["data"]["items"]["type"] == "integer"
            assert set(schema["required"]) == {"result", "data"}
