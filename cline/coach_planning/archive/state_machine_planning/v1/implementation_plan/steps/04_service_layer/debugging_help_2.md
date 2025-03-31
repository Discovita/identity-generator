# String Formatting Bug in Coach Service

## Error
```
KeyError: ' "type"'
```

The coach API is failing with this error when trying to format prompt templates. The error occurs in the prompt manager's get_prompt method when trying to format a template with context variables.

## Stack Trace
```python
api/routes/coach.py:16 -> handle_user_input
  service/coach/service.py:49 -> process_message
    service/coach/prompt/manager.py:52 -> get_prompt
      template.template.format(...)  # Error occurs here
```

## Issue Description

The error occurs because Python's string formatter is encountering unescaped curly braces in our markdown templates and interpreting them as format placeholders. Specifically, it's trying to find a variable named "type" which isn't provided in the format arguments.

This is happening because our templates contain JSON examples like:
```json
{ "type": "TRANSITION_STATE", "params": { "to_state": "IDENTITY_BRAINSTORMING" } }
```

We attempted to fix this by wrapping these examples in markdown code blocks:
```markdown
Example:
```json
{ "type": "TRANSITION_STATE", "params": { "to_state": "IDENTITY_BRAINSTORMING" } }
```
```

However, the error persists. This suggests either:
1. The markdown code block syntax isn't being preserved during template loading
2. The template loading process is stripping the code block markers
3. There are other unescaped curly braces we haven't found

Need guidance on best approach to fix this - either by properly escaping all curly braces or by modifying how templates are loaded and processed.
