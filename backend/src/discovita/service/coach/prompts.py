"""Coaching system prompts and dialogue management."""

import os

def load_prompt_file(filename):
    """Load content from a text file in the same directory."""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return ""

# Load the system prompt from the text file
SYSTEM_PROMPT = load_prompt_file("prompts.txt")

def load_sample_dialogue() -> str:
    """Load sample dialogue for reference in prompts."""
    dialogue_path = os.path.join(
        os.path.dirname(__file__),
        "sample_dialogue.txt"
    )
    if os.path.exists(dialogue_path):
        with open(dialogue_path, "r") as f:
            return f.read()
    return ""
