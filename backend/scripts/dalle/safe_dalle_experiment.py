#!/usr/bin/env python3
"""Live integration test for safe DALL-E image generation."""

import asyncio
import os
from openai import AsyncOpenAI, APIError

async def safe_image_generation(client: AsyncOpenAI, prompt: str) -> dict:
    """Attempt to generate an image with safety handling."""
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return {
            "success": True,
            "data": response
        }
    except APIError as e:
        if "safety system" in str(e):
            return {
                "success": False,
                "error": str(e),
                "safety_violation": True
            }
        return {
            "success": False,
            "error": str(e),
            "safety_violation": False
        }

async def test_safe_prompt():
    """Test image generation with a safe prompt."""
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("\nTesting safe prompt...")
    prompt = "A cute cartoon puppy playing with a red ball in a sunny park"
    print(f"Prompt: {prompt}")
    
    raw_response = await safe_image_generation(client, prompt)
    print("\nRaw OpenAI Response:")
    print(raw_response)

async def test_unsafe_prompt():
    """Test image generation with an unsafe prompt."""
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("\nTesting unsafe prompt...")
    # Using a prompt that should trigger safety system
    prompt = "Graphic violence with blood and gore"
    print(f"Prompt: {prompt}")
    
    raw_response = await safe_image_generation(client, prompt)
    print("\nRaw OpenAI Response:")
    print(raw_response)

async def main():
    """Run the integration tests."""
    print("Starting DALL-E safety integration tests...")
    
    try:
        await test_safe_prompt()
        await test_unsafe_prompt()
        print("\nTests completed successfully!")
    except Exception as e:
        print(f"\nError during tests: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
