"""
Tests for the message creation functionality of OpenAIService.

This module tests the message creation capabilities of the OpenAIService,
including text messages, system messages, and messages with image content.
"""

import base64
import os
from unittest.mock import MagicMock, patch

import pytest
from discovita.service.openai import OpenAIService


class TestMessageCreation:
    """
    Tests for message creation in the OpenAIService.

    These tests verify that the service correctly creates
    various types of messages for use with the OpenAI API.
    """

    # Removed individual message creation tests since create_message doesn't exist

    def test_create_messages_with_prompt(self):
        """
        Test creation of messages with a prompt.

        This test verifies that the create_messages method creates
        a list with a single user message when only a prompt is provided.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            messages = service.create_messages(prompt="Hello world")

            assert len(messages) == 1
            assert messages[0]["role"] == "user"
            assert messages[0]["content"] == "Hello world"

    def test_create_messages_with_system_message(self):
        """
        Test creation of messages with a system message.

        This test verifies that the create_messages method creates
        a list with a system message followed by a user message when
        both a system message and a prompt are provided.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            messages = service.create_messages(
                prompt="Hello world", system_message="You are a helpful assistant."
            )

            assert len(messages) == 2
            assert messages[0]["role"] == "system"
            assert messages[0]["content"] == "You are a helpful assistant."
            assert messages[1]["role"] == "user"
            assert messages[1]["content"] == "Hello world"

    def test_create_message_with_image(self, temp_image_file):
        """
        Test creation of a message with an image.

        This test verifies that a message with an image is created
        correctly with the user role and a multimodal content structure.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            message = service.create_messages(
                prompt="Describe this image", images=[temp_image_file]
            )[
                0
            ]  # Get the first (and only) message

            # Verify the message has the correct structure
            assert message["role"] == "user"
            assert isinstance(message["content"], list)
            assert len(message["content"]) == 2

            # Verify the text part
            assert message["content"][0]["type"] == "text"
            assert message["content"][0]["text"] == "Describe this image"

            # Verify the image part - don't check the exact base64 content
            assert message["content"][1]["type"] == "image_url"
            assert "image_url" in message["content"][1]
            assert "url" in message["content"][1]["image_url"]
            assert message["content"][1]["image_url"]["url"].startswith(
                "data:image/jpeg;base64,"
            )

    def test_create_message_with_multiple_images(self, temp_image_file):
        """
        Test creation of a message with multiple images.

        This test verifies that a message with multiple images is created
        correctly with the user role and a multimodal content structure.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            # Create a message with multiple images
            message = service.create_messages(
                prompt="Describe these images",
                images=[temp_image_file, temp_image_file],  # Use the same file twice
            )[
                0
            ]  # Get the first (and only) message

            # Verify the message has the correct structure
            assert message["role"] == "user"
            assert isinstance(message["content"], list)
            assert len(message["content"]) == 3  # Text + 2 images

            # Verify the text part
            assert message["content"][0]["type"] == "text"
            assert message["content"][0]["text"] == "Describe these images"

            # Verify the image parts - don't check the exact base64 content
            assert message["content"][1]["type"] == "image_url"
            assert "image_url" in message["content"][1]
            assert "url" in message["content"][1]["image_url"]
            assert message["content"][1]["image_url"]["url"].startswith(
                "data:image/jpeg;base64,"
            )

            assert message["content"][2]["type"] == "image_url"
            assert "image_url" in message["content"][2]
            assert "url" in message["content"][2]["image_url"]
            assert message["content"][2]["image_url"]["url"].startswith(
                "data:image/jpeg;base64,"
            )

    def test_create_message_with_image_url(self):
        """
        Test creation of a message with an image URL.

        This test verifies that a message with an image URL is created
        correctly with the user role and a multimodal content structure.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            image_url = "https://example.com/image.jpg"

            message = service.create_messages(
                prompt="Describe this image", images=[image_url]
            )[
                0
            ]  # Get the first (and only) message

            # Verify the message has the correct structure
            assert message["role"] == "user"
            assert isinstance(message["content"], list)
            assert len(message["content"]) == 2

            # Verify the text part
            assert message["content"][0]["type"] == "text"
            assert message["content"][0]["text"] == "Describe this image"

            # Verify the image part
            assert message["content"][1]["type"] == "image_url"
            assert message["content"][1]["image_url"]["url"] == image_url

    def test_create_text_and_image_messages(self, temp_image_file):
        """
        Test creation of multiple messages including text and image messages.

        This test verifies that the create_messages method correctly
        creates a sequence of messages including text and image messages.
        """
        with patch("discovita.service.openai.core.base.OpenAI"):
            service = OpenAIService(api_key="test_api_key")

            # Create a system message and a user message with an image
            messages = service.create_messages(
                prompt="Describe this image",
                system_message="You are a helpful assistant.",
                images=[temp_image_file],
            )

            # Verify there are two messages
            assert len(messages) == 2

            # Verify the system message
            assert messages[0]["role"] == "system"
            assert messages[0]["content"] == "You are a helpful assistant."

            # Verify the user message with image - don't check the exact base64 content
            assert messages[1]["role"] == "user"
            assert isinstance(messages[1]["content"], list)
            assert messages[1]["content"][0]["type"] == "text"
            assert messages[1]["content"][0]["text"] == "Describe this image"
            assert messages[1]["content"][1]["type"] == "image_url"
            assert "image_url" in messages[1]["content"][1]
            assert "url" in messages[1]["content"][1]["image_url"]
            assert messages[1]["content"][1]["image_url"]["url"].startswith(
                "data:image/jpeg;base64,"
            )
