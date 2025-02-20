"""OpenAI Image Generation API operations."""

from openai import AsyncOpenAI
from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    ImageGenerationRequest,
    ImageResponse,
    GeneratedImage
)

async def generate_image(
    client: AsyncOpenAI,
    api_key: str,
    prompt: str,
) -> ImageResponse:
    """Generate an image from a text prompt."""
    request = ImageGenerationRequest(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="standard"
    )
    
    logging.log_request("generate_image", **request.model_dump(exclude_none=True))
    response = await client.images.generate(**request.model_dump(exclude_none=True))
    logging.log_response("generate_image", response)
    return ImageResponse(
        created=int(response.created),
        data=[
            GeneratedImage(
                url=str(img.url),
                revised_prompt=getattr(img, "revised_prompt", prompt)
            )
            for img in response.data
        ]
    )
