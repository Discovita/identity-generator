import os
import json
import re
from typing import Dict, Any, List, Optional, Set, Tuple
import yaml
from pathlib import Path

from discovita.service.coach.models import CoachingState, ActionType
from .templates import PromptTemplate, Example

class PromptLoader:
    """Loads prompt templates from markdown files."""
    
    def __init__(self, prompts_dir: str = None):
        """Initialize the loader with the prompts directory."""
        if prompts_dir is None:
            # Default to the prompts directory in the same package
            self.prompts_dir = Path(__file__).parent.parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_dir)
    
    def load_template(self, state: CoachingState) -> PromptTemplate:
        """Load a prompt template for a specific state."""
        # Load the main template content
        state_name = state.value
        template_path = self.prompts_dir / "states" / f"{state_name}.md"
        template_content = self._read_markdown_file(template_path)
        
        # Extract frontmatter metadata if present
        template_content, metadata = self._extract_frontmatter(template_content)
        
        # Load examples
        examples_path = self.prompts_dir / "examples" / f"{state_name}_examples.md"
        examples = self._load_examples(examples_path)
        
        # Load metadata from JSON if not in frontmatter
        if not metadata:
            metadata_path = self.prompts_dir / "metadata" / f"{state_name}_meta.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
        
        # Get required context keys
        required_keys = metadata.get("required_context_keys", [])
        
        # Get allowed actions
        allowed_actions = set()
        for action_name in metadata.get("allowed_actions", []):
            try:
                allowed_actions.add(ActionType(action_name))
            except ValueError:
                # Log warning about invalid action
                pass
        
        # Create and return the template
        return PromptTemplate(
            state=state,
            template=template_content,
            required_context_keys=required_keys,
            examples=examples.get("examples", []),
            counter_examples=examples.get("counter_examples", []),
            allowed_actions=allowed_actions
        )
    
    def _read_markdown_file(self, path: Path) -> str:
        """Read a markdown file and return its contents."""
        if not path.exists():
            return ""
        
        with open(path, "r") as f:
            return f.read()
    
    def _extract_frontmatter(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """Extract YAML frontmatter from markdown content."""
        frontmatter_pattern = r"^---\n(.*?)\n---\n"
        match = re.search(frontmatter_pattern, content, re.DOTALL)
        
        if not match:
            return content, {}
        
        frontmatter_yaml = match.group(1)
        try:
            metadata = yaml.safe_load(frontmatter_yaml)
            # Remove frontmatter from content
            content = re.sub(frontmatter_pattern, "", content, flags=re.DOTALL)
            return content, metadata
        except yaml.YAMLError:
            # If YAML parsing fails, return original content
            return content, {}
    
    def _load_examples(self, path: Path) -> Dict[str, List[Example]]:
        """Load examples and counter-examples from a markdown file."""
        content = self._read_markdown_file(path)
        if not content:
            return {"examples": [], "counter_examples": []}
        
        # Extract sections
        examples_section = self._extract_section(content, "# Examples")
        counter_examples_section = self._extract_section(content, "# Counter-Examples")
        
        # Parse examples
        examples = self._parse_examples(examples_section)
        counter_examples = self._parse_examples(counter_examples_section)
        
        return {
            "examples": examples,
            "counter_examples": counter_examples
        }
    
    def _extract_section(self, content: str, section_header: str) -> str:
        """Extract a section from markdown content."""
        pattern = f"{re.escape(section_header)}(.*?)(?:^#|$)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        if not match:
            return ""
        return match.group(1).strip()
    
    def _parse_examples(self, section: str) -> List[Example]:
        """Parse examples from a markdown section."""
        examples = []
        
        # Pattern for example blocks
        example_pattern = r"## (.*?)\n\n.*?User: (.*?)\n\nCoach: (.*?)(?=\n\n##|\Z)"
        matches = re.finditer(example_pattern, section, re.DOTALL)
        
        for match in matches:
            description = match.group(1).strip()
            user_message = match.group(2).strip()
            coach_response = match.group(3).strip()
            
            examples.append(Example(
                user=user_message,
                coach=coach_response,
                description=description
            ))
        
        return examples
