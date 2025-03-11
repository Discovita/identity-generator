"""Tests for face selection in Icons8 client."""

import pytest
from discovita.service.icons8.client.client import Icons8Client
from discovita.service.icons8.models import (
    FaceSwapResponse,
    ProcessedImage,
    ProcessStatus,
)
from .mock_response import MockLandmarksResponse, MockSwapResponse
from fixtures.icons8 import mock_landmarks_response, mock_swap_response

pytestmark = pytest.mark.asyncio

async def test_face_selection_in_swap(mock_landmarks_response: list[dict], mock_swap_response: dict) -> None:
    """Test that face swap selects largest faces from source and target images."""
    client = Icons8Client(api_key="test-key", base_url="https://api.icons8.com")
    
    # Create mock post function with proper typing
    async def mock_post(url: str, **kwargs):
        if "/get_bbox" in url:
            return MockLandmarksResponse(mock_landmarks_response, url="https://api.icons8.com/get_bbox")
        return MockSwapResponse(mock_swap_response, url="https://api.icons8.com/process_image")

    # Monkey patch the client's post method
    setattr(client.client, "post", mock_post)
    
    # Perform face swap
    response = await client.swap_faces(
        source_url="https://example.com/source.jpg",
        target_url="https://example.com/target.jpg"
    )
    
    # Verify response
    assert isinstance(response, FaceSwapResponse)
    assert response.id == "test-job-id"
    assert response.status == ProcessStatus.READY
    assert isinstance(response.processed, ProcessedImage)
    assert str(response.processed.url) == "https://example.com/result.jpg"
