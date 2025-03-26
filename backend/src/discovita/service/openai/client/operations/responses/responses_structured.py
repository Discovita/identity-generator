"""OpenAI Responses API structured outputs operations."""

import json
from typing import TypeVar, Type, Optional, Generic
from openai import AsyncOpenAI
from openai.types.responses import Response
from openai.types.responses.response_output_text import ResponseOutputText
from pydantic import BaseModel
from discovita.service.openai.models import (
    StructuredOutputSchema,
    LLMResponseModel,
    ToolChoice,
)
from .responses_basic import create_response
from .responses import ResponseInput, ResponseTools

T = TypeVar("T", bound=LLMResponseModel)

class StructuredResponseResult(BaseModel, Generic[T]):
    """Result of a structured response operation."""
    response: Response
    parsed: Optional[T] = None
    is_valid: bool = False
    error: Optional[str] = None

async def get_response(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    response_model: Type[T],
    model: str = "gpt-4o",
    schema_name: Optional[str] = None,
    store: bool = True,
    previous_response_id: Optional[str] = None,
    tools: Optional[ResponseTools] = None,
) -> StructuredResponseResult[T]:
    """Get a structured response from the OpenAI Responses API."""
    # Create schema and tools configuration
    if tools is None:
        schema = StructuredOutputSchema.from_llm_response_model(
            response_model, 
            name=schema_name
        )
        tools = ResponseTools(
            tools=[schema.model_dump()],
            tool_choice=ToolChoice.specific(schema.name)
        )

    # Get response with schema as tool
    response = await create_response(
        client=client,
        input_data=input_data,
        model=model,
        tools=tools,
        store=store,
        previous_response_id=previous_response_id,
    )

    # Create result with response
    result = StructuredResponseResult(response=response)
    
    # Assert response has expected structure
    assert response.output, "Response must have output"
    assert len(response.output) > 0, "Response output cannot be empty"
    assert hasattr(response.output[0], 'content'), "Response output must have content"
    assert len(response.output[0].content) > 0, "Response content cannot be empty"
    assert hasattr(response.output[0].content[0], 'text'), "Response content must have text"
    
    # Extract message
    message = response.output[0].content[0].text
    
    # Create response data
    data = {
        "message": message,
        "actions": []  # We'll add function call handling later
    }
    
    # Parse into model
    result.parsed = response_model.model_validate(data)
    result.is_valid = True

    return result
