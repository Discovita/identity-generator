"""Service for getting clean descriptions of headshot images."""

from pydantic import AnyHttpUrl

from .base import OpenAIService


class ImageDescriptionService:
    """Service for getting clean descriptions of headshot images."""

    def __init__(self, client: OpenAIService):
        """
        Initialize the service with an OpenAIService client.

        Parameters
        ----------
        client : OpenAIService
            OpenAIService instance for making API calls
        """
        self.client = client

    async def get_clean_description(self, image_url: AnyHttpUrl) -> str:
        """
        Get a clean description of a headshot image.

        This is a two-step process:
        1. Get a detailed description using GPT-4 Vision
        2. Clean up the description using GPT-4o to remove irrelevant details

        Parameters
        ----------
        image_url : AnyHttpUrl
            URL of the headshot image to analyze

        Returns
        -------
        str
            Clean, focused description of the person's physical appearance
        """
        # Step 1: Get initial description using the vision API
        initial_description = self.client.describe_image_with_vision(
            str(image_url),
            "Describe this person's physical appearance in detail. Focus on "
            + "their facial features, hair, and any distinctive characteristics. In particular, race and gender can and should be included in the description.",
        )

        # Step 2: Clean up description using regular chat completion
        clean_description = self.client.get_completion(
            f"""Clean up this description of a person by removing any irrelevant details about pose, background, or setting. 
            Keep only physical characteristics of the person that would be relevant for generating a new image of them.
            In particular, race and gender description should be retained.
            
            Description: {initial_description}"""
        )

        return clean_description
