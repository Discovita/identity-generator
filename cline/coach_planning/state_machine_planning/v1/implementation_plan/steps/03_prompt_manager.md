# Step 3: Create Prompt Manager

This document details the implementation of the prompt manager component for the coaching system, using markdown files for prompt content.

## Overview

The prompt manager is responsible for:

1. Loading prompt templates from markdown files
2. Providing state-specific prompts with appropriate context
3. Managing examples and counter-examples for each state
4. Defining allowed actions for each state

## Implementation Details

### 1. Create Prompt Manager Directory Structure

First, create the directory structure for the prompt manager components:

```
backend/src/discovita/service/coach/
├── prompt/
│   ├── __init__.py
│   ├── manager.py        # Prompt manager implementation
│   ├── loader.py         # Markdown file loader
│   └── templates.py      # Prompt template models
├── prompts/              # Directory for prompt markdown files
│   ├── states/           # State-specific prompts
│   │   ├── introduction.md
│   │   ├── identity_brainstorming.md
│   │   ├── identity_refinement.md
│   │   ├── identity_visualization.md
│   │   ├── action_planning.md
│   │   └── accountability.md
│   ├── examples/         # Example conversations
│   │   ├── introduction_examples.md
│   │   ├── brainstorming_examples.md
│   │   └── ...
│   ├── shared/           # Shared prompt components
│   │   ├── system_context.md
│   │   ├── identity_instructions.md
│   │   └── action_instructions.md
│   └── metadata/         # Metadata for prompts (allowed actions, etc.)
│       ├── introduction_meta.json
│       ├── brainstorming_meta.json
│       └── ...
```

### 2. Define Prompt Template Model

The prompt template model defines the structure of prompt templates and examples. See [templates.py](./03_prompt_manager/code/templates.py) for implementation details.

Key features:
- Strong typing with Pydantic models
- Use of enums for action types
- Support for examples and counter-examples
- Clear definition of required context keys

### 3. Implement Markdown Loader

The markdown loader handles loading and parsing prompt files from the filesystem. See [loader.py](./03_prompt_manager/code/loader.py) for implementation details.

Key features:
- Loads prompt content from markdown files
- Extracts YAML frontmatter for metadata
- Parses examples and counter-examples
- Converts string action names to ActionType enum values

### 4. Implement Prompt Manager

The prompt manager provides the main interface for getting prompts and allowed actions. See [manager.py](./03_prompt_manager/code/manager.py) for implementation details.

Key features:
- Loads all templates at initialization
- Formats prompts with context variables
- Validates required context keys
- Provides allowed actions for each state

### 5. Create Factory Function

A factory function simplifies creating and configuring the prompt manager. See [__init__.py](./03_prompt_manager/code/__init__.py) for implementation details.

### 6. Prompt File Format

Prompt files use markdown with YAML frontmatter for metadata. See [example_prompt.md](./03_prompt_manager/code/example_prompt.md) for an example.

Key features:
- YAML frontmatter for metadata
- Required context keys specified in metadata
- Allowed actions specified as enum values
- Markdown content with placeholders for context variables

### 7. Examples File Format

Example files contain examples and counter-examples for each state. See [example_examples.md](./03_prompt_manager/code/example_examples.md) for an example.

Key features:
- Clear section headers for examples and counter-examples
- Structured format for user and coach messages
- Descriptive titles for each example

## Next Steps

After implementing the prompt manager with markdown files:

1. Create all the necessary prompt markdown files for each state
2. Ensure the prompt manager integrates well with the state machine
3. Proceed to implementing the context manager in Step 4
