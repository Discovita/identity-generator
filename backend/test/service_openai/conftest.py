"""
Common fixtures and configurations for testing the OpenAI Service.

This module provides shared fixtures and configurations for all test modules,
including mock responses, test data, and utility functions.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest


# Define a custom marker for tests requiring an API key
# These tests will be skipped by default unless --run-api-tests is passed to pytest
def pytest_addoption(parser):
    """Add command-line options for the test suite."""
    parser.addoption(
        "--run-api-tests",
        action="store_true",
        default=False,
        help="Run tests that require an API key",
    )


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers",
        "requires_api: mark test as requiring API access (skipped by default)",
    )


# Skip tests marked with requires_api unless --run-api-tests is specified
def pytest_collection_modifyitems(config, items):
    """Skip API-dependent tests unless explicitly enabled."""
    if not config.getoption("--run-api-tests"):
        skip_api = pytest.mark.skip(reason="Need --run-api-tests option to run")
        for item in items:
            if "requires_api" in item.keywords:
                item.add_marker(skip_api)


# Mock OpenAI API Response Fixtures
@pytest.fixture
def mock_chat_completion_response():
    """Create a mock OpenAI chat completion API response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "Test response content"
    mock_response.model = "gpt-4o"
    mock_response.usage = MagicMock()
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    return mock_response


@pytest.fixture
def mock_json_completion_response():
    """Create a mock OpenAI JSON mode API response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = (
        '{"result": "success", "data": [1, 2, 3]}'
    )
    mock_response.model = "gpt-4o"
    return mock_response


@pytest.fixture
def mock_streaming_response():
    """Create a mock OpenAI streaming API response."""
    chunk1 = MagicMock()
    chunk1.choices = [MagicMock()]
    chunk1.choices[0].delta = MagicMock()
    chunk1.choices[0].delta.content = "Hello"

    chunk2 = MagicMock()
    chunk2.choices = [MagicMock()]
    chunk2.choices[0].delta = MagicMock()
    chunk2.choices[0].delta.content = " world"

    chunk3 = MagicMock()
    chunk3.choices = [MagicMock()]
    chunk3.choices[0].delta = MagicMock()
    chunk3.choices[0].delta.content = None

    return [chunk1, chunk2, chunk3]


@pytest.fixture
def mock_structured_response():
    """Create a mock OpenAI structured output API response."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = None
    mock_response.choices[0].message.tool_calls = [MagicMock()]
    mock_response.choices[0].message.tool_calls[0].function = MagicMock()
    mock_response.choices[0].message.tool_calls[0].function.name = "get_result"
    mock_response.choices[0].message.tool_calls[
        0
    ].function.arguments = '{"result": "success", "data": [1, 2, 3]}'
    return mock_response


@pytest.fixture
def mock_openai_client():
    """Create a fully mocked OpenAI client with all necessary methods."""
    with patch("openai.OpenAI") as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Set up chat completions
        mock_client.chat = MagicMock()
        mock_client.chat.completions = MagicMock()
        mock_client.chat.completions.create = MagicMock()

        return mock_client


@pytest.fixture
def temp_image_file():
    """Create a temporary image file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp.write(b"fake image data")
        tmp_path = tmp.name

    yield tmp_path

    # Clean up
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
