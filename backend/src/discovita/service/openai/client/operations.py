"""OpenAI API operations."""

from typing import List, Dict, Any
from openai import AsyncOpenAI, APIError
from pydantic import AnyHttpUrl
from discovita.service.openai.client import logging
from discovita.service.openai.models import (
    ImageGenerationRequest,
    ImageResponse,
    GeneratedImage,
    OpenAIError,
    VisionRequest,
    CompletionRequest,
    ChatMessage,
    ChatResponse,
    SafeImageResponse
)

async def describe_image_with_vision(
    client: AsyncOpenAI,
    image_url: AnyHttpUrl,
    prompt: str
) -> str:
    """Get a description of an image using GPT-4 Vision."""
    request = VisionRequest(
        messages=[
            ChatMessage(
                role="system",
                content="You are trained to analyze and describe people's physical appearance in images. Your role is to provide detailed, factual descriptions of facial features, hair, and other visible physical characteristics. You should make responsible observations about race, gender, and other physical traits that would be relevant for generating an accurate image of the person."
            ),
            ChatMessage(
                role="user",
                content=[
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": str(image_url)}
                    }
                ]
            )
        ]
    )
    
    logging.log_request("vision", **request.model_dump())
    response = await client.chat.completions.create(**request.model_dump())
    logging.log_response("vision", response)
    return ChatResponse.from_openai_response(response).content

async def get_completion(
    client: AsyncOpenAI,
    prompt: str
) -> str:
    """Get a completion from GPT-4o."""
    request = CompletionRequest(
        messages=[ChatMessage(
            role="user",
            content=prompt
        )]
    )
    
    logging.log_request("completion", **request.model_dump())
    response = await client.chat.completions.create(**request.model_dump())
    logging.log_response("completion", response)
    return ChatResponse.from_openai_response(response).content

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
    # Extract revised_prompt from OpenAI's response
    return ImageResponse(
        created=int(response.created),
        data=[
            GeneratedImage(
                url=str(img.url),  # Ensure url is str
                revised_prompt=getattr(img, "revised_prompt", prompt)  # Fallback to original prompt
            )
            for img in response.data
        ]
    )

async def safe_generate_image(
    client: AsyncOpenAI,
    api_key: str,
    prompt: str,
) -> SafeImageResponse:
    """Generate an image with safety handling."""
    try:
        response = await generate_image(client, api_key, prompt)
        return SafeImageResponse(
            success=True,
            original_prompt=prompt,
            error=None,
            safety_violation=False,
            cleaned_prompt=None,
            data=response
        )
    except APIError as e:
        error_str = str(e)
        if "safety system" in error_str:
            # Clean the prompt using GPT-4
            system_prompt = """You are an AI that helps make image generation prompts safe and appropriate. 
            Rewrite the following prompt to remove any content that might violate content policies 
            while preserving the core intent. Focus on making the prompt family-friendly and non-violent.
            
            Original prompt: """
            
            try:
                cleaned_prompt = await get_completion(client, system_prompt + prompt)
                # Try again with cleaned prompt
                try:
                    response = await generate_image(client, api_key, cleaned_prompt)
                    return SafeImageResponse(
                        success=True,
                        data=response,
                        original_prompt=prompt,
                        error=None,
                        safety_violation=True,
                        cleaned_prompt=cleaned_prompt
                    )
                except APIError as retry_error:
                    return SafeImageResponse(
                        success=False,
                        error=str(retry_error),
                        safety_violation=True,
                        original_prompt=prompt,
                        data=None,
                        cleaned_prompt=cleaned_prompt
                    )
            except APIError as clean_error:
                return SafeImageResponse(
                    success=False,
                    error=str(clean_error),
                    safety_violation=True,
                    original_prompt=prompt,
                    cleaned_prompt=None,
                    data=None
                )
        return SafeImageResponse(
            success=False,
            error=error_str,
            original_prompt=prompt,
            safety_violation=False,
            cleaned_prompt=None,
            data=None
        )
