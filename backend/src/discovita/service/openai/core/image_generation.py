"""Service for generating images using OpenAI."""

from ..models.image_models import ImageResponse, SafeImageResponse
from .base import OpenAIService


class ImageGenerationService:
    """Service for generating images using OpenAI."""

    def __init__(self, open_ai_service: OpenAIService):
        """
        Initialize the service with an OpenAIService instance.

        Parameters
        ----------
        open_ai_service : OpenAIService
            OpenAIService instance for making API calls
        """
        self.open_ai_service = open_ai_service

    def generate_scene(
        self,
        setting: str,
        outfit: str,
        emotion: str,
        user_description: str | None = None,
        user_feedback: str | None = None,
        previous_augmented_prompt: str | None = None,
    ) -> ImageResponse:
        """
        Generate a scene based on user input.

        Parameters
        ----------
        setting : str
            The setting or location for the scene
        outfit : str
            Description of what the person is wearing
        emotion : str
            The emotion the person should express
        user_description : str, optional
            Description of the person's appearance
        user_feedback : str, optional
            User feedback from a previous generation
        previous_augmented_prompt : str, optional
            The prompt used in the previous generation

        Returns
        -------
        ImageResponse
            The generated image data
        """
        # Build base prompt including user description if available
        person_desc = (
            f"a person with {user_description}" if user_description else "a person"
        )
        base_prompt = f"A photo of {person_desc} in {setting}, wearing {outfit}, expressing {emotion}. Make sure the scene prominently features a person with these physical characteristics. Make it a realistic, colored, photo-quality image."

        if user_feedback and previous_augmented_prompt:
            # If we have feedback and a previous prompt, use those for refinement
            # Emphasize the user feedback by putting it first and making it a requirement
            prompt = f"""IMPORTANT REQUIREMENTS FROM USER: {user_feedback}

Based on these requirements, generate a new version of this scene:
{previous_augmented_prompt}

The above description should be modified to strongly emphasize and incorporate the user's requirements."""
        else:
            prompt = base_prompt

        # Generate the image using OpenAIService
        result = self.open_ai_service.generate_image(
            prompt=prompt, model="dall-e-3", size="1024x1024", quality="hd"
        )

        # Convert to expected response format
        if result and len(result) > 0:
            image_data = result[0]
            return ImageResponse(
                url=image_data.get("url", ""),
                revised_prompt=image_data.get("revised_prompt", ""),
            )

        return ImageResponse(url="", revised_prompt="")

    def safe_generate_scene(
        self,
        setting: str,
        outfit: str,
        emotion: str,
        user_description: str | None = None,
        user_feedback: str | None = None,
        previous_augmented_prompt: str | None = None,
    ) -> SafeImageResponse:
        """
        Generate a scene based on user input with safety handling.

        Parameters
        ----------
        setting : str
            The setting or location for the scene
        outfit : str
            Description of what the person is wearing
        emotion : str
            The emotion the person should express
        user_description : str, optional
            Description of the person's appearance
        user_feedback : str, optional
            User feedback from a previous generation
        previous_augmented_prompt : str, optional
            The prompt used in the previous generation

        Returns
        -------
        SafeImageResponse
            The generated image data with safety handling
        """
        try:
            # Build base prompt including user description if available
            person_desc = (
                f"a person with {user_description}" if user_description else "a person"
            )
            base_prompt = f"A photo of {person_desc} in {setting}, wearing {outfit}, expressing {emotion}. Make sure the scene prominently features a person with these physical characteristics. Make it a realistic, colored, photo-quality image."

            if user_feedback and previous_augmented_prompt:
                # If we have feedback and a previous prompt, use those for refinement
                # Emphasize the user feedback by putting it first and making it a requirement
                prompt = f"""IMPORTANT REQUIREMENTS FROM USER: {user_feedback}

Based on these requirements, generate a new version of this scene:
{previous_augmented_prompt}

The above description should be modified to strongly emphasize and incorporate the user's requirements."""
            else:
                prompt = base_prompt

            # Generate the image using OpenAIService
            result = self.open_ai_service.generate_image(
                prompt=prompt, model="dall-e-3", size="1024x1024", quality="hd"
            )

            # Convert to expected response format
            if result and len(result) > 0:
                image_data = result[0]
                return SafeImageResponse(
                    success=True,
                    url=image_data.get("url", ""),
                    revised_prompt=image_data.get("revised_prompt", ""),
                    error=None,
                )

            return SafeImageResponse(
                success=False, url="", revised_prompt="", error="No image was generated"
            )

        except Exception as e:
            # Handle any errors during generation
            return SafeImageResponse(
                success=False, url="", revised_prompt="", error=str(e)
            )
