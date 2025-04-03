"""
Tests for the image generation functionality.

This module tests the image generation capabilities of the OpenAIService,
including validation, response processing, and the mixin class functionality.
"""

import base64
import os
import shutil
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from discovita.service.openai_service import OpenAIService
from discovita.service.openai_service.core.image.response import process_image_response
from discovita.service.openai_service.core.image.utils import save_generated_image
from discovita.service.openai_service.core.image.validation import (
    validate_and_process_image_params,
)
from discovita.service.openai_service.models.image import (
    ImageModel,
    ImageQuality,
    ImageResponseFormat,
    ImageSize,
    ImageStyle,
)

# Define a custom marker for tests requiring an API key
# These tests will be skipped by default unless --run-api-tests is passed to pytest
pytest.mark.requires_api = pytest.mark.skipif(
    "not config.getoption('--run-api-tests')",
    reason="Requires --run-api-tests option to run",
)


# ===============================
# Validation Tests
# ===============================
class TestImageValidation:
    """Tests for the image parameter validation functionality."""

    def test_basic_params(self):
        """Test basic parameter processing with minimal inputs."""
        result = validate_and_process_image_params(prompt="test prompt")
        assert result["prompt"] == "test prompt"
        assert "model" in result  # Should use default model

    def test_enum_conversion(self):
        """Test conversion of enum values to strings."""
        result = validate_and_process_image_params(
            prompt="test prompt",
            model=ImageModel.DALL_E_3,
            size=ImageSize.SQUARE_1024,
            quality=ImageQuality.HD,
            style=ImageStyle.VIVID,
            response_format=ImageResponseFormat.B64_JSON,
        )

        assert result["model"] == "dall-e-3"
        assert result["size"] == "1024x1024"
        assert result["quality"] == "hd"
        assert result["style"] == "vivid"
        assert result["response_format"] == "b64_json"

    def test_prompt_truncation_dalle2(self):
        """Test prompt truncation for DALL-E 2."""
        long_prompt = "a" * 1200  # Exceeds DALL-E 2 limit
        result = validate_and_process_image_params(
            prompt=long_prompt, model=ImageModel.DALL_E_2
        )

        assert len(result["prompt"]) == 1000  # Should be truncated

    def test_prompt_truncation_dalle3(self):
        """Test prompt truncation for DALL-E 3."""
        long_prompt = "a" * 5000  # Exceeds DALL-E 3 limit
        result = validate_and_process_image_params(
            prompt=long_prompt, model=ImageModel.DALL_E_3
        )

        assert len(result["prompt"]) == 4000  # Should be truncated

    def test_dalle3_n_restriction(self):
        """Test DALL-E 3 n=1 restriction."""
        result = validate_and_process_image_params(
            prompt="test prompt", model=ImageModel.DALL_E_3, n=5
        )

        assert result["n"] == 1  # Should be forced to 1 for DALL-E 3

    def test_response_format_override(self):
        """Test response_format override when save_to_path is provided."""
        result = validate_and_process_image_params(
            prompt="test prompt", save_to_path="/tmp"
        )

        assert result["response_format"] == "b64_json"  # Should be overridden

    def test_dalle2_ignores_quality_style(self):
        """Test DALL-E 2 ignores quality and style parameters."""
        result = validate_and_process_image_params(
            prompt="test prompt",
            model=ImageModel.DALL_E_2,
            quality=ImageQuality.HD,
            style=ImageStyle.VIVID,
        )

        assert "quality" not in result  # Should be ignored for DALL-E 2
        assert "style" not in result  # Should be ignored for DALL-E 2


