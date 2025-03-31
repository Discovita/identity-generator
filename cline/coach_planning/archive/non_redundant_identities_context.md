# Preventing Redundant Identities in the Coach System

This document provides context for implementing a solution to prevent the coach from creating redundant identities during coaching sessions.

## Problem Description

Currently, the coach sometimes creates redundant identities during a coaching session. For example:

1. The user might create an identity of "Loving Father" early in the session
2. Later in the session, if the user references this identity, the coach might create a new "Loving Father" identity instead of referencing the existing one

This redundancy creates confusion and clutters the identity list with duplicate entries.

## Root Cause Analysis

The likely causes of this issue are:

1. **Insufficient Context**: The existing identities may not be properly included in the prompt context during identity brainstorming and refinement stages
2. **Lack of Clear Instructions**: The prompts may not explicitly instruct the coach to avoid creating redundant identities
3. **Missing Identity Checking**: The coach may not be checking if a similar identity already exists before creating a new one

## Current Codebase Structure

### Prompt Context Building

The prompt context is built in:
- `backend/src/discovita/service/coach/prompt_manager.py`

This is where the identities should be included in the context for all relevant prompts.

### Prompt Templates

The identity-related prompt templates are in:
- `backend/src/discovita/service/coach/prompts/states/identity_brainstorming.md`
- `backend/src/discovita/service/coach/prompts/states/identity_refinement.md`

These templates should include clear instructions about avoiding redundant identities.

### State Management

The coach state, including identities, is managed in:
- `backend/src/discovita/service/coach/models/state.py`
- `backend/src/discovita/service/coach/actions/handler.py`

## Required Changes

1. **Verify Identity Context in Prompts**:
   - Ensure that the `identities` context key is properly populated in all relevant prompts
   - Confirm that the identities are being formatted in a way that makes them easily recognizable to the LLM

2. **Update Prompt Instructions**:
   - Add explicit instructions in both identity_brainstorming.md and identity_refinement.md to:
     - Review existing identities before creating new ones
     - Reference existing identities rather than creating duplicates
     - Suggest modifications to existing identities when appropriate instead of creating new ones

3. **Enhance Identity Display in Prompts**:
   - Format the identities in the prompt to make them more prominent
   - Include both the identity description and ID to make referencing easier

4. **Consider Adding Similarity Detection**:
   - Optionally, implement a mechanism to detect when a proposed identity is similar to an existing one
   - This could be done at the service layer before sending the action to the handler

## Implementation Strategy

1. First, verify that identities are being included in the prompt context
2. Update the prompt templates with clear instructions about avoiding redundancy
3. Test the changes to ensure they effectively prevent redundant identities
4. If necessary, implement additional safeguards at the service layer

## Testing

The changes can be tested by:
- Manual testing with scenarios that previously led to redundant identities
- Unit tests that verify identities are properly included in the prompt context
- Integration tests that simulate a coaching session with identity references

## Expected Outcome

After implementing these changes, the coach should:
1. Recognize when a user is referring to an existing identity
2. Reference existing identities rather than creating new ones
3. Suggest modifications to existing identities when appropriate
4. Only create new identities when they are genuinely distinct from existing ones
