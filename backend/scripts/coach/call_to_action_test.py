"""Test script to check coach API responses for call to action."""

import asyncio
import json
import requests
from typing import Dict, Any, List, Optional

from discovita.service.coach.models import (
    CoachRequest,
    CoachResponse,
    ChatMessage,
    UserProfile
)

def call_coach_api(message: str) -> Dict[str, Any]:
    """Call the coach API with a message and return the response."""
    # Assuming the API is running on localhost:8000
    url = "http://localhost:8000/api/v1/coach/user_input"
    
    # Create a request object
    request = CoachRequest(
        user_id="test_user_123",
        message=message,
        context=[],  # Empty context for a new conversation
        profile=None  # No profile for this test
    )
    
    # Convert to dict for the request
    request_data = request.model_dump()
    
    # Make the request
    response = requests.post(url, json=request_data)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {}
    
    return response.json()

def analyze_response(response: Dict[str, Any]) -> None:
    """Analyze the coach response for quality and call to action."""
    # Parse the response
    coach_response = CoachResponse.model_validate(response)
    
    # Print the message
    print("\n=== COACH RESPONSE ===")
    print(coach_response.message)
    print("\n=== ANALYSIS ===")
    
    # Check message length
    word_count = len(coach_response.message.split())
    print(f"Word count: {word_count}")
    if word_count < 50:
        print("WARNING: Response is very short!")
    
    # Check for call to action or questions
    has_question = "?" in coach_response.message
    print(f"Contains questions: {has_question}")
    
    # Check for proposed identity
    if coach_response.proposed_identity:
        print("\n=== PROPOSED IDENTITY ===")
        print(f"Category: {coach_response.proposed_identity.category}")
        print(f"Name: {coach_response.proposed_identity.name}")
        print(f"Affirmation: {coach_response.proposed_identity.affirmation}")
    else:
        print("\nNo identity proposed")
    
    # Check for confirmed identity
    if coach_response.confirmed_identity:
        print("\n=== CONFIRMED IDENTITY ===")
        print(f"Category: {coach_response.confirmed_identity.category}")
        print(f"Name: {coach_response.confirmed_identity.name}")
        print(f"Affirmation: {coach_response.confirmed_identity.affirmation}")

def main() -> None:
    """Main function to test the coach API."""
    # Test message
    message = "I want to explore my identity as a visionary engineer."
    
    print(f"Sending message: '{message}'")
    response = call_coach_api(message)
    
    if response:
        analyze_response(response)
    else:
        print("Failed to get a valid response from the coach API.")
        print("Make sure the backend server is running.")

if __name__ == "__main__":
    main()
