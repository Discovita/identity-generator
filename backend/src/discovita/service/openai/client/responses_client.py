"""OpenAI Responses API client methods.

This module contains methods for the OpenAI Responses API that will be mixed into
the OpenAIClient class. These methods provide a high-level interface for interacting
with the Responses API, including function calling and structured outputs.
"""

from typing import Union, List, Dict, Any, TypeVar, Type, Optional, Callable, Awaitable
from openai.types.responses import Response, FunctionTool
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from discovita.service.openai.models.llm_response import LLMResponseModel
from discovita.service.openai.models import (
    ResponsesMessage,
)
from discovita.service.openai.client.operations.responses import (
    create_response,
    call_function,
    handle_function_call_response,
    submit_function_results,
    get_structured_response,
    StructuredResponseResult
)

T = TypeVar('T', bound=LLMResponseModel)

# These methods will be mixed into the OpenAIClient class
async def create_response_with_responses(
    self,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    model: str = "gpt-4o",
    tools: List[Dict[str, Any]] = None,
    tool_choice: Union[str, Dict[str, Any]] = None,
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Create a response using the OpenAI Responses API.
    
    This method sends a request to the OpenAI Responses API and returns
    the response. It handles both text and message list inputs.
    
    Args:
        input_data: Input data, which can be a string or a list of messages
        model: The model to use (default: "gpt-4o")
        tools: Optional tools (including functions) available to the model
        tool_choice: Optional parameter to control which tool the model uses
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The response from the OpenAI Responses API
    """
    return await create_response(
        client=self.client,
        input_data=input_data,
        model=model,
        tools=tools,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )

async def call_function_with_responses(
    self,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    functions: List[Union[Dict[str, Any], FunctionTool]],
    model: str = "gpt-4o",
    tool_choice: Union[str, Dict[str, Any]] = "auto",
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Call a function using the OpenAI Responses API.
    
    This method sends a request to the OpenAI Responses API with function
    definitions and returns the response, which may include function calls.
    
    Args:
        input_data: Input data, which can be a string or a list of messages
        functions: List of function definitions
        model: The model to use (default: "gpt-4o")
        tool_choice: Control which tool the model uses (default: "auto")
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The response from the OpenAI Responses API
    """
    return await call_function(
        client=self.client,
        input_data=input_data,
        functions=functions,
        model=model,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )

async def call_functions_with_responses(
    self,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    functions: List[Union[Dict[str, Any], FunctionTool]],
    function_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[Any]]],
    model: str = "gpt-4o",
    tool_choice: Union[str, Dict[str, Any]] = "auto",
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Call functions with the model and handle the responses automatically.
    
    This method combines call_function, handle_function_call_response, and
    submit_function_results into a single method that handles the entire
    function calling flow.
    
    Args:
        input_data: Input data, which can be a string or a list of messages
        functions: List of function definitions
        function_handlers: Dictionary mapping function names to handler functions
        model: The model to use (default: "gpt-4o")
        tool_choice: Control which tool the model uses (default: "auto")
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The final response from the OpenAI Responses API
    """
    # Call the functions
    response = await self.call_function_with_responses(
        input_data=input_data,
        functions=functions,
        model=model,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )
    
    # Check if there are function calls in the response
    has_function_calls = any(isinstance(output_item, ResponseFunctionToolCall) for output_item in response.output)
    if not has_function_calls:
        return response
    
    # Handle the function calls
    outputs = await handle_function_call_response(
        response=response,
        function_handlers=function_handlers
    )
    
    # Submit the function results
    return await self.submit_function_results_with_responses(
        input_data=input_data,
        function_outputs=outputs,
        tools=[func.model_dump() if isinstance(func, FunctionTool) else func for func in functions],
        model=model,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=response.id
    )

async def submit_function_results_with_responses(
    self,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    function_outputs: Union[Dict[str, Any], List[Dict[str, Any]]],
    tools: List[Dict[str, Any]] = None,
    model: str = "gpt-4o",
    tool_choice: Union[str, Dict[str, Any]] = None,
    store: bool = True,
    previous_response_id: str = None
) -> Response:
    """Submit function results to the OpenAI Responses API.
    
    This method sends function results back to the OpenAI Responses API
    and returns the final response.
    
    Args:
        input_data: Input data, which can be a string or a list of messages
        function_outputs: Function outputs to submit as dictionaries with 'tool_call_id' and 'output' keys
        tools: Optional tools (including functions) available to the model
        model: The model to use (default: "gpt-4o")
        tool_choice: Optional parameter to control which tool the model uses
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        Response: The response from the OpenAI Responses API
    """
    return await submit_function_results(
        client=self.client,
        input_data=input_data,
        function_outputs=function_outputs,
        tools=tools,
        model=model,
        tool_choice=tool_choice,
        store=store,
        previous_response_id=previous_response_id
    )

async def get_structured_response_with_responses(
    self,
    input_data: Union[str, List[Dict[str, Any]], List[ResponsesMessage]],
    response_model: Type[T],
    model: str = "gpt-4o",
    schema_name: Optional[str] = None,
    store: bool = True,
    previous_response_id: str = None
) -> StructuredResponseResult[T]:
    """Get a structured response using the OpenAI Responses API.
    
    This method sends a request to the OpenAI Responses API with a JSON schema
    derived from a Pydantic model and returns the response, which should adhere
    to the schema. The response is automatically validated against the model.
    
    Args:
        input_data: Input data, which can be a string or a list of messages
        response_model: Pydantic model class for response validation (must extend LLMResponseModel)
        model: The model to use (default: "gpt-4o")
        schema_name: Optional name for the schema (default: model class name)
        store: Whether to store the response for future reference
        previous_response_id: ID of the previous response in a conversation
        
    Returns:
        StructuredResponseResult: The result of the structured response operation,
            including the raw response, parsed data, validation status, and error message
    """
    return await get_structured_response(
        client=self.client,
        input_data=input_data,
        response_model=response_model,
        model=model,
        schema_name=schema_name,
        store=store,
        previous_response_id=previous_response_id
    ) 