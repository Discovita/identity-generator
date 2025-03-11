"""Test the LLM response model with schema generation."""

import asyncio
from typing import List, Optional
from openai import AsyncOpenAI
from pydantic import Field

from discovita.config import Settings
from discovita.service.openai.models.llm_response import LLMResponseModel
from discovita.service.coach.models import Identity

class TestResponse(LLMResponseModel):
    """A response from a coaching session that provides guidance and identity suggestions."""
    
    message: str = Field(
        ..., 
        description="The coach's response message to the user"
    )
    suggested_identities: Optional[List[Identity]] = Field(
        None,
        description="List of potential identities extracted from the conversation"
    )

async def test_structured_output():
    """Test OpenAI structured output with schema generation."""
    settings = Settings.from_env()
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    # Test scenario
    user_message = """I want to be more creative in my work. I'm a software engineer 
    but I feel stuck in a rut, just implementing the same patterns over and over. 
    I want to bring more innovation and artistic thinking to my code."""
    
    # Get schema instruction
    schema_instruction = TestResponse.get_prompt_instruction()
    print("\nGenerated Schema Instruction:")
    print(schema_instruction)
    
    # Create prompt with schema instruction
    prompt = f"{user_message}\n\n{schema_instruction}"
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    print("\nRaw OpenAI Response:")
    print(response.choices[0].message.content)
    
    print("\nParsed Response:")
    parsed_response = TestResponse.model_validate_json(
        response.choices[0].message.content
    )
    print(f"\nCoach Message: {parsed_response.message}")
    
    if parsed_response.suggested_identities:
        print("\nExtracted Identities:")
        for identity in parsed_response.suggested_identities:
            print(f"\nCategory: {identity.category}")
            print(f"Name: {identity.name}")
            print(f"Affirmation: {identity.affirmation}")
            if identity.visualization:
                print("Visualization:", identity.visualization)

if __name__ == "__main__":
    asyncio.run(test_structured_output())
