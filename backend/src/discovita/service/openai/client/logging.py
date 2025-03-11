"""Logging configuration for OpenAI client."""

import logging
import json
from pathlib import Path
from typing import Any, Dict
import sys

# Get project root directory (backend folder)
project_root = Path(__file__).resolve().parents[5]  # Go up 5 levels to reach the backend folder
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

# Print debug info
print(f"Project root: {project_root}")
print(f"Log directory: {log_dir}")
print(f"Log directory exists: {log_dir.exists()}")

# Configure logger
logger = logging.getLogger("openai_client")
logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logging

# Create file handler
log_file = log_dir / "openai.log"
print(f"Log file path: {log_file}")
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Add console handler for debugging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Test logger
logger.debug("Logger initialized")

def log_request(operation: str, **kwargs: Any) -> None:
    """Log OpenAI API request details."""
    try:
        # Create a safe copy of kwargs without sensitive data
        safe_kwargs = {k: v for k, v in kwargs.items() if k != "api_key"}
        
        # Log the operation
        logger.info(f"=== OpenAI Request: {operation} ===")
        
        # Log messages in a more readable format if present
        if "messages" in safe_kwargs:
            logger.info("Messages:")
            for msg in safe_kwargs["messages"]:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                logger.info(f"  {role}: {content}")
        
        # Log other parameters
        for key, value in safe_kwargs.items():
            if key != "messages":
                logger.info(f"{key}: {value}")
        
        logger.info("=== End Request ===")
    except Exception as e:
        logger.error(f"Error logging request: {str(e)}")

def log_response(operation: str, response: Any) -> None:
    """Log OpenAI API response details."""
    try:
        logger.info(f"=== OpenAI Response: {operation} ===")
        
        # For OpenAI completion responses, log the content directly
        if hasattr(response, "choices") and len(response.choices) > 0:
            if hasattr(response.choices[0], "message") and hasattr(response.choices[0].message, "content"):
                logger.info(f"Content: {response.choices[0].message.content}")
            
            # Log model and usage info if available
            if hasattr(response, "model"):
                logger.info(f"Model: {response.model}")
            if hasattr(response, "usage"):
                logger.info(f"Usage: {response.usage}")
        else:
            # Fallback for other response types - just dump as string
            logger.info(f"Response: {str(response)}")
        
        logger.info("=== End Response ===")
    except Exception as e:
        logger.error(f"Error logging response: {str(e)}")