# ===============================
# Response Processing Tests
# ===============================
class TestResponseProcessing:
    """Tests for the image response processing functionality."""

    def test_process_empty_response(self):
        """Test processing an empty response."""
        response = MagicMock()
        response.data = []

        result = process_image_response(response)
        assert result == []

    def test_process_url_response(self):
        """Test processing a response with URL data."""
        response = MagicMock()
        img_data = MagicMock()
        img_data.url = "https://example.com/image.png"
        img_data.b64_json = None
        response.data = [img_data]

        result = process_image_response(response)
        assert len(result) == 1
        assert result[0]["url"] == "https://example.com/image.png"

    def test_process_b64_response(self):
        """Test processing a response with base64 data."""
        response = MagicMock()
        img_data = MagicMock()
        img_data.url = None
        img_data.b64_json = "base64data"
        response.data = [img_data]

        result = process_image_response(response)
        assert len(result) == 1
        assert result[0]["b64_json"] == "base64data"

    def test_process_revised_prompt(self):
        """Test processing a response with revised prompt."""
        response = MagicMock()
        img_data = MagicMock()
        img_data.url = "https://example.com/image.png"
        img_data.revised_prompt = "Revised prompt text"
        response.data = [img_data]

        result = process_image_response(response)
        assert len(result) == 1
        assert result[0]["revised_prompt"] == "Revised prompt text"

    def test_save_image_callback(self):
        """Test the save image callback functionality."""
        response = MagicMock()
        img_data = MagicMock()
        img_data.b64_json = "base64data"
        response.data = [img_data]

        save_func = MagicMock(return_value="/tmp/image.png")

        result = process_image_response(
            response, save_to_path="/tmp", save_image_func=save_func
        )

        save_func.assert_called_once()
        assert result[0]["local_path"] == "/tmp/image.png"


# ===============================
# Utility Tests
# ===============================
class TestImageUtils:
    """Tests for the image utility functions."""

    def test_save_generated_image(self):
        """Test saving a generated image."""
        # Create a simple test image
        test_dir = tempfile.mkdtemp()
        try:
            # Create mock image data
            img_data = MagicMock()
            sample_img_data = base64.b64encode(b"test image data").decode("utf-8")
            img_data.b64_json = sample_img_data

            # Save the image
            result = save_generated_image(img_data, test_dir, 0)

            # Verify the result
            assert result is not None
            assert os.path.exists(result)

            # Check file content
            with open(result, "rb") as f:
                content = f.read()
            assert content == b"test image data"
        finally:
            # Clean up
            shutil.rmtree(test_dir)

    def test_save_generated_image_no_b64(self):
        """Test saving an image without b64_json data."""
        img_data = MagicMock()
        img_data.b64_json = None

        result = save_generated_image(img_data, "/tmp", 0)
        assert result is None


# ===============================
# Mixin Tests
# ===============================
class TestImageGenerationMixin:
    """Tests for the ImageGenerationMixin class."""

    @patch(
        "discovita.service.openai_service.core.image.mixin.validate_and_process_image_params"
    )
    @patch("discovita.service.openai_service.core.image.mixin.process_image_response")
    def test_generate_image(self, mock_process, mock_validate):
        """Test the generate_image method with mocked dependencies."""
        # Setup mocks
        mock_validate.return_value = {"prompt": "test prompt"}
        mock_process.return_value = [{"url": "https://example.com/image.png"}]

        # Create a mock client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_client.images.generate.return_value = mock_response

        # Create the service with our mock
        service = OpenAIService(api_key="test_key")
        service.client = mock_client

        # Call the method
        result = service.generate_image(
            prompt="test prompt", model=ImageModel.DALL_E_3, size=ImageSize.SQUARE_1024
        )

        # Verify the result
        assert result == [{"url": "https://example.com/image.png"}]

        # Verify mock calls
        mock_validate.assert_called_once()
        mock_client.images.generate.assert_called_once_with(prompt="test prompt")
        mock_process.assert_called_once()

    def test_encode_image_for_api(self):
        """Test the encode_image_for_api method."""
        with patch(
            "discovita.service.openai_service.core.image.mixin.encode_image"
        ) as mock_encode:
            mock_encode.return_value = "base64encoded"

            service = OpenAIService(api_key="test_key")
            result = service.encode_image_for_api("image.png")

            assert result == "base64encoded"
            mock_encode.assert_called_once_with("image.png")


