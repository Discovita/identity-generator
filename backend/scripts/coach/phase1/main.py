#!/usr/bin/env python
"""Terminal-based coach chatbot with function calling capabilities.

This implementation extends the basic coach chatbot with LLM function calling
to allow the model to update the conversation state as it progresses.

The function calling capability allows the LLM to:
1. Add new identities during brainstorming and refinement phases
2. Mark introduction as completed to trigger state transition
3. Set focus identity during visualization phase
4. Mark identities as visualized
5. Get current state information to guide the conversation
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
current_file = Path(__file__)
backend_dir = current_file.parents[2]  # Go up to backend directory
sys.path.insert(0, str(backend_dir))

from scripts.coach.phase1.extended_context_builder import ExtendedContextBuilder
from scripts.coach.phase1.terminal_coach import TerminalCoach

# Import the necessary modules
from src.discovita.service.coach.service import CoachService
from src.discovita.service.openai.client.client import OpenAIClient
from src.discovita.utils.logger import configure_logging

log = configure_logging(
    logger_name="coach_phase1",
    keep_logs=True,
    log_dir="logs",
    log_filename="coach_phase1.log",
)

# Load environment variables from .env file
current_file = Path(__file__)
project_root = current_file.parents[4]
env_path = project_root / ".env"

# Load environment variables
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    log.warning(f"[ENV] Warning: .env file not found at {env_path}")

# This is the API key from your .env file
API_KEY = os.getenv("OPENAI_API_KEY")


class ExtendedCoachService(CoachService):
    """Extended coach service that uses the extended context builder.

    This service adds:
    1. Function calling capability to update state as conversation progresses
    2. State-specific prompts via the extended context builder
    """

    def __init__(self, client: OpenAIClient):
        """Initialize the extended coach service."""
        super().__init__(client)
        # Replace the context builder with our extended version
        self.context_builder = ExtendedContextBuilder()


async def main():
    """Run the coach chatbot with function calling capability."""
    # Check for OpenAI API key
    if not API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in a .env file or in your environment.")
        return

    try:
        # Initialize OpenAI client with API key and function calling capability
        openai_client = OpenAIClient(
            api_key=API_KEY,
            # Configure the client to support function calling
            default_model="gpt-4o",  # Use a model that supports function calling
        )
        log.info("Initialized OpenAI client with function calling capability")

        # Initialize extended coach service
        coach_service = ExtendedCoachService(openai_client)
        log.info("Initialized extended coach service")

        # Initialize terminal coach with function calling
        terminal_coach = TerminalCoach(coach_service)
        log.info("Initialized terminal coach")

        # Run terminal interface
        print("\nStarting coach with function calling capability...\n")
        await terminal_coach.run_terminal_interface()
    except Exception as e:
        log.error(f"Error running coach: {e}")
        print(f"\nError: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...")
    except Exception as e:
        log.error(f"Unhandled exception: {e}")
        print(f"\nError: {e}")
