"""Test OpenAI structured output functionality directly."""

import asyncio
from typing import List, Optional
from openai import AsyncOpenAI
from discovita.config import Settings
from discovita.service.coach.models import CoachResponse, Identity

async def test_structured_output():
    """Test OpenAI structured output without abstractions."""
    settings = Settings.from_env()
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    # Test scenario: User expresses desire to be more creative
    user_message = """I want to be more creative in my work. I'm a software engineer 
    but I feel stuck in a rut, just implementing the same patterns over and over. 
    I want to bring more innovation and artistic thinking to my code."""
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    
    print("\nRaw OpenAI Response:")
    print(response.choices[0].message.content)
    
    print("\nParsed Response:")
    parsed_response = CoachResponse.model_validate_json(
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
