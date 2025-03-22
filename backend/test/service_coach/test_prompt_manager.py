"""Tests for the prompt manager component."""

import pytest
from pathlib import Path
import os
import re
from typing import Dict, Any, List, Set

from discovita.service.coach.models import CoachingState, ActionType, CoachContext
from discovita.service.coach.prompt import PromptManager, PromptLoader, PromptTemplate, Example, ExamplesCollection

# Test directory for prompt files
TEST_PROMPTS_DIR = Path(__file__).parent / "test_prompts"

@pytest.fixture
def setup_test_prompts(tmp_path):
    """Set up test prompt files in a temporary directory."""
    # Create directory structure
    states_dir = tmp_path / "states"
    examples_dir = tmp_path / "examples"
    shared_dir = tmp_path / "shared"
    metadata_dir = tmp_path / "metadata"
    
    for directory in [states_dir, examples_dir, shared_dir, metadata_dir]:
        directory.mkdir()
    
    # Create a test prompt file with explicit string values for allowed actions
    with open(states_dir / "introduction.md", "w") as f:
        f.write("""---
required_context_keys:
  - user_summary
  - recent_messages
allowed_actions:
  - save_user_info
  - mark_introduction_complete
  - transition_state
---

# Introduction State

You are Leigh Ann, a professional life coach. Your goal is to introduce the client to your coaching process.

## Current Context

Current user information: {user_summary}

Recent conversation: {recent_messages}
""")
    
    # Create a test examples file with very clear formatting
    with open(examples_dir / "introduction_examples.md", "w") as f:
        f.write("""# Examples

## Test Example

User: Hi, I'm new here.

Coach: Welcome! I'm Leigh Ann, your personal life coach.

# Counter-Examples

## Test Counter-Example

User: Hi, I'm new here.

Coach: Let's jump straight into identifying your core values.
""")
    
    return tmp_path

@pytest.fixture
def context():
    """Create a test context."""
    from discovita.service.coach.models.chat import ChatMessage
    return CoachContext(
        user_id="test_user",
        current_state=CoachingState.INTRODUCTION,
        conversation_history=[
            ChatMessage(role="user", content="Hello")
        ],
        consolidated_summary="Test user summary",
        metadata={}
    )

def test_prompt_loader_load_template(setup_test_prompts):
    """Test loading a prompt template."""
    loader = PromptLoader(str(setup_test_prompts))
    template = loader.load_template(CoachingState.INTRODUCTION)
    
    assert template.state == CoachingState.INTRODUCTION
    assert "Introduction State" in template.template
    assert "user_summary" in template.required_context_keys
    assert "recent_messages" in template.required_context_keys
    assert ActionType.SAVE_USER_INFO in template.allowed_actions
    assert ActionType.MARK_INTRODUCTION_COMPLETE in template.allowed_actions
    assert ActionType.TRANSITION_STATE in template.allowed_actions
    assert len(template.examples) == 1
    assert len(template.counter_examples) == 1

def test_prompt_loader_extract_examples(setup_test_prompts):
    """Test extracting examples from a markdown file."""
    loader = PromptLoader(str(setup_test_prompts))
    examples_path = setup_test_prompts / "examples" / "introduction_examples.md"
    examples = loader._load_examples(examples_path)
    
    assert len(examples.examples) == 1
    assert examples.examples[0].user == "Hi, I'm new here."
    assert "Welcome!" in examples.examples[0].coach
    assert examples.examples[0].description == "Test Example"
    
    assert len(examples.counter_examples) == 1
    assert examples.counter_examples[0].user == "Hi, I'm new here."
    assert "Let's jump straight into" in examples.counter_examples[0].coach
    assert examples.counter_examples[0].description == "Test Counter-Example"

def test_prompt_manager_get_prompt(setup_test_prompts, context):
    """Test getting a formatted prompt."""
    manager = PromptManager(str(setup_test_prompts))
    prompt = manager.get_prompt(CoachingState.INTRODUCTION, context)
    
    assert "Introduction State" in prompt
    assert "Test user summary" in prompt
    assert "# Examples" in prompt
    assert "# Counter-Examples" in prompt

def test_prompt_manager_get_allowed_actions(setup_test_prompts):
    """Test getting allowed actions for a state."""
    manager = PromptManager(str(setup_test_prompts))
    actions = manager.get_allowed_actions(CoachingState.INTRODUCTION)
    
    assert ActionType.SAVE_USER_INFO in actions
    assert ActionType.MARK_INTRODUCTION_COMPLETE in actions
    assert ActionType.TRANSITION_STATE in actions
    assert len(actions) == 3

def test_prompt_manager_missing_context_keys(setup_test_prompts):
    """Test error when required context keys are missing."""
    manager = PromptManager(str(setup_test_prompts))
    context = CoachContext(
        user_id="test_user",
        current_state=CoachingState.INTRODUCTION,
        conversation_history=[],
        # Missing consolidated_summary which provides user_summary
        metadata={}
    )
    
    with pytest.raises(ValueError) as excinfo:
        manager.get_prompt(CoachingState.INTRODUCTION, context)
    
    assert "Missing required context keys" in str(excinfo.value)

def test_prompt_manager_reload_templates(setup_test_prompts, context):
    """Test reloading templates."""
    manager = PromptManager(str(setup_test_prompts))
    
    # Get initial prompt
    prompt1 = manager.get_prompt(CoachingState.INTRODUCTION, context)
    
    # Modify the template file
    with open(setup_test_prompts / "states" / "introduction.md", "a") as f:
        f.write("\n\n## Additional Content\n\nThis was added after loading.")
    
    # Reload templates
    manager.reload_templates()
    
    # Get updated prompt
    prompt2 = manager.get_prompt(CoachingState.INTRODUCTION, context)
    
    assert "Additional Content" in prompt2
    assert prompt1 != prompt2
