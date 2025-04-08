"""
Vision API functionality for image analysis.

This module provides functions for analyzing images using the OpenAI Vision API.
"""

import logging
from typing import Any

log = logging.getLogger(__name__)


def describe_image_with_vision(client: Any, image_url: str, prompt: str) -> str:
    """
    Get a description of an image using GPT-4 Vision.

    Parameters
    ----------
    client : OpenAI client
        The OpenAI client instance to use for the API call
    image_url : str
        URL of the image to analyze
    prompt : str
        Specific instructions for the vision model when analyzing the image

    Returns
    -------
    str
        Description of the image based on the provided prompt

    Notes
    -----
    - Uses GPT-4 Vision to analyze images
    - The default system prompt instructs the model to provide detailed physical descriptions
    - This is particularly useful for analyzing headshots and portraits
    """
    system_message = (
        "You are trained to analyze and describe people's physical appearance in images. "
        "Your role is to provide detailed, factual descriptions of facial features, hair, "
        "and other visible physical characteristics. You should make responsible observations "
        "about race, gender, and other physical traits that would be relevant for generating "
        "an accurate image of the person."
    )

    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        },
    ]

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4-vision-preview", messages=messages, max_tokens=300
    )

    # Extract the content from the response
    if hasattr(response, "choices") and len(response.choices) > 0:
        return response.choices[0].message.content

    return "Failed to extract description from image."
