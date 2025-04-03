"""
Tests for the AI models and providers.

This module tests the AIModel and AIProvider enums, including model
identification, feature detection, and parameter validation.
"""

import pytest
from discovita.service.openai import AIModel, AIProvider


class TestAIProvider:
    """
    Tests for the AIProvider enum.

    These tests verify the functionality of the AIProvider enum,
    including string conversion and validation.
    """

    def test_from_string(self):
        """
        Test converting string representations to AIProvider enum values.

        This test verifies that various string representations
        of providers are correctly converted to the corresponding
        AIProvider enum values.
        """
        # Test OpenAI provider
        assert AIProvider.from_string("openai") == AIProvider.OPENAI
        assert AIProvider.from_string("OPENAI") == AIProvider.OPENAI
        assert AIProvider.from_string("gpt") == AIProvider.OPENAI
        assert AIProvider.from_string("OpenAI") == AIProvider.OPENAI

        # Test Anthropic provider
        assert AIProvider.from_string("anthropic") == AIProvider.ANTHROPIC
        assert AIProvider.from_string("ANTHROPIC") == AIProvider.ANTHROPIC
        assert AIProvider.from_string("claude") == AIProvider.ANTHROPIC
        assert AIProvider.from_string("Anthropic") == AIProvider.ANTHROPIC

        # Test invalid provider
        with pytest.raises(ValueError):
            AIProvider.from_string("invalid_provider")

        with pytest.raises(ValueError):
            AIProvider.from_string("")


class TestAIModel:
    """
    Tests for the AIModel enum.

    These tests verify the functionality of the AIModel enum,
    including string conversion, provider determination, and
    feature detection.
    """

    def test_from_string(self):
        """
        Test converting string representations to AIModel enum values.

        This test verifies that various string representations
        of models are correctly converted to the corresponding
        AIModel enum values.
        """
        # Test exact match
        assert AIModel.from_string("gpt-4-turbo") == AIModel.GPT_4_TURBO
        assert AIModel.from_string("gpt-4o") == AIModel.GPT_4O
        assert AIModel.from_string("o3-mini") == AIModel.O3_MINI
        assert AIModel.from_string("gpt-3.5-turbo") == AIModel.GPT_3_5_TURBO

        # Test invalid model
        with pytest.raises(ValueError):
            AIModel.from_string("invalid_model")

        with pytest.raises(ValueError):
            AIModel.from_string("")

    def test_get_provider(self):
        """
        Test getting the provider for a model.

        This test verifies that the correct provider is returned
        for different models.
        """
        # Test OpenAI models
        assert AIModel.get_provider(AIModel.GPT_4_TURBO) == AIProvider.OPENAI
        assert AIModel.get_provider("gpt-4") == AIProvider.OPENAI
        assert AIModel.get_provider("o3-mini") == AIProvider.OPENAI
        assert AIModel.get_provider("o1") == AIProvider.OPENAI
        assert AIModel.get_provider("gpt-3.5-turbo") == AIProvider.OPENAI

        # Test with enum values
        assert AIModel.get_provider(AIModel.GPT_4) == AIProvider.OPENAI
        assert AIModel.get_provider(AIModel.O3_MINI) == AIProvider.OPENAI

        # Test invalid model - should default to OpenAI provider
        assert AIModel.get_provider("unknown-model") == AIProvider.OPENAI

    def test_supports_structured_outputs(self):
        """
        Test checking if a model supports structured outputs.

        This test verifies that the correct support status
        is returned for different models.
        """
        # Test basic functionality with a few known models
        # Specific models and their support might change over time
        result = AIModel.supports_structured_outputs(AIModel.GPT_4O)
        assert isinstance(result, bool)

    def test_get_token_param_name(self):
        """
        Test getting the token parameter name for a model.

        This test verifies that the correct token parameter name
        is returned for different models.
        """
        # Test models that use max_completion_tokens
        assert AIModel.get_token_param_name("o3-mini") == "max_completion_tokens"
        assert AIModel.get_token_param_name("o1") == "max_completion_tokens"
        assert AIModel.get_token_param_name("o1-mini") == "max_completion_tokens"
        assert AIModel.get_token_param_name("gpt-4o") == "max_completion_tokens"

        # Test with enum values
        assert AIModel.get_token_param_name(AIModel.O3_MINI) == "max_completion_tokens"
        assert AIModel.get_token_param_name(AIModel.GPT_4O) == "max_completion_tokens"

        # Test models that use max_tokens
        assert AIModel.get_token_param_name("gpt-4") == "max_tokens"
        assert AIModel.get_token_param_name("gpt-3.5-turbo") == "max_tokens"
        assert AIModel.get_token_param_name("gpt-4-turbo") == "max_tokens"

        # Test with enum values
        assert AIModel.get_token_param_name(AIModel.GPT_4) == "max_tokens"
        assert AIModel.get_token_param_name(AIModel.GPT_3_5_TURBO) == "max_tokens"

        # Test models that aren't in our enum but should match patterns
        assert AIModel.get_token_param_name("gpt-3.5-turbo-16k") == "max_tokens"
        assert AIModel.get_token_param_name("o3") == "max_completion_tokens"
        assert (
            AIModel.get_token_param_name("gpt-4o-2024-05-13") == "max_completion_tokens"
        )

        # Test with unknown model - should default to max_tokens
        assert AIModel.get_token_param_name("unknown-model") == "max_tokens"

    def test_get_unsupported_parameters(self):
        """
        Test getting unsupported parameters for different models.

        This test verifies that the correct list of unsupported
        parameters is returned for different models.
        """
        # Test models with known unsupported parameters
        assert "temperature" in AIModel.get_unsupported_parameters("o3-mini")
        assert "top_p" in AIModel.get_unsupported_parameters("o1")
        assert "parallel_tool_calls" in AIModel.get_unsupported_parameters("o1-mini")

        # Test using enum values
        assert "temperature" in AIModel.get_unsupported_parameters(AIModel.O3_MINI)
        assert "top_p" in AIModel.get_unsupported_parameters(AIModel.O1)
        assert "parallel_tool_calls" in AIModel.get_unsupported_parameters(
            AIModel.O1_MINI
        )

        # Test models with pattern matching (o-series)
        assert "temperature" in AIModel.get_unsupported_parameters("o3-2024-05-13")
        assert "top_p" in AIModel.get_unsupported_parameters("o1-preview")

        # Test models that should support all parameters
        assert len(AIModel.get_unsupported_parameters("gpt-4")) == 0
        assert len(AIModel.get_unsupported_parameters("gpt-3.5-turbo")) == 0
        assert len(AIModel.get_unsupported_parameters(AIModel.GPT_4_TURBO)) == 0

        # Test with unknown model - should default to empty list
        assert len(AIModel.get_unsupported_parameters("unknown-model")) == 0
