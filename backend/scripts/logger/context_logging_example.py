#!/usr/bin/env python3
"""
Simple example demonstrating all log levels in discovita.utils.logger.

Run this script with different CONTEXT_DISPLAY settings to see how
context information appears in logs.

Examples:
    # No context (default)
    python context_logging_example.py

    # Function-only context
    CONTEXT_DISPLAY=function python context_logging_example.py

    # Class and function context
    CONTEXT_DISPLAY=class_function python context_logging_example.py

    # Full context with file and line information
    CONTEXT_DISPLAY=full python context_logging_example.py
"""

import os
from pathlib import Path

from discovita.utils.logger import configure_logging
from dotenv import load_dotenv

# Configure with a custom log filename
log = configure_logging(
    logger_name="logger_example",
    keep_logs=True,
    log_dir="../../logs",
    log_filename="custom_example.log",
    log_level="DEBUG",
)

load_dotenv()

# Load environment variables from .env file
current_file = Path(__file__)
project_root = current_file.parents[3]
env_path = project_root / ".env"

# Load environment variables
if env_path.exists():
    log.info(f"Loading environment variables from {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    log.warning(f"No .env file found at {env_path}")


def demonstrate_all_log_levels():
    """Simple function demonstrating all available log levels."""
    # Display current context display setting
    context_display = os.getenv("CONTEXT_DISPLAY")
    log.info(f"Running example with CONTEXT_DISPLAY={context_display}")
    log.info(f"Logs will be saved to logs/custom_example.log")

    print(f"\nStandard log levels")
    log.debug("This is a DEBUG level message")
    log.info("This is an INFO level message")
    log.warning("This is a WARNING level message")
    log.error("This is an ERROR level message")
    log.critical("This is a CRITICAL level message")

    print(f"\nCustom log levels")
    log.fine("This is a FINE level message")
    log.step("This is a STEP level message")
    log.success("This is a SUCCESS level message")


if __name__ == "__main__":
    demonstrate_all_log_levels()
