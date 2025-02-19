#!/usr/bin/env python3
"""Test script for image generation endpoint."""

from dataclasses import dataclass
from typing import Optional
import httpx
import asyncio
import json

@dataclass
class GenerateImageRequest:
    setting: str
    outfit: str
    emotion: str
    userFeedback: Optional[str] = None
    previousAugmentedPrompt: Optional[str] = None

@dataclass
class GenerateImageResponse:
    imageUrl: str
    augmentedPrompt: str

async def test_generate_image() -> None:
    """Test the image generation endpoint."""
    print("Starting image generation test...")
    
    request = GenerateImageRequest(
        setting="a modern office with floor-to-ceiling windows",
        outfit="a professional business suit",
        emotion="confident and successful"
    )
    
    print("\nRequest payload:")
    print(json.dumps({
        "setting": request.setting,
        "outfit": request.outfit,
        "emotion": request.emotion,
        "userFeedback": request.userFeedback,
        "previousAugmentedPrompt": request.previousAugmentedPrompt
    }, indent=2))
    
    timeout = httpx.Timeout(timeout=120.0)  # 2 minutes total timeout
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        try:
            print("\nSending request to server...")
            response = await client.post(
                "http://localhost:8000/api/v1/generate",
                json={
                    "setting": request.setting,
                    "outfit": request.outfit,
                    "emotion": request.emotion,
                    "userFeedback": request.userFeedback,
                    "previousAugmentedPrompt": request.previousAugmentedPrompt
                }
            )
            
            print(f"\nStatus Code: {response.status_code}")
            print("Response Headers:")
            print(json.dumps(dict(response.headers), indent=2))
            print("\nRaw Response Content:")
            print(response.text)
            
            if response.status_code == 200:
                print("\nParsed JSON Response:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"\nError: Non-200 status code received: {response.status_code}")
                if response.text:
                    print("Error details:", response.text)
                
        except httpx.TimeoutException as e:
            print(f"Request timed out: {str(e)}")
        except httpx.RequestError as e:
            print(f"Request failed: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_generate_image())
