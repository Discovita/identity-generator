"""Test identity extraction in coach API."""

import asyncio
from typing import List
from discovita.config import Settings
from discovita.service.coach.models import ChatMessage, CoachRequest, Identity
from discovita.service.coach.service import CoachService
from discovita.service.openai.client.client import OpenAIClient

async def test_identity_extraction():
    """Test basic identity extraction scenario."""
    settings = Settings.from_env()
    client = OpenAIClient(api_key=settings.openai_api_key)
    service = CoachService(client)
    
    # Initial conversation context
    context: List[ChatMessage] = []
    
    # Test scenario: User expresses desire to be more creative
    request = CoachRequest(
        user_id="test_user",
        message="I want to be more creative in my work. I'm a software engineer but I feel stuck in a rut, just implementing the same patterns over and over. I want to bring more innovation and artistic thinking to my code.",
        context=context
    )
    
    response = await service.get_response(request)
    print("\nCoach Response:")
    print(response.message)
    
    if response.suggested_identities:
        print("\nExtracted Identities:")
        for identity in response.suggested_identities:
            print(f"\nCategory: {identity.category}")
            print(f"Name: {identity.name}")
            print(f"Affirmation: {identity.affirmation}")
            if identity.visualization:
                print("Visualization:", identity.visualization)
    else:
        print("\nNo identities were extracted")

if __name__ == "__main__":
    asyncio.run(test_identity_extraction())
