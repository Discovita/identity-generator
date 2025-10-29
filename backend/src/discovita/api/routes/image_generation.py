"""Image generation route handlers."""

import logging
from fastapi import APIRouter, Depends, HTTPException

from ...models import GenerateImageRequest, GenerateImageResponse
from ...service.openai.core.image_generation import ImageGenerationService
from ..dependencies import get_image_generation_service

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/generate", response_model=GenerateImageResponse)
async def generate_scene(
    request: GenerateImageRequest,
    service: ImageGenerationService = Depends(get_image_generation_service),
) -> GenerateImageResponse:
    """Generate an image based on the user's vision."""
    response = service.safe_generate_scene(
        setting=request.setting,
        outfit=request.outfit,
        emotion=request.emotion,
        user_description=request.userDescription,
        user_feedback=request.userFeedback,
        previous_augmented_prompt=request.previousAugmentedPrompt,
    )

    if response.data is None:
        log.error(f"Image generation returned None data. Response: {response}")
        raise HTTPException(status_code=500, detail="An unknown error occurred during image generation")

    image = response.data.data[0]
    return GenerateImageResponse(
        imageUrl=image.url, augmentedPrompt=image.revised_prompt
    )
