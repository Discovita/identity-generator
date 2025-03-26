# Discovitas OpenAI Client

A type-safe client for interacting with OpenAI's APIs, with strong support for structured responses.

## Core Features

1. **Structured Responses**: Get JSON responses that conform to Pydantic models
2. **Function Calling**: Define callable functions for the model to use
3. **Type Safety**: Full type checking with Pydantic models

## Structured Responses

The primary way to get structured data from OpenAI is through response models:

```python
from discovita.service.openai.models import LLMResponseModel
from pydantic import Field
from typing import List

class Identity(BaseModel):
    """An identity proposed by the coach."""
    category: str = Field(..., description="Category of identity (e.g. PASSIONS)")
    name: str = Field(..., description="Name of the identity")
    affirmation: str = Field(..., description="Affirmation statement")

class CoachResponse(LLMResponseModel):
    """Response from the coach."""
    message: str = Field(..., description="Coach's response message")
    actions: List[Action] = Field(
        default_factory=list,
        description="Actions to perform"
    )

# Get structured response
response = await client.get_structured_response_with_responses(
    input_data=input_data,
    response_model=CoachResponse
)

if response.is_valid:
    coach_response = response.parsed
    print(f"Message: {coach_response.message}")
    for action in coach_response.actions:
        print(f"Action: {action.type}")
```

Key points about structured responses:

1. Inherit from `LLMResponseModel` to get schema generation
2. Use Pydantic fields with descriptions
3. The model schema is automatically sent to OpenAI
4. Responses are validated against the model

## Function Calling

For cases where you need the model to call specific functions:

```python
from openai.types.responses import FunctionTool

# Define calculator function
calculator = FunctionTool(
    type="function",
    name="calculator",
    description="Perform basic arithmetic",
    parameters={
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": ["add", "subtract"]},
            "a": {"type": "number"},
            "b": {"type": "number"}
        }
    }
)

# Define handler
async def handle_calculator(args):
    op = args["operation"]
    a = args["a"]
    b = args["b"]
    return a + b if op == "add" else a - b

# Call function
response = await client.call_functions_with_responses(
    input_data="What is 5 plus 3?",
    functions=[calculator],
    function_handlers={"calculator": handle_calculator}
)
```

## Which Approach to Use?

- **Structured Responses**: When you want the model to return data in a specific format
- **Function Calling**: When you want the model to trigger specific actions

The coach service uses structured responses to get both the coach's message and any actions to perform, as this provides a cleaner separation between the model's response and action handling.

## API Reference

### Structured Responses

```python
async def get_structured_response_with_responses(
    self,
    input_data: ResponseInput,
    response_model: Type[T],
    model: str = "gpt-4o"
) -> StructuredResponseResult[T]
```

### Function Calling

```python
async def call_functions_with_responses(
    self,
    input_data: ResponseInput,
    functions: List[FunctionTool],
    function_handlers: Dict[str, Callable]
) -> Response
```

## Testing

The client includes a test mode:

```python
# Initialize test client
client = OpenAIClient(api_key="fake-key", test_mode=True)

# No actual API calls will be made
response = await client.get_structured_response_with_responses(
    input_data="test",
    response_model=CoachResponse
)
