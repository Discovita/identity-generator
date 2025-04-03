"""
Tests for OpenAIService initialization and base functionality.

This module tests the initialization of the OpenAIService class,
including API key handling, organization configuration, and
dependency version checking.
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from discovita.service.openai_service import OpenAIService


class TestServiceInitialization:
    """
    Tests for the initialization of the OpenAIService class.

    These tests verify that the service properly initializes with
    the correct API key and organization, and that it properly
    checks dependencies.
    """

    def test_init_with_api_key(self):
        """
        Test that OpenAIService initializes correctly with an API key.

        This test verifies that the OpenAI client is initialized with
        the provided API key.
        """
        with patch("discovita.service.openai_service.core.base.OpenAI") as mock_openai:
            service = OpenAIService(api_key="test_api_key")
            mock_openai.assert_called_once_with(
                api_key="test_api_key", organization=None
            )

    def test_init_with_api_key_and_org(self):
        """
        Test that OpenAIService initializes correctly with an API key and organization.

        This test verifies that the OpenAI client is initialized with
        both the provided API key and organization.
        """
        with patch("discovita.service.openai_service.core.base.OpenAI") as mock_openai:
            service = OpenAIService(api_key="test_api_key", organization="test_org")
            mock_openai.assert_called_once_with(
                api_key="test_api_key", organization="test_org"
            )

    def test_version_check(self):
        """
        Test that the dependency version check works correctly.

        This test verifies that a warning is logged when using an unsupported
        version of the OpenAI package, and that the warning can be muted.
        """
        # Import the actual OPENAI_VERSION constant
        from discovita.service.openai_service.utils.model_utils import OPENAI_VERSION

        # Create a custom version function for mocking
        def mock_version_func(package_name):
            if package_name == "openai":
                return "0.0.1"  # Return a version different from OPENAI_VERSION
            return "1.0.0"  # Default for other packages

        with (
            patch("discovita.service.openai_service.core.base.OpenAI"),
            patch(
                "discovita.service.openai_service.utils.model_utils.version",
                side_effect=mock_version_func,
            ),
            patch("discovita.service.openai_service.utils.model_utils.log") as mock_log,
            patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "False"}),
        ):

            # Initialize the service, which should trigger the version check
            service = OpenAIService(api_key="test_api_key")

            # Verify that a warning was logged
            mock_log.warning.assert_called_once()

            # Test with muted warnings
            mock_log.reset_mock()
            with patch.dict(os.environ, {"MUTE_OPENAI_HELPER_WARNING": "True"}):
                service = OpenAIService(api_key="test_api_key")
                mock_log.warning.assert_not_called()

    def test_dependency_check_with_matching_version(self):
        """
        Test that no warning is logged when the OpenAI package version matches the expected version.

        This test verifies that no warning is logged when using a supported
        version of the OpenAI package.
        """
        # Import the actual OPENAI_VERSION constant
        from discovita.service.openai_service.utils.model_utils import OPENAI_VERSION

        # Create a custom version function that returns the expected version
        def mock_version_func(package_name):
            if package_name == "openai":
                return OPENAI_VERSION
            return "1.0.0"  # Default for other packages

        with (
            patch("discovita.service.openai_service.core.base.OpenAI"),
            patch(
                "discovita.service.openai_service.utils.model_utils.version",
                side_effect=mock_version_func,
            ),
            patch("discovita.service.openai_service.utils.model_utils.log") as mock_log,
        ):

            # Initialize the service, which should trigger the version check
            service = OpenAIService(api_key="test_api_key")

            # Verify that no warning was logged
            mock_log.warning.assert_not_called()
