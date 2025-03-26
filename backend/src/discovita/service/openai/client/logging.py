"""Logging configuration for OpenAI client."""

import logging
from typing import Any

from discovita.utils.logger import configure_logging

# Configure the OpenAI client logger using the new logger implementation
# Use INFO as default level so request/response details are only shown when debug is enabled
logger = configure_logging(
    logger_name="openai_client",
    log_level=logging.INFO,  # Default to INFO level
    keep_logs=False,
    log_dir="logs",
    log_filename="openai.log",
)

# Test logger - only appears in debug mode
logger.debug("Logger initialized")


def log_request(operation: str, **kwargs: Any) -> None:
    """Log OpenAI API request details.

    All logs are at DEBUG level so they only appear when debug logging is enabled.
    """
    try:
        # Create a safe copy of kwargs without sensitive data
        safe_kwargs = {k: v for k, v in kwargs.items() if k != "api_key"}

        # Log the operation (debug level)
        logger.debug(f"=== OpenAI Request: {operation} ===")

        # Log messages in a more readable format if present
        if "messages" in safe_kwargs:
            logger.debug("Messages:")
            for msg in safe_kwargs["messages"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                logger.debug(f"  {role}: {content}")

        # Log other parameters
        for key, value in safe_kwargs.items():
            if key != "messages":
                logger.debug(f"{key}: {value}")

        logger.debug("=== End Request ===")
    except Exception as e:
        logger.error(f"Error logging request: {str(e)}")


def log_response(operation: str, response: Any) -> None:
    """Log OpenAI API response details.

    All logs are at DEBUG level so they only appear when debug logging is enabled.
    """
    try:
        logger.debug(f"=== OpenAI Response: {operation} ===")

        # For OpenAI completion responses, log the content directly
        if hasattr(response, "choices") and len(response.choices) > 0:
            if hasattr(response.choices[0], "message") and hasattr(
                response.choices[0].message, "content"
            ):
                logger.debug(f"Content: {response.choices[0].message.content}")

            # Log model and usage info if available
            if hasattr(response, "model"):
                logger.debug(f"Model: {response.model}")
            if hasattr(response, "usage"):
                logger.debug(f"Usage: {response.usage}")
        else:
            # Fallback for other response types - just dump as string
            logger.debug(f"Response: {str(response)}")

        logger.debug("=== End Response ===")
    except Exception as e:
        logger.error(f"Error logging response: {str(e)}")


# Add a helper method to enable/disable debug logging at runtime
def set_debug_logging(enable: bool = False) -> None:
    """Enable or disable debug logging for OpenAI requests and responses.

    Args:
        enable: If True, sets the logger level to DEBUG; if False, sets it to INFO
    """
    level = logging.DEBUG if enable else logging.INFO
    logger.setLevel(level)

    # Also update the log level for any existing handlers
    for handler in logger.handlers:
        handler.setLevel(level)

    logger.info(f"OpenAI API logging level set to: {'DEBUG' if enable else 'INFO'}")
