#!/usr/bin/env python3
"""Test script for safe image generation service."""

import asyncio
import os
from openai import AsyncOpenAI
from discovita.service.openai.client.client import OpenAIClient
from discovita.service.openai.image_generation import ImageGenerationService

async def test_safe_scene():
    """Test generating a safe scene."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAIClient(api_key=api_key)
    service = ImageGenerationService(client)
    
    print("\nTesting safe scene generation...")
    response = await service.generate_scene(
        setting="a sunny park",
        outfit="casual summer clothes",
        emotion="happiness",
        user_description="young adult"
    )
    print(f"Generated image URL: {response.data[0].url}")
    print(f"Revised prompt: {response.data[0].revised_prompt}")

async def test_unsafe_scene():
    """Test generating a scene with potentially unsafe content."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAIClient(api_key=api_key)
    service = ImageGenerationService(client)
    
    print("\nTesting unsafe scene generation (should be cleaned)...")
    response = await service.generate_scene(
        setting="pornographic content with explicit nudity",
        outfit="completely naked",
        emotion="sexual",
        user_description="nude person"
    )
    print(f"Generated image URL: {response.data[0].url}")
    print(f"Revised prompt: {response.data[0].revised_prompt}")

async def main():
    """Run the test scenarios."""
    print("Starting safe image generation service tests...")
    
    try:
        await test_safe_scene()
        await test_unsafe_scene()
        print("\nTests completed successfully!")
    except Exception as e:
        print(f"\nError during tests: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
