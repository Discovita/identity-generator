"""
Tests for utility functions in the OpenAI service.

This module tests the utility functions used by the OpenAI service,
including image encoding, model utilities, and parameter handling.
"""

import base64
import os
import tempfile
from unittest.mock import MagicMock, mock_open, patch

import pytest
from discovita.service.openai_service import AIModel
from discovita.service.openai_service.utils.image import encode_image
from discovita.service.openai_service.utils.model_utils import (
    check_dependency_versions,
    filter_unsupported_parameters,
)


class TestImageUtils:
    """
    Tests for image utility functions.

    These tests verify that image utility functions correctly
    handle image encoding and validation.
    """

    def test_encode_image_jpg(self, temp_image_file):
        """
        Test encoding a JPEG image to base64.

        This test verifies that a JPEG image is correctly
        encoded to base64 and formatted with the appropriate
        MIME type.
        """
        # Mock base64 encoding
        with patch("base64.b64encode", return_value=b"encoded_data"):
            result = encode_image(temp_image_file)

            assert result == "data:image/jpeg;base64,encoded_data"

    def test_encode_image_png(self):
        """
        Test encoding a PNG image to base64.

        This test verifies that a PNG image is also correctly
        encoded to base64 with a JPEG MIME type (since the
        implementation always uses JPEG).
        """
        # Create a temporary PNG file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(b"fake png data")
            tmp_path = tmp.name

        try:
            # Mock base64 encoding
            with patch("base64.b64encode", return_value=b"encoded_data"):
                result = encode_image(tmp_path)

                # Note: The implementation always uses jpeg MIME type
                assert result == "data:image/jpeg;base64,encoded_data"
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_file_not_found(self):
        """
        Test encoding a non-existent image file.

        This test verifies that attempting to encode a
        non-existent file raises an appropriate error.
        """
        with pytest.raises(FileNotFoundError):
            encode_image("nonexistent_file.jpg")

    def test_encoding_error(self):
        """
        Test error handling during encoding.

        This test verifies that errors during encoding are
        properly caught and re-raised.
        """
        # Create a test file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(b"fake image data")
            tmp_path = tmp.name

        try:
            # Mock open to raise an exception during encoding
            mock_file = mock_open()
            mock_file.side_effect = Exception("Test encoding error")

            with patch("builtins.open", mock_file):
                with pytest.raises(Exception) as excinfo:
                    encode_image(tmp_path)

                assert "Test encoding error" in str(excinfo.value)
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestModelUtils:
    """
    Tests for model utility functions.

    These tests verify that model utility functions correctly
    handle version checking and parameter validation.
    """

    def test_check_dependency_versions(self):
        """
        Test checking dependency versions.

        This test verifies that the version check function
        correctly identifies compatible and incompatible versions.
        """
        # Import the actual OPENAI_VERSION constant
        from discovita.service.openai_service.utils.model_utils import OPENAI_VERSION

        # Test with matching version
        with (
            patch(
                "discovita.service.openai_service.utils.model_utils.version"
            ) as mock_version,
            patch("discovita.service.openai_service.utils.model_utils.log") as mock_log,
        ):
            mock_version.side_effect = lambda package: (
                OPENAI_VERSION if package == "openai" else "1.0.0"
            )

            check_dependency_versions()

            # No warning should be logged
            mock_log.warning.assert_not_called()

        # Test with non-matching version
        with (
            patch(
                "discovita.service.openai_service.utils.model_utils.version"
            ) as mock_version,
            patch("discovita.service.openai_service.utils.model_utils.log") as mock_log,
            patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "False"}),
        ):
            mock_version.side_effect = lambda package: (
                "0.0.1" if package == "openai" else "1.0.0"
            )

            check_dependency_versions()

            # Warning should be logged
            mock_log.warning.assert_called_once()

        # Test with muted warnings
        with (
            patch(
                "discovita.service.openai_service.utils.model_utils.version"
            ) as mock_version,
            patch("discovita.service.openai_service.utils.model_utils.log") as mock_log,
            patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "True"}),
        ):
            mock_version.side_effect = lambda package: (
                "0.0.1" if package == "openai" else "1.0.0"
            )

            check_dependency_versions()

            # No warning should be logged due to muting
            mock_log.warning.assert_not_called()

    def test_filter_unsupported_parameters(self):
        """
        Test filtering unsupported parameters.

        This test verifies that parameters not supported by a
        specific model are correctly filtered out.
        """
        # Test with o3-mini model (doesn't support temperature)
        params = {
            "model": "o3-mini",
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 0.9,
        }

        filtered_params = filter_unsupported_parameters(params, "o3-mini")

        assert "temperature" not in filtered_params
        assert "top_p" not in filtered_params
        assert "max_tokens" in filtered_params

        # Test with standard model (should support all parameters)
        params = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 100, "top_p": 0.9}

        filtered_params = filter_unsupported_parameters(params, "gpt-4")

        assert "temperature" in filtered_params
        assert "top_p" in filtered_params
        assert "max_tokens" in filtered_params
