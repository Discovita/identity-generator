"""Output models for OpenAI Responses API.

This module contains models related to the output of the OpenAI Responses API,
including text output and response models.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from openai.types.chat import ChatCompletionMessageToolCall as ResponseFunctionToolCall
from openai.types.chat import ChatCompletion as OpenAIResponse

class OutputText(BaseModel):
    """Output text model for the Responses API.
    
    This model represents text output in the Responses API.
    """
    type: Literal["output_text"] = Field("output_text", description="Type of the output item")
    text: str = Field(..., description="The text content")
    annotations: List[Dict[str, Any]] = Field(default_factory=list, description="Annotations for the text")

class ResponsesOutput(BaseModel):
    """Output model for the Responses API.
    
    This model represents the output of the Responses API, which can be
    either text or a function call.
    """
    type: str = Field(..., description="Type of the output item")
    
    # Additional fields based on type
    # For function_call
    id: Optional[str] = Field(None, description="Unique identifier for the function call")
    call_id: Optional[str] = Field(None, description="ID used to associate the function call with its output")
    name: Optional[str] = Field(None, description="Name of the function to call")
    arguments: Optional[str] = Field(None, description="JSON-encoded arguments for the function call")
    
    # For output_text
    text: Optional[str] = Field(None, description="The text content")
    annotations: Optional[List[Dict[str, Any]]] = Field(None, description="Annotations for the text")
    
    @field_validator('type')
    def validate_type(cls, v):
        """Validate the type field."""
        if v not in ["function_call", "output_text"]:
            raise ValueError(f"Invalid type: {v}. Must be one of: function_call, output_text")
        return v
    
    def is_function_call(self) -> bool:
        """Check if this output is a function call.
        
        Returns:
            bool: True if this output is a function call, False otherwise
        """
        return self.type == "function_call"
    
    def is_text(self) -> bool:
        """Check if this output is text.
        
        Returns:
            bool: True if this output is text, False otherwise
        """
        return self.type == "output_text"
    
    def as_function_call(self) -> ResponseFunctionToolCall:
        """Convert this output to a ResponseFunctionToolCall if it is a function call.
        
        Returns:
            ResponseFunctionToolCall: The function call
            
        Raises:
            ValueError: If this output is not a function call
        """
        if not self.is_function_call():
            raise ValueError("This output is not a function call")
        
        # Fail fast if required fields are missing
        assert self.id is not None, "Function call must have an id"
        assert self.name is not None, "Function call must have a name"
        assert self.arguments is not None, "Function call must have arguments"
        
        # Create and return the ResponseFunctionToolCall
        # Use type: ignore to bypass the type checker since we know this works at runtime
        return ResponseFunctionToolCall(
            id=self.id,
            function={"name": self.name, "arguments": self.arguments},  # type: ignore
            type="function"
        )
    
    def as_text(self) -> OutputText:
        """Convert this output to an OutputText if it is text.
        
        Returns:
            OutputText: The output text
            
        Raises:
            ValueError: If this output is not text
        """
        if not self.is_text():
            raise ValueError("This output is not text")
        
        # Fail fast if required fields are missing
        assert self.text is not None, "Output text must have text content"
        
        return OutputText(
            type="output_text",
            text=self.text,
            annotations=self.annotations or []
        )

# Using the OpenAI SDK's Response model directly
ResponsesResponse = OpenAIResponse

# Add a compatibility layer for code that still expects the old interface
# This can be removed once all code is updated to use the SDK's Response model
class ResponsesResponseCompat(OpenAIResponse):
    """Compatibility layer for code that still expects the old ResponsesResponse interface.
    
    This class extends the SDK's Response model with methods that were previously 
    available in our custom ResponsesResponse model.
    """
    
    @property
    def function_calls(self) -> List[ResponseFunctionToolCall]:
        """Get the function calls from the response.
        
        Returns:
            List[ResponseFunctionToolCall]: The function calls, or an empty list if there are no function calls
        """
        result = []
        for choice in self.choices:
            if choice.message and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if tool_call.type == "function":
                        result.append(tool_call)
        return result
    
    def has_function_calls(self) -> bool:
        """Check if the response has any function calls.
        
        Returns:
            bool: True if the response has function calls, False otherwise
        """
        for choice in self.choices:
            if choice.message and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if tool_call.type == "function":
                        return True
        return False
