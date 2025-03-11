"""Test script to verify OpenAI client logging."""

import asyncio
import os
from pathlib import Path
from discovita.config import Settings
from discovita.service.openai.client.client import OpenAIClient
from discovita.service.coach.models import CoachStructuredResponse

async def test_openai_logging():
    """Test OpenAI client logging."""
    print("Starting OpenAI logging test...")
    
    # Get settings
    settings = Settings.from_env()
    
    # Create client with explicit test_mode=False
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        base_url="https://api.openai.com/v1",
        test_mode=False
    )
    
    # Print client mode
    print(f"Client mode: {client.mode}")
    
    # Check if logs directory exists
    project_root = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    log_dir = project_root / "logs"
    log_file = log_dir / "openai.log"
    
    print(f"Project root: {project_root}")
    print(f"Log directory: {log_dir}")
    print(f"Log directory exists: {log_dir.exists()}")
    print(f"Log file path: {log_file}")
    print(f"Log file exists: {log_file.exists()}")
    
    # Make a simple request
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, world!"}
    ]
    
    print("\nSending request to OpenAI...")
    response = await client.get_structured_completion(
        messages=messages,
        response_model=CoachStructuredResponse
    )
    
    print(f"\nReceived response: {response.message}")
    
    # Check if log file was created
    print(f"\nAfter request, log file exists: {log_file.exists()}")
    if log_file.exists():
        # Print the last few lines of the log file
        print("\nLast 10 lines of log file:")
        with open(log_file, "r") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    
    print("\nTest completed.")

if __name__ == "__main__":
    asyncio.run(test_openai_logging())
