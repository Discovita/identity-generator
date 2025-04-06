"""Tests for LLMResponseModel in OpenAI service."""

import json
from typing import List, Optional

import pytest
from discovita.service.openai.models.llm_response import LLMResponseModel
from pydantic import BaseModel, Field


class TestLLMResponseModel:
    """Test cases for the LLMResponseModel base class."""

    def test_schema_generation(self):
        """Test OpenAI schema generation from Pydantic model."""

        # Create a test model that inherits from LLMResponseModel
        class TestResponse(LLMResponseModel):
            """Test response model for testing schema generation."""

            name: str
            age: int
            items: List[str]
            description: Optional[str] = None

        # Generate schema
        schema = TestResponse.get_openai_schema()

        # Validate schema structure
        assert isinstance(schema, dict)
        assert "properties" in schema
        assert "required" in schema

        # Validate properties
        assert "name" in schema["properties"]
        assert "age" in schema["properties"]
        assert "items" in schema["properties"]
        assert "description" in schema["properties"]

        # Validate required fields include all properties
        assert set(schema["required"]) == {"name", "age", "items", "description"}

        # Validate types
        assert schema["properties"]["name"]["type"] == "string"
        assert schema["properties"]["age"]["type"] == "integer"
        assert schema["properties"]["items"]["type"] == "array"

    def test_prompt_instruction_generation(self):
        """Test prompt instruction generation."""

        # Create a test model
        class TestResponse(LLMResponseModel):
            """Test response model for generating prompt instructions."""

            result: str = Field(..., description="The result of the operation")
            confidence: float = Field(
                ..., description="Confidence score between 0 and 1"
            )

        # Generate prompt instruction
        instruction = TestResponse.get_prompt_instruction()

        # Validate instruction format
        assert isinstance(instruction, str)
        assert instruction.startswith(
            "Please provide your response in the following JSON format:"
        )

        # The instruction should contain a JSON schema
        assert "result" in instruction
        assert "confidence" in instruction

        # Parse the JSON schema from the instruction
        # Extract the JSON part from the instruction
        json_start = instruction.find("{")
        json_end = instruction.rfind("}") + 1
        schema_str = instruction[json_start:json_end]

        # Parse the schema
        schema = json.loads(schema_str)

        # Validate schema structure
        assert "properties" in schema
        assert "required" in schema
        assert set(schema["required"]) == {"result", "confidence"}

        # Validate property descriptions
        assert (
            schema["properties"]["result"]["description"]
            == "The result of the operation"
        )
        assert (
            schema["properties"]["confidence"]["description"]
            == "Confidence score between 0 and 1"
        )

    def test_model_inheritance(self):
        """Test that model inheritance works correctly with LLMResponseModel."""

        # Create a parent model
        class BaseResponse(LLMResponseModel):
            """Base response with common fields."""

            success: bool
            message: str

        # Create a child model
        class DetailedResponse(BaseResponse):
            """Detailed response with additional fields."""

            data: List[str]
            count: int

        # Validate inheritance
        schema = DetailedResponse.get_openai_schema()

        # Should include fields from both parent and child
        assert "success" in schema["properties"]
        assert "message" in schema["properties"]
        assert "data" in schema["properties"]
        assert "count" in schema["properties"]

        # All fields should be required
        assert set(schema["required"]) == {"success", "message", "data", "count"}

        # Test instantiation
        response = DetailedResponse(
            success=True, message="OK", data=["item1", "item2"], count=2
        )
        assert response.success is True
        assert response.message == "OK"
        assert response.data == ["item1", "item2"]
        assert response.count == 2
