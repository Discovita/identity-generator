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
) -> StructuredResponseResult[T]:
    """Get a structured response from the OpenAI Responses API."""
    # Create schema and tools configuration
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

    # Create result and parse output
    result = StructuredResponseResult(response=response)
    text_output = next(
        (item.text for item in response.output 
         if isinstance(item, ResponseOutputText)),
        None
    )

    if text_output:
        try:
            data = json.loads(text_output)
            result.parsed = response_model.model_validate(data)
            result.is_valid = True
        except Exception as e:
            result.error = str(e)

    return result
