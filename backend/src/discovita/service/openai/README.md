# OpenAI Helper

A modular Python package for interacting with OpenAI's API, providing a simplified interface with support for:

- Text completions
- Image inputs (multimodal)
- Image generation with DALL-E models
- Vision capabilities for image analysis
- JSON mode
- Structured outputs
- Streaming responses
- Automatic parsing of responses into Pydantic models
- Conversation history management
- Support for the latest models (GPT-4.5-preview, O1, O1-mini, O3-mini, GPT-4o, GPT-4o-mini)

## Module Structure

The module is organized into the following directories:

```
openai/
├── __init__.py              # Main entry point
├── core/                    # Core functionality
│   ├── __init__.py          # Exports core components
│   ├── base.py              # Base OpenAIService class
│   ├── chat/                # Chat completion functionality
│   │   ├── generic/         # Generic chat completion handlers
│   │   └── structured/      # Structured output chat completion
│   │       ├── __init__.py
│   │       ├── mixin.py     # Structured completion functionality
│   │       ├── streaming.py # Backward compatibility for streaming
│   │       ├── stream_completion.py # Core streaming functionality
│   │       ├── stream_with_final.py # Stream with final result functionality
│   │       └── structured_completion.py # Core structured completion
│   ├── messages/            # Message handling
│   ├── image/               # Image generation and vision capabilities
│   │   ├── mixin.py         # Image generation mixin
│   │   ├── vision.py        # Vision API functionality
│   │   ├── response.py      # Process image responses
│   │   ├── utils.py         # Image utilities
│   │   └── validation.py    # Image parameter validation
│   └── responses/           # Response processing
├── enums/                   # Enumerations
│   ├── __init__.py          # Exports all enums
│   ├── ai_models.py         # AIModel enum with model capabilities
│   ├── ai_providers.py      # AIProvider enum for provider identification
│   └── model_features.py    # Collections of model-specific features
├── models/                  # Data models
│   ├── __init__.py
│   ├── chat_models.py       # Chat completion models
│   ├── image.py             # Image generation models
│   └── llm_response.py      # LLM response models
├── types/                   # Type definitions
│   ├── __init__.py
│   └── response_types.py    # Response type definitions
└── utils/                   # Utility functions
    ├── __init__.py
    ├── image.py             # Image handling utilities
    └── model_utils.py       # Model-specific utilities
```

## Usage Examples

### Basic Usage

```python
from discovita.service.openai import OpenAIService

# Initialize the client
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Simple text completion
response = client.create_chat_completion(
    prompt="Tell me a joke about programming.",
    model="gpt-4o"  # Or try newer models like "gpt-4.5-preview", "o1", "o1-mini", "o3-mini"
)

print(response)
```

### Managing Conversation History

```python
from discovita.service.openai import OpenAIService
from pydantic import BaseModel
from typing import List

# Define a simple Message model
class Message(BaseModel):
    role: str  # "user", "assistant", or custom roles like "coach"
    content: str

# Initialize the client
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create a conversation history
conversation = [
    Message(role="user", content="Tell me a joke"),
    Message(role="assistant", content="Why don't scientists trust atoms? Because they make up everything!"),
    Message(role="user", content="Tell me another one")
]

# Create messages array with conversation history and system prompt
messages = client.create_messages(
    system_message="You are a helpful AI assistant with a good sense of humor.",
    messages=conversation
)

# Get a response using the conversation history
response = client.create_chat_completion(
    messages=messages,
    model="gpt-4o"
)

# Add the response to the conversation history for future interactions
conversation.append(Message(role="assistant", content=response))

# For the next interaction, just update the conversation and create messages again
conversation.append(Message(role="user", content="Explain that joke"))
updated_messages = client.create_messages(
    system_message="You are a helpful AI assistant with a good sense of humor.",
    messages=conversation
)
```

### Working with Images (Vision)

```python
from discovita.service.openai import OpenAIService

client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Analyze an image using the vision capabilities
image_description = client.describe_image_with_vision(
    image_url="https://example.com/image.jpg",
    prompt="What's in this image? Describe all the details you can see."
)

print(image_description)

# Multimodal input with image in chat completion
response = client.create_chat_completion(
    prompt="What's in this image?",
    images=["path/to/your/image.jpg"],
    model="gpt-4o"
)

print(response)
```

### Image Description Service

```python
from discovita.service.openai import OpenAIService
from discovita.service.openai.core.image_description import ImageDescriptionService

# Initialize the OpenAI service
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create the image description service
description_service = ImageDescriptionService(client)

# Get a clean description of a headshot image
description = await description_service.get_clean_description("https://example.com/headshot.jpg")

print(description)
```

### Using JSON Mode

```python
from discovita.service.openai import OpenAIService

client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Get response in JSON format
response = client.create_chat_completion(
    prompt="Generate a list of 3 programming languages with their creator and year.",
    model="gpt-4o",
    json_mode=True
)

# response is a Python dictionary
for language in response["languages"]:
    print(f"{language['name']} - {language['creator']} ({language['year']})")
```

### Structured Outputs with Pydantic

