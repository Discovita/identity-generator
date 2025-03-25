import json
import re
from typing import List, Dict, Any, Optional

from .models.action import Action

class ActionParser:
    """Parses actions from LLM responses."""
    
    def __init__(self):
        # Default action pattern looks for [ACTION:NAME]{...json...}[/ACTION]
        self.action_pattern = r'\[ACTION:([A-Z_]+)\](.*?)\[/ACTION\]'
    
    def parse_actions(self, response: str) -> List[Action]:
        """Parse actions from an LLM response string."""
        matches = re.findall(self.action_pattern, response, re.DOTALL)
        
        parsed_actions = []
        for action_name, action_params in matches:
            try:
                params = self._parse_params(action_params)
                parsed_actions.append(Action(
                    name=action_name,
                    params=params
                ))
            except Exception as e:
                # Log error but continue with other actions
                print(f"Error parsing action {action_name}: {str(e)}")
        
        return parsed_actions
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """Parse parameters from a JSON string."""
        try:
            return json.loads(params_str)
        except json.JSONDecodeError:
            # Try to clean up the string and parse again
            cleaned_str = self._clean_params_string(params_str)
            return json.loads(cleaned_str)
    
    def _clean_params_string(self, params_str: str) -> str:
        """Clean up a parameters string to make it valid JSON."""
        # Remove any leading/trailing whitespace
        cleaned = params_str.strip()
        
        # Replace single quotes with double quotes
        cleaned = re.sub(r"'([^']*)'", r'"\1"', cleaned)
        
        # Ensure property names are quoted
        cleaned = re.sub(r'(\s*)(\w+)(\s*):(\s*)', r'\1"\2"\3:\4', cleaned)
        
        return cleaned

class XMLActionParser(ActionParser):
    """Parses actions from LLM responses in XML format."""
    
    def __init__(self):
        super().__init__()
        # XML pattern looks for <action name="NAME">...json...</action>
        self.action_pattern = r'<action\s+name="([A-Z_]+)">(.*?)</action>'
    
    def _parse_params(self, params_str: str) -> Dict[str, Any]:
        """Parse parameters from XML content."""
        # Extract parameters from XML elements
        param_pattern = r'<param\s+name="(\w+)">(.*?)</param>'
        matches = re.findall(param_pattern, params_str, re.DOTALL)
        
        params = {}
        for name, value in matches:
            # Try to parse as JSON if possible
            try:
                params[name] = json.loads(value)
            except json.JSONDecodeError:
                # Otherwise use as string
                params[name] = value
        
        return params

# Factory function to create the appropriate parser
def create_parser(format: str = "default") -> ActionParser:
    """Create an action parser for the specified format."""
    if format.lower() == "xml":
        return XMLActionParser()
    else:
        return ActionParser()
