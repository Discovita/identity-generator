# Summary of Changes for Step 3: Prompt Manager

## Overview

This step implemented the prompt manager component of the coaching system. The prompt manager is responsible for loading prompt templates from markdown files, providing state-specific prompts with appropriate context, and managing examples and allowed actions for each state.

## Changes Made

1. Created new files in `backend/src/discovita/service/coach/prompt/`:
   - `__init__.py`: Exports the prompt manager factory function
   - `manager.py`: Implements the `PromptManager` class
   - `loader.py`: Implements the `PromptLoader` class for loading markdown files
   - `templates.py`: Defines the prompt template models

2. Created prompt files in `backend/src/discovita/service/coach/prompts/`:
   - `states/`: Contains state-specific prompt templates
     - `introduction.md`: Prompt for the introduction state
     - `identity_brainstorming.md`: Prompt for the identity brainstorming state
     - `identity_refinement.md`: Prompt for the identity refinement state
     - `identity_visualization.md`: Prompt for the identity visualization state
     - `action_planning.md`: Prompt for the action planning state
     - `accountability.md`: Prompt for the accountability state
   - `examples/`: Contains example conversations for each state
     - `introduction_examples.md`: Examples for the introduction state
     - `identity_brainstorming_examples.md`: Examples for the identity brainstorming state
     - `identity_refinement_examples.md`: Examples for the identity refinement state
     - `identity_visualization_examples.md`: Examples for the identity visualization state
     - `action_planning_examples.md`: Examples for the action planning state
     - `accountability_examples.md`: Examples for the accountability state
   - `shared/`: Contains shared prompt components
     - `system_context.md`: System context for all prompts
     - `identity_instructions.md`: Instructions for identity-related prompts
     - `action_instructions.md`: Instructions for action-related prompts

3. Enhanced the regex patterns in the `PromptLoader` class to better handle various markdown formats and example structures.

4. Added type annotations to all components to ensure type safety.

## Component Details

### PromptTemplate Model

The `PromptTemplate` model defines the structure of prompt templates:
- `state`: The coaching state this template is for
- `template`: The prompt template with placeholders
- `required_context_keys`: Required keys in the context
- `examples`: Example conversations
- `counter_examples`: Counter-examples
- `allowed_actions`: Allowed actions in this state

### Example Model

The `Example` model defines the structure of example conversations:
- `user`: User message
- `coach`: Coach response
- `description`: Description of the example

### PromptLoader Class

The `PromptLoader` class handles loading and parsing prompt files:
- `load_template`: Loads a prompt template for a specific state
- `_read_markdown_file`: Reads a markdown file and returns its contents
- `_extract_frontmatter`: Extracts YAML frontmatter from markdown content
- `_load_examples`: Loads examples and counter-examples from a markdown file
- `_extract_section`: Extracts a section from markdown content
- `_parse_examples`: Parses examples from a markdown section

### PromptManager Class

The `PromptManager` class provides the main interface for getting prompts:
- `get_prompt`: Gets a formatted prompt for the current state
- `get_allowed_actions`: Gets the allowed actions for the current state
- `reload_templates`: Reloads all templates from disk

## Prompt File Format

Prompt files use markdown with YAML frontmatter for metadata:
```markdown
---
required_context_keys:
  - user_summary
  - recent_messages
allowed_actions:
  - SAVE_USER_INFO
  - MARK_INTRODUCTION_COMPLETE
  - TRANSITION_STATE
---

# Introduction State

You are Leigh Ann, a professional life coach. Your goal is to introduce the client to your coaching process.

## Current Context

Current user information: {user_summary}

Recent conversation: {recent_messages}
```

## Examples File Format

Example files contain examples and counter-examples for each state:
```markdown
# Examples

## Effective Introduction

User: Hi, I'm new here and not sure how this works.

Coach: Welcome! I'm Leigh Ann, your personal life coach.

# Counter-Examples

## Too Vague

User: Hi, I'm new here.

Coach: Let's jump straight into identifying your core values.
```

## Technical Notes

- All components use strong typing with clear type annotations
- The prompt manager is designed to be extensible, allowing new prompt templates to be added
- The implementation includes comprehensive tests for all functionality
- The prompt manager integrates with the `CoachContext` model from Step 1
- The implementation uses regex patterns to parse markdown files, with fallback patterns for different formats
