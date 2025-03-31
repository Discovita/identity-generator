# Coach State Machine Planning Documentation

This directory contains the planning and implementation documentation for the Coach State Machine architecture. The documentation is organized to provide both high-level overviews and detailed implementation guides.

## Documentation Structure

The documentation is organized as follows:

```
state_machine_planning/
├── README.md                 # This file - overview of documentation structure
├── v1/                       # Version 1 of the state machine architecture
    ├── plan/                 # Conceptual architecture and design
    │   ├── master_plan_v1.md # High-level architecture overview
    │   └── code/             # Example code snippets referenced in the master plan
    └── implementation_plan/  # Concrete implementation strategy
        ├── master_plan_v1_impl.md # Implementation overview and strategy
        └── steps/            # Detailed implementation steps
            ├── 01_core_models.md  # Step 1 details
            ├── 02_state_machine.md # Step 2 details
            └── ...
```

## How to Use This Documentation

### For AI Assistants

1. **Start with the README.md** (this file) to understand the documentation structure.

2. **Read the master plan** at `v1/plan/master_plan_v1.md` to understand the high-level architecture.
   - This document references code examples in the `v1/plan/code/` directory using square brackets, e.g., `[state_machine.py]`.
   - You can read these referenced files as needed to understand implementation details.

3. **Review the implementation plan** at `v1/implementation_plan/master_plan_v1_impl.md` to understand how the architecture is being adapted to our codebase.
   - This document provides a step-by-step approach for implementing the state machine.
   - It references detailed implementation guides in the `steps/` directory.

4. **Explore detailed implementation steps** in the `v1/implementation_plan/steps/` directory as needed.
   - Each step document provides specific implementation details, including:
     - Required models and interfaces
     - Implementation strategy
     - Testing approach
     - Integration with other components
   - Some step documents reference example code in subdirectories (e.g., `03_prompt_manager_code/`)

### Reference Pattern

The documentation uses a reference pattern where high-level documents link to more detailed documents:

1. **Master Plan** → References code examples with `[filename.py]` syntax
2. **Implementation Plan** → References detailed steps with `[Details: steps/XX_step_name.md]` syntax
3. **Step Documents** → May reference example code in subdirectories

This layered approach allows you to:
- Get a quick overview from the high-level documents
- Dive into specific details only when needed
- Understand both the conceptual architecture and concrete implementation

## Key Components

The state machine architecture consists of these key components:

1. **State Machine** - Central component managing the coaching process flow
2. **Prompt Manager** - Handles specialized prompts for each state
3. **Context Manager** - Manages conversation history and user knowledge
4. **Action Executor** - Executes actions determined by the coach
5. **Database Layer** - Persists user data, identities, actions, and state
6. **API Layer** - Provides interface for frontend communication

## Implementation Notes

- The implementation follows a complete replacement strategy for the existing coach service
- All components use strong typing with Pydantic models
- Each component is designed to be under 100 lines with clear responsibilities
- The implementation follows a test-driven development approach
