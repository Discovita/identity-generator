"""Tests for error handling in Icons8 client."""

import pytest
from discovita.service.icons8.client.client import Icons8Client
from .mock_response import MockResponse

pytestmark = pytest.mark.asyncio

async def test_no_faces_error() -> None:
    """Test error when no faces are detected."""
    client = Icons8Client(api_key="test-key", base_url="https://api.icons8.com")
    
    # Create mock post function with proper typing
    async def mock_post(url: str, **kwargs) -> MockResponse:
        return MockResponse([
            {
                "img_url": "https://example.com/source.jpg",
                "faces": []
            },
            {
                "img_url": "https://example.com/target.jpg",
                "faces": [
                    {
                        "bbox": [0, 0, 100, 100],
                        "landmarks": [0.0] * 68  # Icons8 uses 68 facial landmarks
                    }
                ]
            }
        ], url="https://api.icons8.com/get_bbox")
    
    # Monkey patch the client's post method
    setattr(client.client, "post", mock_post)
    
    # Verify assertion error is raised
    with pytest.raises(AssertionError, match="No faces detected in source image"):
        await client.swap_faces(
            source_url="https://example.com/source.jpg",
            target_url="https://example.com/target.jpg"
        )
