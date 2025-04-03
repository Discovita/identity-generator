"""
Mixin for image generation functionality in OpenAIService.

This mixin provides methods for generating images using OpenAI's DALL-E models.
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union

from ...models.image import ImageModel, ImageSize
from ...utils.image import encode_image
from .response import process_image_response
from .utils import save_generated_image
from .validation import validate_and_process_image_params
from .vision import describe_image_with_vision

log = logging.getLogger(__name__)


class ImageGenerationMixin:
    """Mixin providing image generation functionality for OpenAIService."""

    def encode_image_for_api(self, image_path: str) -> str:
        """Encode an image for use with OpenAI's API."""
        return encode_image(image_path)

    def generate_image(
        self,
        prompt: str,
        model: Union[str, ImageModel] = None,
        n: Optional[int] = None,
        size: Optional[Union[str, ImageSize]] = None,
        quality: Optional[Union[str, Literal["standard", "hd"]]] = None,
        style: Optional[Union[str, Literal["vivid", "natural"]]] = None,
        response_format: Optional[Union[str, Literal["url", "b64_json"]]] = None,
        save_to_path: Optional[str] = None,
        user: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate images from a text prompt using DALL-E models.
        See https://platform.openai.com/docs/api-reference/images/create for param details.

        Returns
        -------
        List[Dict[str, Any]]
            List of generated image data. Each item contains:
            - url (if response_format is "url")
            - b64_json (if response_format is "b64_json")
            - revised_prompt (DALL-E 3 only)
            - local_path (if save_to_path is provided)

        Notes
        -----
        - DALL-E 3 automatically revises prompts for safety and quality
        - DALL-E 3 only supports generating one image at a time (n=1)
        - URL responses expire after 1 hour
        """
        # Validate and process parameters
        params = validate_and_process_image_params(
            prompt=prompt,
            model=model,
            n=n,
            size=size,
            quality=quality,
            style=style,
            response_format=response_format,
            save_to_path=save_to_path,
            user=user,
        )

        # Make API call
        response = self.client.images.generate(**params)

        # Process response and save images if needed
        return process_image_response(
            response=response,
            save_to_path=save_to_path,
            save_image_func=save_generated_image,
        )

    def describe_image_with_vision(
        self,
        image_url: str,
        prompt: str = "Describe this person's physical appearance in detail. Focus on their facial features, hair, and any distinctive characteristics. In particular, race and gender can and should be included in the description.",
    ) -> str:
        """
        Get a description of an image using GPT-4 Vision.
        """
        return describe_image_with_vision(self.client, image_url, prompt)
