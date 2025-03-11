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
    # Handle potential None value
    content = response.choices[0].message.content
    if content is None:
        print("Error: Received None content from OpenAI")
        return
        
    parsed_response = CoachResponse.model_validate_json(content)
    print(f"\nCoach Message: {parsed_response.message}")
    
    # Check for proposed or confirmed identities
    identities = []
    if parsed_response.proposed_identity:
        identities.append(parsed_response.proposed_identity)
        print("\nProposed Identity:")
        print(f"Category: {parsed_response.proposed_identity.category}")
        print(f"Name: {parsed_response.proposed_identity.name}")
        print(f"Affirmation: {parsed_response.proposed_identity.affirmation}")
        if parsed_response.proposed_identity.visualization:
            print("Visualization:", parsed_response.proposed_identity.visualization)
    
    if parsed_response.confirmed_identity:
        identities.append(parsed_response.confirmed_identity)
        print("\nConfirmed Identity:")
        print(f"Category: {parsed_response.confirmed_identity.category}")
        print(f"Name: {parsed_response.confirmed_identity.name}")
        print(f"Affirmation: {parsed_response.confirmed_identity.affirmation}")
        if parsed_response.confirmed_identity.visualization:
            print("Visualization:", parsed_response.confirmed_identity.visualization)
    
    if not identities:
        print("\nNo identities were extracted")

if __name__ == "__main__":
    asyncio.run(test_structured_output())
