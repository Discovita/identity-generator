"""
Message utility functions for OpenAI API interactions.

This module provides utility functions for working with chat messages
in the format expected by OpenAI's API.
"""

import logging
from typing import Any, List, Optional

from discovita.service.openai.utils.image import encode_image
from openai.types.chat import ChatCompletionContentPartParam, ChatCompletionMessageParam

log = logging.getLogger(__name__)


def create_messages(
    prompt: str = None,
    system_message: Optional[str] = None,
    images: Optional[List[str]] = None,
    messages: Optional[List[Any]] = None,
) -> List[ChatCompletionMessageParam]:
    """
    Create a list of messages for the chat completion API.

    This function formats the user prompt, system message, and images
    into the format expected by OpenAI's API.

    Parameters
    ----------
        system_message : Optional system message to set context
        prompt : The user prompt/query text (not required if messages is provided)
        images : Optional list of image paths or URLs to include
        messages : Optional list of Message objects with role and content attributes

    Returns
    -------
        Formatted messages ready for API use
    """
    result_messages = []

    # Add system message if provided
    if system_message:
        result_messages.append({"role": "system", "content": system_message})

    # Add messages from history if provided
    if messages:
        for msg in messages:
            # Convert "coach" role to "assistant" for OpenAI API compatibility
            role = "assistant" if msg.role == "coach" else msg.role
            result_messages.append({"role": role, "content": msg.content})

    # Add new prompt if provided
    if prompt:
        if images:
            content_parts: List[ChatCompletionContentPartParam] = []

            content_parts.append({"type": "text", "text": prompt})

            for image_path in images:
                log.debug(f"Adding image from {image_path} to request")
                try:
                    if image_path.startswith(("http://", "https://")):
                        image_url = image_path
                    else:
                        image_url = encode_image(image_path)

                    content_parts.append(
                        {"type": "image_url", "image_url": {"url": image_url}}
                    )
                except Exception as e:
                    log.error(f"Failed to encode image {image_path}: {str(e)}")
                    continue

            result_messages.append({"role": "user", "content": content_parts})
        else:
            result_messages.append({"role": "user", "content": prompt})

    return result_messages
