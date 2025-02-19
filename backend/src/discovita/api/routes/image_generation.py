"""Image generation route handlers."""

from fastapi import APIRouter, Depends
from ...models import GenerateImageRequest, GenerateImageResponse
from ...service.openai.image_generation import ImageGenerationService
from ..dependencies import get_image_generation_service

router = APIRouter()

@router.post("/generate", response_model=GenerateImageResponse)
async def generate_scene(
    request: GenerateImageRequest,
    service: ImageGenerationService = Depends(get_image_generation_service)
) -> GenerateImageResponse:
    """Generate an image based on the user's vision."""
    response = await service.safe_generate_scene(
        setting=request.setting,
        outfit=request.outfit,
        emotion=request.emotion,
        user_description=request.userDescription,
        user_feedback=request.userFeedback,
        previous_augmented_prompt=request.previousAugmentedPrompt
    )
    if not response.success:
        raise HTTPException(status_code=500, detail=response.error)
        
    # Get the first generated image
    image = response.data.data[0]
    return GenerateImageResponse(
        imageUrl=image.url,
        augmentedPrompt=image.revised_prompt
    )
