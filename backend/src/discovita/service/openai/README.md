# Discovitas OpenAI Client

A type-safe client for interacting with OpenAI's APIs, with strong support for structured responses and function calling.

## Core Features

1. **Unified API**: A single, flexible interface for all OpenAI Responses API operations
2. **Structured Responses**: Get JSON responses that conform to Pydantic models
3. **Function Calling**: Define callable functions for the model to use
4. **Type Safety**: Full type checking with Pydantic models
5. **Simplified Code**: Clean, maintainable implementation with minimal abstractions

## Using the Unified API

The client provides a single unified method for all interactions with the OpenAI Responses API:

```python
from discovita.service.openai.client import OpenAIClient
from discovita.service.openai.models import ResponseInput

client = OpenAIClient(api_key="your-key")

# The behavior changes based on which parameters you provide:
# 1. Basic response - Just provide input
# 2. Structured output - Provide response_model
# 3. Function calling - Provide tools and handlers
```

### Basic Response

```python
# Simple text-based response
response = await client.get_response_with_responses(
    input_data=ResponseInput.from_str("Tell me a joke about programming")
)

# Access the output
print(response.output_text)  # Outputs the raw text response
```

### Structured Responses

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
result = await client.get_response_with_responses(
    input_data=ResponseInput.from_str("Generate a new identity for me"),
    response_model=CoachResponse
)

if result.is_valid:
    coach_response = result.parsed
    print(f"Message: {coach_response.message}")
    for action in coach_response.actions:
        print(f"Action: {action.type}")
```

### Function Calling

```python
from openai.types.responses import Tool

# Define a calculator tool
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform basic arithmetic",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "subtract"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    }
}

# Define handler function
async def calculator_handler(args):
    op = args["operation"]
    a = args["a"]
    b = args["b"]
    return a + b if op == "add" else a - b

# Call functions
response = await client.get_response_with_responses(
    input_data=ResponseInput.from_str("What is 5 plus 3?"),
    tools=[calculator_tool],
    handlers={"calculator": calculator_handler}
)

print(response.output_text)  # Will include the result after function execution
```

## Key Concepts

### ResponseInput

The `ResponseInput` class represents input to the model and provides convenient methods:

```python
# From a string
input_data = ResponseInput.from_str("Hello, how are you?")

# From a list of message objects
input_data = ResponseInput.from_messages([
    ResponsesMessage(role="user", content="Hello"),
    ResponsesMessage(role="assistant", content="Hi there!")
])

# From a list of dictionaries
input_data = ResponseInput.from_dict_list([
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
])
```

### StructuredResponseResult

When using a response model, the result is wrapped in a `StructuredResponseResult`:

```python
result = await client.get_response_with_responses(
    input_data=input_data,
    response_model=CoachResponse
)

# Check if the response is valid
if result.is_valid:
    # Access the parsed model
    model = result.parsed
    
    # Access the raw response
    raw_response = result.response
else:
    # Handle error
    print(f"Error: {result.error}")
```

## Which Approach to Use?

- **Basic Response**: When you just need simple text responses
- **Structured Responses**: When you want the model to return data in a specific format
- **Function Calling**: When you want the model to trigger specific actions in your code

The coach service uses structured responses to get both the coach's message and any actions to perform, as this provides a cleaner separation between the model's response and action handling.

## API Reference

### Unified Response Method

```python
async def get_response_with_responses(
    self,
    input_data: ResponseInput,
    model: str = "gpt-4o",
    response_model: Optional[Type[T]] = None,
    schema_name: Optional[str] = None,
    tools: Optional[List[Union[Tool, Dict[str, Any]]]] = None,
    tool_choice: Optional[ToolChoice] = None,
    handlers: Optional[Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]]] = None,
    auto_handle_functions: bool = True,
    store: bool = True,
    previous_response_id: Optional[str] = None,
) -> Union[Response, StructuredResponseResult[T]]
```

## Testing

The client includes a test mode:

```python
# Initialize test client
client = OpenAIClient(api_key="fake-key", test_mode=True)

# No actual API calls will be made
response = await client.get_response_with_responses(
    input_data=ResponseInput.from_str("test"),
    response_model=CoachResponse
)