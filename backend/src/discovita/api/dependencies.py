"""API dependencies."""

from discovita.config import Settings
from discovita.dependencies import get_settings
from discovita.service.coach.prompt.manager import PromptManager
from discovita.service.coach.service import CoachService
from discovita.service.openai.core import OpenAIService
from discovita.service.openai.core.image_description import ImageDescriptionService
from discovita.service.openai.core.image_generation import ImageGenerationService
from fastapi import Depends


async def get_openai_client(
    settings: Settings = Depends(get_settings),
) -> OpenAIService:
    """Get OpenAI client."""
    return OpenAIService(
        api_key=settings.openai_api_key,
    )


async def get_image_description_service(
    client: OpenAIService = Depends(get_openai_client),
) -> ImageDescriptionService:
    """Get image description service."""
    return ImageDescriptionService(client)


async def get_image_generation_service(
    client: OpenAIService = Depends(get_openai_client),
) -> ImageGenerationService:
    """Get image generation service."""
    return ImageGenerationService(client)


async def get_coach_service(
    client: OpenAIService = Depends(get_openai_client),
) -> CoachService:
    """Get coach service."""
    prompt_manager = PromptManager()
    return CoachService(client, prompt_manager)
