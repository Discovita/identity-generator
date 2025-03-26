"""Inspect OpenAI package structure."""

import inspect
import sys
import json
from openai import AsyncOpenAI

# Print OpenAI version
import openai
print(f"OpenAI version: {openai.__version__}")

# Create client
client = AsyncOpenAI(api_key="dummy")

# Check ChatCompletionToolParam structure
print("\n=== ChatCompletionToolParam structure ===")
try:
    from openai.types.chat import ChatCompletionToolParam
    print(f"Available attributes: {[attr for attr in dir(ChatCompletionToolParam) if not attr.startswith('_')]}")
    
    # Create an instance to inspect
    tool_param = ChatCompletionToolParam(type="function", function={"name": "test", "description": "test"})
    print(f"\nInstance attributes: {dir(tool_param)}")
    print(f"\nInstance type: {type(tool_param)}")
    print(f"\nInstance content: {dict(tool_param)}")
except ImportError:
    print("ChatCompletionToolParam not found")
except Exception as e:
    print(f"Error with ChatCompletionToolParam: {e}")

# Check ChatCompletionMessageToolCall structure
print("\n=== ChatCompletionMessageToolCall structure ===")
try:
    from openai.types.chat import ChatCompletionMessageToolCall
    print(f"Available attributes: {[attr for attr in dir(ChatCompletionMessageToolCall) if not attr.startswith('_')]}")
    
    # Create an instance to inspect
    tool_call = ChatCompletionMessageToolCall(
        id="call_123",
        type="function",
        function={"name": "test", "arguments": "{}"}
    )
    print(f"\nInstance type: {type(tool_call)}")
    
    # Check if it's a Pydantic model
    if hasattr(tool_call, 'model_dump'):
        print(f"\nModel dump: {tool_call.model_dump()}")
    else:
        print(f"\nInstance content: {dict(tool_call)}")
        
    # Check for specific attributes
    print("\nChecking for specific attributes:")
    for attr in ['id', 'type', 'function', 'name', 'arguments', 'call_id']:
        print(f"Has '{attr}': {hasattr(tool_call, attr)}")
except ImportError:
    print("ChatCompletionMessageToolCall not found")
except Exception as e:
    print(f"Error with ChatCompletionMessageToolCall: {e}")

# Check ChatCompletion structure
print("\n=== ChatCompletion structure ===")
try:
    from openai.types.chat import ChatCompletion, ChatCompletionMessage
    sample = ChatCompletion(
        id="123",
        choices=[{
            "index": 0,
            "message": ChatCompletionMessage(
                role="assistant",
                content="Hello"
            ),
            "finish_reason": "stop"
        }],
        created=123,
        model="gpt-4",
        object="chat.completion",
        system_fingerprint="abc"
    )
    
    print(f"Instance type: {type(sample)}")
    
    # Check if it's a Pydantic model
    if hasattr(sample, 'model_dump'):
        print(f"\nModel dump: {json.dumps(sample.model_dump(), indent=2)}")
    else:
        print(f"\nInstance content: {dict(sample)}")
        
    # Check for specific attributes
    print("\nChecking for specific attributes:")
    for attr in ['id', 'choices', 'created', 'model', 'object', 'output']:
        print(f"Has '{attr}': {hasattr(sample, attr)}")
except Exception as e:
    print(f"Error with ChatCompletion: {e}")