# ===============================
# Integration Tests (Mock API)
# ===============================
@pytest.mark.requires_api
class TestImageGenerationIntegration:
    """Integration tests for image generation using mock API responses."""

    def setup_method(self):
        """Set up the test method by creating mock objects."""
        # Create a standard response for all tests
        self.mock_response = MagicMock()
        self.mock_img_data = MagicMock()
        self.mock_img_data.url = "https://example.com/image.png"
        self.mock_img_data.b64_json = "base64data"
        self.mock_img_data.revised_prompt = "Revised prompt"
        self.mock_response.data = [self.mock_img_data]

        # Create a mock OpenAI client
        self.mock_client = MagicMock()
        self.mock_client.images.generate.return_value = self.mock_response

    def test_generate_image_dalle3(self):
        """Test generating an image with DALL-E 3."""
        # Create the service with our mock directly
        service = OpenAIService(api_key="test_key")
        service.client = self.mock_client  # Replace the client directly

        result = service.generate_image(
            prompt="A beautiful landscape",
            model=ImageModel.DALL_E_3,
            size=ImageSize.LANDSCAPE_1792x1024,
            quality=ImageQuality.HD,
            style=ImageStyle.VIVID,
        )

        # Verify the mock was called with the correct parameters
        self.mock_client.images.generate.assert_called_once()
        call_args = self.mock_client.images.generate.call_args[1]
        assert call_args["prompt"] == "A beautiful landscape"
        assert call_args["model"] == "dall-e-3"

        # Verify the result
        assert len(result) == 1
        assert "url" in result[0]
        assert "b64_json" in result[0]
        assert "revised_prompt" in result[0]

    def test_generate_image_dalle2(self):
        """Test generating an image with DALL-E 2."""
        # Create the service with our mock directly
        service = OpenAIService(api_key="test_key")
        service.client = self.mock_client  # Replace the client directly

        result = service.generate_image(
            prompt="A cute cat",
            model=ImageModel.DALL_E_2,
            n=4,
            size=ImageSize.SQUARE_512,
        )

        # Verify the mock was called with the correct parameters
        self.mock_client.images.generate.assert_called_once()
        call_args = self.mock_client.images.generate.call_args[1]
        assert call_args["prompt"] == "A cute cat"
        assert call_args["model"] == "dall-e-2"
        assert call_args["n"] == 4

        # Verify the result
        assert len(result) == 1  # Mock only returns 1 item

    def test_generate_and_save(self, tmp_path):
        """Test generating and saving an image."""
        # Create the service with our mock directly
        service = OpenAIService(api_key="test_key")
        service.client = self.mock_client  # Replace the client directly

        with patch(
            "discovita.service.openai_service.core.image.utils.base64.b64decode"
        ) as mock_decode:
            mock_decode.return_value = b"test image data"

            result = service.generate_image(
                prompt="A beautiful landscape", save_to_path=str(tmp_path)
            )

            # Verify the mock was called
            self.mock_client.images.generate.assert_called_once()

            # Verify the result
            assert len(result) == 1
            assert "local_path" in result[0]
            assert os.path.exists(result[0]["local_path"])


# Optional: Live API Test (only runs with API_KEY in env)
@pytest.mark.requires_api
@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="Requires API key")
class TestLiveImageGeneration:
    """Live API tests for image generation (only runs with --run-api-tests and API key)."""

    def setup_class(self):
        """Set up the test class."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.service = OpenAIService(api_key=self.api_key)
        self.tmp_dir = tempfile.mkdtemp()

    def teardown_class(self):
        """Clean up after the test class."""
        if hasattr(self, "tmp_dir") and os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_live_generate_simple(self):
        """Test generating a simple image with default settings."""
        result = self.service.generate_image(
            prompt="A simple test image with abstract shapes", save_to_path=self.tmp_dir
        )

        assert len(result) > 0
        assert "local_path" in result[0]
        assert os.path.exists(result[0]["local_path"])

        # Check if the image file has content
        img_path = result[0]["local_path"]
        assert os.path.getsize(img_path) > 0
