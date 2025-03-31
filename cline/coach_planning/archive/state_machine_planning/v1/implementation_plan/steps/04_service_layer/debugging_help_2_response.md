It looks like you've done a thorough job analyzing the issue! Based on your description, the `KeyError: ' "type"'` is likely caused by unescaped curly braces in your markdown templates. Let's break down the debugging process and potential fixes step by step:

---

## Debugging Steps

### 1. **Verify Template Content Before Formatting**
Add debug logging to print the raw template content after it's loaded but before formatting. This will help confirm whether the issue originates from unescaped curly braces in the markdown template.

```python
def load_template(self, state: CoachingState) -> PromptTemplate:
    state_name = state.value
    template_path = self.prompts_dir / "states" / f"{state_name}.md"
    template_content = self._read_markdown_file(template_path)
    
    # Debug: Print raw template content
    print(f"Loaded template for state {state_name}: {template_content}")
    
    return PromptTemplate(template=template_content)
```

Run your code and inspect the logs for any suspicious `{}` placeholders in the raw markdown content.

---

### 2. **Check Markdown Code Block Syntax**
Markdown code blocks should preserve their content as-is, but if your `_read_markdown_file` function or downstream processing strips formatting or escapes characters incorrectly, it could cause issues. Ensure that:

- The code block syntax (` ```json `) is intact.
- Curly braces inside code blocks are not being interpreted as placeholders.

If you suspect code blocks are being altered, consider explicitly escaping curly braces in JSON examples within your templates:

```
{{ "type": "TRANSITION_STATE", "params": {{ "to_state": "IDENTITY_BRAINSTORMING" }} }}
```

---

### 3. **Escape All Curly Braces in Templates**
Python's string formatter treats `{}` as placeholders, so any literal curly braces in your templates must be escaped by doubling them (`{{` and `}}`). For example:

```
Example:
```json
{{ "type": "TRANSITION_STATE", "params": {{ "to_state": "IDENTITY_BRAINSTORMING" }} }}
```

To automate this process:
- Write a script to scan all markdown files for unescaped curly braces.
- Replace single `{` and `}` with `{{` and `}}`.

---

### 4. **Add Validation for Templates**
Before formatting templates, validate their content to ensure all placeholders are properly escaped. You can use regular expressions to detect unescaped curly braces:

```python
import re

def validate_template(template_content: str):
    # Regex to find unescaped curly braces
    unescaped_curly_braces = re.findall(r'(?<!{){(?!{)|(?<!})}(?!})', template_content)
    if unescaped_curly_braces:
        raise ValueError(f"Template contains unescaped curly braces: {unescaped_curly_braces}")
```

Call this function when loading templates to catch formatting issues early.

---

### 5. **Check All Template Files**
Ensure you've reviewed every markdown file in `backend/src/discovita/service/coach/prompts/states/`. If possible, write a script to scan all files for `{}` placeholders that aren't properly escaped.

Example script:

```python
import os

def scan_templates_for_unescaped_curly_braces(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    if '{' in content or '}' in content:
                        print(f"Potential issue in file: {path}")
                        print(content)

scan_templates_for_unescaped_curly_braces("backend/src/discovita/service/coach/prompts/states/")
```

---

## Fixing the Bug

### Option 1: Escape Curly Braces in Templates
Manually or programmatically escape all `{}` placeholders in your markdown files.

### Option 2: Update Template Loading Logic
If escaping curly braces isn't ideal (e.g., it makes templates harder to read), consider using a different placeholder syntax (e.g., `[[variable]]`) and replace it dynamically before formatting:

```python
template_content = template_content.replace("[[", "{").replace("]]", "}")
formatted_prompt = template_content.format(...)
```

---

## Next Steps

1. Implement debug logging to confirm where the issue originates.
2. Validate all templates for unescaped curly braces.
3. Decide whether to escape `{}` manually or switch to an alternative placeholder syntax.
4. Test thoroughly with all state templates to ensure the fix works across the board.

Let me know how it goes or if you'd like help with specific parts of this process!

---
Answer from Perplexity: pplx.ai/share