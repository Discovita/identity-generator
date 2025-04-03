"""Tests for tool_choice models in OpenAI service."""

from typing import Any, Dict

import pytest
from discovita.service.openai.models.tool_choice import (
    SpecificToolChoice,
    ToolChoice,
    ToolChoiceMode,
)


class TestToolChoice:
    """Test cases for tool choice models used with OpenAI API."""

    def test_tool_choice_mode_enum(self):
        """Test ToolChoiceMode enum values."""
        assert ToolChoiceMode.NONE == "none"
        assert ToolChoiceMode.AUTO == "auto"

        # Test string conversion
        assert ToolChoiceMode.NONE.value == "none"
        assert ToolChoiceMode.AUTO.value == "auto"

    def test_specific_tool_choice_creation(self):
        """Test SpecificToolChoice model initialization."""
        # Test with basic function
        tool = SpecificToolChoice(function={"name": "get_weather"})
        assert tool.type == "function"  # Default value
        assert tool.function["name"] == "get_weather"

        # Test with function arguments
        tool = SpecificToolChoice(
            function={
                "name": "get_weather",
                "arguments": '{"location": "San Francisco"}',
            }
        )
        assert tool.function["name"] == "get_weather"
        assert "arguments" in tool.function
        assert "San Francisco" in tool.function["arguments"]

    def test_tool_choice_default_creation(self):
        """Test ToolChoice model initialization with default values."""
        tool_choice = ToolChoice()
        assert tool_choice.mode == ToolChoiceMode.AUTO
        assert tool_choice.specific_tool is None

    def test_tool_choice_custom_creation(self):
        """Test ToolChoice model initialization with custom values."""
        specific_tool = SpecificToolChoice(function={"name": "get_weather"})
        tool_choice = ToolChoice(mode=ToolChoiceMode.NONE, specific_tool=specific_tool)

        assert tool_choice.mode == ToolChoiceMode.NONE
        assert tool_choice.specific_tool is not None
        assert tool_choice.specific_tool.function["name"] == "get_weather"

    def test_tool_choice_none_factory(self):
        """Test ToolChoice.none() factory method."""
        tool_choice = ToolChoice.none()

        assert tool_choice.mode == ToolChoiceMode.NONE
        assert tool_choice.specific_tool is None

    def test_tool_choice_auto_factory(self):
        """Test ToolChoice.auto() factory method."""
        tool_choice = ToolChoice.auto()

        assert tool_choice.mode == ToolChoiceMode.AUTO
        assert tool_choice.specific_tool is None

    def test_tool_choice_specific_factory(self):
        """Test ToolChoice.specific() factory method."""
        # Test with just a function name
        tool_choice = ToolChoice.specific(function_name="get_weather")

        assert tool_choice.mode == ToolChoiceMode.AUTO  # Should be AUTO when specific
        assert tool_choice.specific_tool is not None
        assert tool_choice.specific_tool.type == "function"
        assert tool_choice.specific_tool.function["name"] == "get_weather"

        # Test with function arguments
        tool_choice = ToolChoice.specific(
            function_name="search_database",
            arguments='{"query": "Claude AI", "limit": 10}',
        )

        assert tool_choice.specific_tool is not None
        assert tool_choice.specific_tool.function["name"] == "search_database"
        assert "arguments" in tool_choice.specific_tool.function
        assert "Claude AI" in tool_choice.specific_tool.function["arguments"]

    def test_tool_choice_json_serialization(self):
        """Test that ToolChoice can be serialized to JSON for API requests."""
        # Create a tool choice with a specific tool
        tool_choice = ToolChoice.specific(function_name="get_weather")

        # Convert to dict (simulating JSON serialization)
        tool_dict = tool_choice.model_dump()

        # Verify the structure
        assert isinstance(tool_dict, dict)
        assert "mode" in tool_dict
        assert "specific_tool" in tool_dict
        assert tool_dict["mode"] == "auto"
        assert tool_dict["specific_tool"]["type"] == "function"
        assert tool_dict["specific_tool"]["function"]["name"] == "get_weather"
