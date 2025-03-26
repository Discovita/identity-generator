"""OpenAI structured output operations."""

from typing import TypeVar, Type, Optional, Generic
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel
from discovita.service.openai.models import LLMResponseModel
from .responses_basic import create_response
from .responses import ResponseInput

T = TypeVar("T", bound=LLMResponseModel)

class StructuredResponseResult(BaseModel, Generic[T]):
    """Result of a structured response operation."""
    response: ChatCompletion
    parsed: Optional[T] = None
    is_valid: bool = False
    error: Optional[str] = None

async def get_response(
    client: AsyncOpenAI,
    input_data: ResponseInput,
    response_model: Type[T],
    model: str = "gpt-4o",
    store: bool = True,
    previous_response_id: Optional[str] = None,
) -> StructuredResponseResult[T]:
    """Get a structured response from the OpenAI Chat API."""
    # Get response with JSON format
    response = await create_response(
        client=client,
        input_data=input_data,
        model=model,
        response_format={"type": "json_object"},
        store=store,
        previous_response_id=previous_response_id,
    )

    # Create result with response
    result = StructuredResponseResult(response=response)
    
    # Extract and validate response
    assert response.choices and response.choices[0].message, "Response must have a message"
    assert response.choices[0].message.content, "Message must have content"
    
    # Parse structured JSON response
    result.parsed = response_model.model_validate_json(response.choices[0].message.content)
    result.is_valid = True

    return result
