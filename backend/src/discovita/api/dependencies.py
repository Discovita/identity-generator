"""API dependencies."""

from typing import AsyncGenerator
from fastapi import Depends
from httpx import AsyncClient, Limits, Timeout

from discovita.config import Settings
from discovita.dependencies import get_settings
from discovita.service.coach.prompt.manager import PromptManager
from discovita.service.coach.service import CoachService
from discovita.service.coach.state.machine import StateMachine
from discovita.service.openai.client.client import OpenAIClient
from discovita.service.openai.image_description import ImageDescriptionService
from discovita.service.openai.image_generation import ImageGenerationService

async def get_openai_client(
    settings: Settings = Depends(get_settings)
) -> OpenAIClient:
    """Get OpenAI client."""
    return OpenAIClient(
        api_key=settings.openai_api_key,
        base_url="https://api.openai.com/v1",
        test_mode=False
    )

async def get_image_description_service(
    client: OpenAIClient = Depends(get_openai_client)
) -> ImageDescriptionService:
    """Get image description service."""
    return ImageDescriptionService(client)

async def get_image_generation_service(
    client: OpenAIClient = Depends(get_openai_client)
) -> ImageGenerationService:
    """Get image generation service."""
    return ImageGenerationService(client)

async def get_coach_service(
    client: OpenAIClient = Depends(get_openai_client)
) -> CoachService:
    """Get coach service."""
    prompt_manager = PromptManager()
    state_machine = StateMachine()
    return CoachService(client, prompt_manager, state_machine)
