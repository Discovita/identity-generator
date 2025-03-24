"""
Function Calling Example with OpenAI Responses API

This example demonstrates how to use the OpenAI Responses API for function calling.
It shows how to define functions, handle function calls, and process the results.

The example implements a simple calculator that can perform basic arithmetic
operations (add, subtract, multiply, divide) and a weather service that returns
weather information for a given location.
"""

import asyncio
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from discovita.service.openai.client import OpenAIClient
from openai.types.responses import FunctionTool
from openai.types.responses.response_output_text import ResponseOutputText
from openai.types.responses import ResponseOutputMessage
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
current_file = Path(__file__)
project_root = current_file.parents[3]
env_path = project_root / ".env"

# Load environment variables
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    logger.info(f"[ENV] Loaded environment from {env_path}")
else:
    logger.warning(f"[ENV] Warning: .env file not found at {env_path}")

# This is the API key from your .env file
API_KEY = os.getenv("OPENAI_API_KEY")

if API_KEY:
    masked_key = f"{API_KEY[:5]}...{API_KEY[-4:]}"
    logger.info(f"[AUTH] Using API key: {masked_key}")
else:
    logger.error("[AUTH] Error: OPENAI_API_KEY environment variable not found")
    exit(1)  # Exit if no API key is found

# Define calculator function
calculator_function = FunctionTool(
    type="function",
    name="calculator",
    description="Perform basic arithmetic operations",
    parameters={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The operation to perform (add, subtract, multiply, divide)",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {
                "type": "number",
                "description": "The first number"
            },
            "b": {
                "type": "number",
                "description": "The second number"
            }
        },
        "required": ["operation", "a", "b"],
        "additionalProperties": False
    },
    strict=True
)

# Define weather function
weather_function = FunctionTool(
    type="function",
    name="get_weather",
    description="Get the current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and country, e.g., 'Paris, France'"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    },
    strict=True
)

# Function handlers
async def calculator(args: Dict[str, Any]) -> str:
    """Handle calculator function calls."""
    logger.info(f"*****************[FUNCTION] calculator: {args}")
    operation = args["operation"]
    a = args["a"]
    b = args["b"]
    
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Error: Unknown operation '{operation}'"
    
    return f"Result of {a} {operation} {b} = {result}"

async def get_weather(args: Dict[str, Any]) -> str:
    """Handle weather function calls.
    
    In a real implementation, this would call a weather API.
    For this example, we'll return mock data.
    """
    logger.info(f"*****************[FUNCTION] get_weather")
    location = args["location"]
    
    # Mock weather data
    weather_data = {
        "Paris, France": {"temperature": 22, "condition": "Sunny"},
        "London, UK": {"temperature": 18, "condition": "Cloudy"},
        "New York, USA": {"temperature": 25, "condition": "Partly Cloudy"},
        "Tokyo, Japan": {"temperature": 28, "condition": "Rainy"}
    }
    
    if location in weather_data:
        data = weather_data[location]
        return f"The weather in {location} is {data['condition']} with a temperature of {data['temperature']}°C"
    else:
        return f"Weather data for {location} is not available. Available locations: {', '.join(weather_data.keys())}"

# Function handlers mapping
function_handlers = {
    "calculator": calculator,
    "get_weather": get_weather
}

def print_header(text: str, char: str = "="):
    """Print a formatted header."""
    logger.info("")
    logger.info(text)
    logger.info(char * len(text))

def format_args(args: Dict[str, Any]) -> str:
    """Format function arguments for display."""
    return "\n".join([f"  - {key}: {value}" for key, value in args.items()])

async def main():
    """Run the function calling example."""
    print_header("OpenAI Function Calling Example")
    logger.info("This example demonstrates how to use the OpenAI Responses API")
    logger.info("to call functions based on natural language queries.")
    
    # Initialize the client
    client = OpenAIClient(api_key=API_KEY)
    
    examples = [
        # "What is 25 plus 17?",
        # "What's the weather like in Paris today?",
        # "If I have 120 divided by 4, what do I get?",
        # "What's the weather in Tokyo and New York?",
        "Calculate 15 * 7"
    ]
    
    # Run each example
    for i, query in enumerate(examples):
        print_header(f"Example {i+1}: '{query}'", "-")
        
        try:
            # Call functions with automatic handling
            response = await client.call_functions_with_responses( 
                input_data=query,
                functions=[calculator_function, weather_function],
                function_handlers=function_handlers,
                model="gpt-4o"
            )
            
            # First, log any function calls that were made
            for output_item in response.output:
                if hasattr(output_item, 'name') and hasattr(output_item, 'arguments'):
                    args = json.loads(output_item.arguments)
                    logger.info(f"[FUNCTION CALL] {output_item.name}")
                    logger.info(f"Arguments:")
                    logger.info(format_args(args))
            
            # Then extract the final text response
            text_output = ""
            for output_item in response.output:
                if isinstance(output_item, ResponseOutputMessage):
                    for content in output_item.content:
                        if hasattr(content, 'text'):
                            text_output = content.text
                            break
            
            # Print the response
            logger.info(f"[AI RESPONSE] {text_output}")
            logger.info("")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())