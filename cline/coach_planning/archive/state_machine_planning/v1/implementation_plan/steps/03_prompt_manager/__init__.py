from .manager import PromptManager
from .templates import PromptTemplate, Example

def create_prompt_manager(prompts_dir: str = None) -> PromptManager:
    """Create and configure a prompt manager."""
    return PromptManager(prompts_dir)

__all__ = [
    'PromptManager',
    'PromptTemplate',
    'Example',
    'create_prompt_manager'
]
