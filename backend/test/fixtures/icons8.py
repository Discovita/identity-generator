"""Test fixtures for Icons8 client tests."""

import pytest
from discovita.service.icons8.models import ProcessStatus

@pytest.fixture
def mock_landmarks_response() -> dict:
    """Mock response for get_landmarks endpoint."""
    return {
        "__root__": [
            {
                "img_url": "https://example.com/source.jpg",
                "faces": [
                    {
                        "bbox": [10, 20, 100, 100, 0.9],  # Small face, high confidence
                        "landmarks": [1, 2, 3, 4]
                    },
                    {
                        "bbox": [30, 40, 200, 200, 0.7],  # Large face, medium confidence - should be selected due to higher relevance (area * confidence)
                        "landmarks": [5, 6, 7, 8]
                    }
                ]
            },
            {
                "img_url": "https://example.com/target.jpg",
                "faces": [
                    {
                        "bbox": [50, 60, 150, 150, 0.95],  # Medium face, highest confidence
                        "landmarks": [9, 10, 11, 12]
                    },
                    {
                        "bbox": [70, 80, 300, 300, 0.8],  # Largest face, high confidence - should be selected due to highest relevance
                        "landmarks": [13, 14, 15, 16]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def mock_swap_response() -> dict:
    """Mock response for face swap endpoint."""
    return {
        "id": "test-job-id",
        "processed": {
            "width": 800,
            "height": 600,
            "type": "jpeg",
            "url": "https://example.com/result.jpg"
        },
        "status": ProcessStatus.READY,
        "statusName": "ready"
    }
