"""API communication functions for identity testing."""

import sys
from typing import Dict, Any, List
import requests

def send_message(
    base_url: str,
    session_id: str,
    message: str,
    conversation_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Send a message to the coach API and return the response.
    
    Args:
        base_url: Base URL for the coach API
        session_id: Session identifier
        message: The user message to send
        conversation_history: Previous conversation history
        
    Returns:
        The complete response from the coach API
    """
    url = f"{base_url}/api/v1/coach/user_input"
    
    # Create a copy of the conversation history with the new message
    updated_history = conversation_history.copy()
    updated_history.append({"role": "user", "content": message})
    
    payload = {
        "user_id": session_id,
        "message": message,
        "context": conversation_history  # Send previous history without current message
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the coach API: {e}")
        sys.exit(1)

def check_server_health(base_url: str) -> bool:
    """
    Check if the server is running.
    
    Args:
        base_url: Base URL for the API
        
    Returns:
        True if the server is running, False otherwise
    """
    try:
        requests.get(f"{base_url}/api/v1/health")
        return True
    except requests.exceptions.RequestException:
        try:
            # Try alternative health endpoint
            requests.get(f"{base_url}/api/health")
            return True
        except requests.exceptions.RequestException:
            return False
