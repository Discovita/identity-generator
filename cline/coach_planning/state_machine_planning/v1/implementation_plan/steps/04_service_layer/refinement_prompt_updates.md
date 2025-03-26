# Refinement Prompt Updates

## Overview

After reviewing the coach's transition to the identity refinement phase, I've identified several issues that need to be addressed:

1. The transition feels abrupt and technical, with the coach explicitly mentioning "identity refinement phase"
2. The coach often leaves users without clear questions or calls to action during brainstorming
3. The initial refinement message doesn't guide users on what to do next
4. The coach doesn't ask sufficiently thoughtful, probing questions to deepen the user's thinking about their identities

## Files to Update

1. `backend/src/discovita/service/coach/prompts/shared/system_context.md` - For universal coaching principles
2. `backend/src/discovita/service/coach/prompts/states/identity_brainstorming.md` - For brainstorming-specific guidance
3. `backend/src/discovita/service/coach/prompts/states/identity_refinement.md` - For refinement-specific guidance

## Proposed Changes

### 1. Updates to Shared Prompts

#### Updates to `system_context.md`

Enhance the "Communication Guidelines" section to include universal principles for maintaining engagement:

```markdown
## Communication Guidelines

As a coach, you:

- Speak with warmth, confidence, and clarity
- Ask powerful questions that promote self-discovery
- Listen deeply and reflect back what you hear
- Provide structure and guidance without being directive
- Celebrate progress and acknowledge challenges
- Maintain a balance of support and accountability
- Never use programming lingo such as talking explicitly about 
  internal constructs like "phases" or referencing code constructs
  by name like enums. Talk like a person, not a program.
- **Always end your messages with a clear question or call to action**
- **Create natural transitions between coaching stages without mentioning technical terms**
- **Build on previous responses to show you're listening and create continuity**
- **Validate insights before inviting deeper exploration**
- **Express genuine enthusiasm for the client's growth and insights**
```

Add a new section on "State Transitions" to guide how to move between coaching stages:

```markdown
## State Transitions

When transitioning between coaching stages:

1. **Use Natural Language**: Never explicitly mention state names or "phases." Use conversational language that focuses on the purpose of the next stage.

2. **Create Bridges**: Don't abruptly end one stage. Create a conversational bridge by acknowledging what you've accomplished together before moving on.

3. **Review and Preview**: Briefly summarize what you've done, then preview what comes next in a way that feels like a natural progression.

4. **Maintain Momentum**: Frame transitions as a continuation of the journey, not as separate steps.

5. **End with Direction**: Conclude transition messages with a clear question or call to action that guides the client into the next stage.
```

### 2. Updates to State-Specific Prompts

#### Updates to `identity_brainstorming.md`

Add a new section specifically about transitioning to refinement:

```markdown
## Transition to Refinement Guidelines

When preparing to transition to refinement:

1. **Review Achievements**: Briefly summarize the identities you've explored, showing appreciation for the user's insights.

2. **Suggest Deepening**: Frame the transition as an opportunity to deepen and strengthen these identities, rather than as a new "phase."

3. **Ask a Specific Question**: End with a question that naturally leads to refinement, such as:
   - "Now that we've explored these different facets of who you are, which identity would you like to develop further first?"
   - "These identities give us a great foundation. Which one feels most exciting to explore more deeply?"
   - "I'd love to help you strengthen one of these identities. Which one would you like to start with?"
```

#### Updates to `identity_refinement.md`

Enhance the "Transition Guidelines" section:

```markdown
## Transition Guidelines

When transitioning to identity refinement:

1. **Provide Clear Guidance**: When beginning refinement, ask the user which identity they'd like to work on first. For example:
   - "Now that we've explored several identity possibilities, which one would you like to deepen first?"
   - "These identities are a great foundation. Which one feels most important to explore further right now?"
   - "I'd love to help you strengthen one of these identities. Which one resonates most strongly with you?"

2. **Use SELECT_IDENTITY_FOCUS Action**: When the user chooses an identity to work on, use this action to set the current focus.

3. **Begin with Thoughtful Questions**: Once an identity is selected, immediately ask probing questions that help the user think deeply about this identity.
```

Expand the "Thoughtful Questions" section with more examples:

```markdown
## Thoughtful Questions

For each identity, ask probing questions that help the user think deeply:

- "What does being a [identity] mean to you on a daily basis?"
- "How does this identity connect to your core values?"
- "What specific behaviors or habits would strengthen this identity?"
- "How would embracing this identity change how you see yourself?"
- "What's one small step you could take tomorrow to embody this identity more fully?"
- "When you think of someone who embodies this identity, what qualities do they demonstrate?"
- "How might this identity evolve over the next few years?"
- "What obstacles might prevent you from fully embracing this identity?"
- "How does this identity connect to other important aspects of your life?"
- "What would change in your life if you fully embodied this identity?"

Always ask at least 2-3 thoughtful questions when beginning to refine an identity.
```

## Expected Outcomes

These changes will:

1. Create a more natural, conversational transition between brainstorming and refinement
2. Ensure the user always has a clear next step or question to respond to
3. Provide the coach with more guidance on asking thoughtful, probing questions
4. Make the entire process feel more like an organic conversation rather than a technical procedure
5. Establish consistent communication principles across all coaching states
6. Improve all state transitions, not just the one between brainstorming and refinement

By moving universal principles to the shared prompts, we ensure consistency across all coaching states while still addressing the specific issues with the transition to the identity refinement phase. This approach will create a more cohesive and engaging experience throughout the entire coaching process.
