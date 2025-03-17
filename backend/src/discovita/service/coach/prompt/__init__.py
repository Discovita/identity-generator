"""Prompt management for coaching service."""

from pathlib import Path
from .manager import PromptManager
from .loader import PromptLoader
from .templates import PromptTemplate, Example, ExamplesCollection

def create_prompt_manager(prompts_dir: str = None) -> PromptManager:
    """Create and configure a prompt manager.
    
    Args:
        prompts_dir: Optional directory path for prompt files.
            If not provided, defaults to the 'prompts' directory in the same package.
    
    Returns:
        A configured PromptManager instance.
    """
    return PromptManager(prompts_dir)

__all__ = [
    'PromptManager',
    'PromptLoader',
    'PromptTemplate',
    'Example',
    'ExamplesCollection',
    'create_prompt_manager'
]