```python
from pydantic import BaseModel
from typing import List
from discovita.service.openai import OpenAIService

# Define your response structure
class ProgrammingLanguage(BaseModel):
    name: str
    creator: str
    year: int

class LanguagesResponse(BaseModel):
    languages: List[ProgrammingLanguage]

# Initialize the client
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages for the conversation
messages = [
    {"role": "system", "content": "You are a programming historian."},
    {"role": "user", "content": "List 3 programming languages with their creator and year."}
]

# Get a structured response
response = client.create_structured_chat_completion(
    messages=messages,
    model="gpt-4.5-preview", 
    response_format=LanguagesResponse
)

# Work with the typed response
for language in response.parsed_model.languages:
    print(f"{language.name} - {language.creator} ({language.year})")
```

### Structured Outputs with Conversation History

```python
from pydantic import BaseModel, Field
from typing import List
from discovita.service.openai import OpenAIService

# Define your data models
class Message(BaseModel):
    role: str
    content: str

class UserProfile(BaseModel):
    name: str
    interests: List[str]
    skills: List[str]

# Initialize the client
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create a conversation history
conversation = [
    Message(role="user", content="Hi, I'm Alex. I love programming and hiking."),
    Message(role="assistant", content="Nice to meet you Alex! What kind of programming do you do?"),
    Message(role="user", content="I work with Python and JavaScript mainly. I'm also learning Rust.")
]

# Create formatted messages with conversation history
messages = client.create_messages(
    system_message="Extract information about the user from the conversation.",
    messages=conversation
)

# Get a structured response based on the conversation
response = client.create_structured_chat_completion(
    messages=messages,
    model="o1",  # O1 model supports structured outputs
    response_format=UserProfile
)

# Use the structured data
user_profile = response.choices[0].message.parsed
print(f"User: {user_profile.name}")
print(f"Interests: {', '.join(user_profile.interests)}")
print(f"Skills: {', '.join(user_profile.skills)}")
```

### Using Stream Mode

```python
from discovita.service.openai import OpenAIService

client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Stream the response
stream = client.create_chat_completion(
    prompt="Write a short story about AI.",
    model="gpt-4o",
    stream=True
)

# Process the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Streaming Structured Outputs

```python
from pydantic import BaseModel
from typing import List
from discovita.service.openai import OpenAIService

# Define the response format using Pydantic
class EntityExtraction(BaseModel):
    attributes: List[str]
    colors: List[str]
    animals: List[str]

# Initialize the client
client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Create messages
system_message = "Extract entities from the input text"
prompt = "The quick brown fox jumps over the lazy dog with piercing blue eyes"
messages = client.create_messages(prompt=prompt, system_message=system_message)

# Stream the structured completion
for parsed_data, is_final in client.stream_structured_completion(
    messages=messages,
    model="gpt-4o-mini",
    response_format=EntityExtraction,
    temperature=0.7,
):
    if is_final:
        print("\nFinal completion:")
        print(parsed_data)
    else:
        # Incremental updates
        print(parsed_data)
```

### Image Generation with DALL-E

```python
from discovita.service.openai import OpenAIService, ImageModel, ImageSize, ImageQuality, ImageStyle

client = OpenAIService(
    api_key="YOUR_API_KEY",
    organization="YOUR_ORG_ID"
)

# Generate an image with DALL-E 3
image_response = client.generate_image(
    prompt="A futuristic city with flying cars and tall glass buildings against a sunset sky",
    model=ImageModel.DALL_E_3,
    size=ImageSize.LANDSCAPE_1792x1024,
    quality=ImageQuality.HD,
    style=ImageStyle.VIVID
)

# Save the generated image to a file
saved_path = client.save_generated_image(
    image_response.data[0].url,
    output_path="./generated_images",
    filename="futuristic_city.png"
)

print(f"Image saved to: {saved_path}")
```

## Using AIModel for Model-Specific Logic

```python
from discovita.service.openai import AIModel

# Check if a model supports structured outputs
supports_structured = AIModel.supports_structured_outputs("gpt-4.5-preview")
print(f"Does gpt-4.5-preview support structured outputs? {supports_structured}")

# Get the appropriate token parameter name for a model
token_param = AIModel.get_token_param_name("o3-mini")
print(f"Token parameter for o3-mini: {token_param}")  # Returns "max_completion_tokens"

# Get the provider for a model
provider = AIModel.get_provider("o1")
print(f"Provider for o1: {provider}")  # Returns AIProvider.OPENAI
```

## Compatibility

This module was developed and tested with OpenAI Python SDK version 1.68.2. If you encounter issues with other versions, you can silence the compatibility warning by setting the environment variable:

```
MUTE_OPENAI_HELPER_WARNING=True
```

## Development

To contribute to this module, please follow the modular structure. Each file should have:

1. Comprehensive docstrings
2. Type annotations
3. Proper error handling
4. Logging for important operations

When adding new functionality, consider which module it belongs in:
- `core`: For main functionality that users will interact with directly
- `utils`: For client functions and utilities
- `types`: For type definitions and parsing logic
- `enums`: For enumeration types and constants