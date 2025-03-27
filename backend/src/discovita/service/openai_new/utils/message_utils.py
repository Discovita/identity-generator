"""
Message utility functions for OpenAI API interactions.

This module provides utility functions for working with chat messages
in the format expected by OpenAI's API.
"""

import os
from typing import List, Optional

from discovita.utils.logger import configure_logging
from openai.types.chat import ChatCompletionContentPartParam, ChatCompletionMessageParam

log = configure_logging(__name__)

# Import necessary utility functions
from .image import encode_image


def create_messages(
    prompt: str,
    system_message: Optional[str] = None,
    images: Optional[List[str]] = None,
) -> List[ChatCompletionMessageParam]:
    """
    Create a list of messages for the chat completion API.

    This function formats the user prompt, system message, and images
    into the format expected by OpenAI's API.

    Parameters
    ----------
    prompt : str
        The user prompt/query text
    system_message : Optional[str]
        Optional system message to set context
    images : Optional[List[str]]
        Optional list of image paths to include

    Returns
    -------
    List[ChatCompletionMessageParam]
        Formatted messages ready for API use
    """
    messages = []

    # Add system message if provided
    if system_message:
        messages.append({"role": "system", "content": system_message})

    # Process user message based on whether there are images
    if images:
        # Create a multimodal message with text and images
        content_parts: List[ChatCompletionContentPartParam] = []

        # Add the prompt text
        content_parts.append({"type": "text", "text": prompt})

        # Add each image
        for image_path in images:
            # Log that we're adding an image
            log.debug(f"Adding image from {image_path} to request")
            try:
                # Encode the image and add to content parts
                encoded_image = encode_image(image_path)
                content_parts.append(
                    {"type": "image_url", "image_url": {"url": encoded_image}}
                )
            except Exception as e:
                log.error(f"Failed to encode image {image_path}: {str(e)}")
                # Continue with other images if any
                continue

        # Create the multimodal user message
        messages.append({"role": "user", "content": content_parts})
    else:
        # Simple text-only user message
        messages.append({"role": "user", "content": prompt})

    return messages
