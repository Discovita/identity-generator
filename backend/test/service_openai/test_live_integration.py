"""
Live integration tests for the OpenAI service.

This module contains tests that make actual API calls to OpenAI.
These tests are skipped by default and should only be run when
explicitly enabled with the --run-api-tests flag.

To run these tests:
    pytest test_live_integration.py -v --run-api-tests
"""

import os
import tempfile
from typing import Any, Dict, List, Optional

import pytest
from discovita.service.openai_service import AIModel, OpenAIService
from pydantic import BaseModel, Field

# Mark all tests in this module with the 'requires_api' mark
pytestmark = pytest.mark.requires_api


# Define a fixture to check if an API key is available
@pytest.fixture(scope="module")
def openai_service():
    """
    Create an OpenAIService instance for live testing.

    This fixture checks if the OPENAI_API_KEY environment variable
    is set. If the condition is met, an OpenAIService instance is created.
    """
    # Check if the OPENAI_API_KEY environment variable is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY environment variable is not set")

    # Create and return an OpenAIService instance
    service = OpenAIService(api_key=api_key)
    return service


class TestLiveIntegration:
    """
    Live integration tests for the OpenAI service.

    These tests make actual API calls to OpenAI and should only
    be run when explicitly enabled.
    """

    def test_basic_chat_completion(self, openai_service):
        """
        Test basic chat completion with the live API.

        This test verifies that a simple chat completion request
        is processed correctly by the OpenAI API.
        """
        messages = openai_service.create_messages(prompt="Hello, how are you?")

        response = openai_service.create_chat_completion(
            messages=messages, model="gpt-3.5-turbo"  # Use a cheaper model for testing
        )

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

    def test_json_mode(self, openai_service):
        """
        Test JSON mode with the live API.

        This test verifies that a chat completion request with
        JSON mode is processed correctly by the OpenAI API.
        """
        messages = openai_service.create_messages(
            prompt="List 3 colors as a JSON array with 'colors' as the key"
        )

        response = openai_service.create_chat_completion(
            messages=messages,
            model="gpt-3.5-turbo",  # Use a cheaper model for testing
            json_mode=True,
        )

        assert response is not None
        assert isinstance(response, dict)
        assert "colors" in response
        assert isinstance(response["colors"], list)
        assert len(response["colors"]) == 3

    def test_structured_output(self, openai_service):
        """
        Test structured output with the live API.

        This test verifies that a structured output request
        is processed correctly by the OpenAI API.
        """

        # Define a Pydantic model for testing
        class ColorList(BaseModel):
            """A list of colors."""

            colors: List[str] = Field(
                description="A list of color names", min_length=3, max_length=3
            )

        messages = openai_service.create_messages(
            prompt="List exactly 3 colors. Respond in JSON format."
        )

        response = openai_service.create_chat_completion(
            messages=messages,
            model="gpt-4o",  # Use a model that supports JSON mode
            response_format={"type": "json_object"},
        )

        # Handle response - it's already a dictionary, no need to parse
        if isinstance(response, str):
            # Parse if it's a string (shouldn't happen with JSON mode)
            import json

            response_data = json.loads(response)
        else:
            # Already a dictionary
            response_data = response

        color_list = ColorList(**response_data)

        assert color_list is not None
        assert isinstance(color_list.colors, list)
        assert len(color_list.colors) == 3

    def test_image_input(self, openai_service):
        """
        Test image input with the live API.

        This test verifies that a chat completion request with
        an image input is processed correctly by the OpenAI API.
        """
        # Create a temporary image file (a simple colored square)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            # Write a minimal valid PNG file (1x1 pixel)
            tmp.write(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
            )
            tmp_path = tmp.name

        try:
            messages = openai_service.create_messages(
                prompt="What's in this image?", images=[tmp_path]
            )

            response = openai_service.create_chat_completion(
                messages=messages,
                model="gpt-4o",  # Use the current multi-modal model
            )

            assert response is not None
            assert isinstance(response, str)
            assert len(response) > 0
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_streaming_response(self, openai_service):
        """
        Test streaming response with the live API.

        This test verifies that a streaming response is processed
        correctly by the OpenAI API.
        """
        messages = openai_service.create_messages(prompt="Count from 1 to 5")

        # Get the streaming response
        stream = openai_service.create_chat_completion(
            messages=messages,
            model="gpt-3.5-turbo",  # Use a cheaper model for testing
            stream=True,
        )

        # Collect the chunks
        chunks = []
        full_text = ""
        for chunk in stream:
            chunks.append(chunk)
            if (
                hasattr(chunk.choices[0].delta, "content")
                and chunk.choices[0].delta.content
            ):
                full_text += chunk.choices[0].delta.content

        # Verify the response
        assert len(chunks) > 0
        assert full_text is not None
        assert len(full_text) > 0
        assert "1" in full_text and "5" in full_text
