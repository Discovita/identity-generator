from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import asyncio

class UserMessage(BaseModel):
    user_id: str
    message: str

class CoachResponse(BaseModel):
    message: str
    current_state: str

class CoachAPI:
    def __init__(self, llm_service, db_service):
        self.app = FastAPI()
        self.llm_service = llm_service
        self.db_service = db_service
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        """Set up API routes."""
        @self.app.post("/coach/message", response_model=CoachResponse)
        async def process_message(user_message: UserMessage):
            return await self.handle_message(user_message)
    
    async def handle_message(self, user_message: UserMessage) -> Dict[str, Any]:
        """Process a user message and generate a coach response."""
        user_id = user_message.user_id
        message = user_message.message
        
        # Get or create user session
        session = self._get_or_create_session(user_id)
        
        # Add user message to context
        session["context_manager"].add_message("user", message)
        
        # Get the current state
        state = session["state_machine"].current_state
        
        # Get appropriate prompt for this state
        context = session["context_manager"].get_context_for_prompt()
        prompt = session["prompt_manager"].get_prompt(state, context)
        
        if not prompt:
            raise HTTPException(status_code=500, detail="Failed to generate prompt")
        
        # Get allowed actions for this state
        allowed_actions = session["prompt_manager"].get_allowed_actions(state)
        
        # Add action instructions to prompt
        action_instructions = self._create_action_instructions(allowed_actions)
        full_prompt = f"{prompt}\n\n{action_instructions}"
        
        # Get response from LLM
        response = await self.llm_service.get_response_async(full_prompt)
        
        # Extract display message and actions
        display_message, actions = self._process_llm_response(response)
        
        # Add coach message to context
        session["context_manager"].add_message("coach", display_message)
        
        # Execute actions
        session["action_executor"].execute_actions(actions)
        
        # Check if state transition occurred
        new_state = session["state_machine"].current_state
        
        return {
            "message": display_message,
            "current_state": new_state.name
        }
    
    def _get_or_create_session(self, user_id: str) -> Dict[str, Any]:
        """Get existing session or create a new one for the user."""
        if user_id not in self.user_sessions:
            # Load user data from database
            user_data = self.db_service.get_user_data(user_id)
            
            # Initialize components
            state_machine = CoachStateMachine()
            prompt_manager = PromptManager()
            context_manager = ContextManager()
            
            # If we have existing user data, restore their state
            if user_data:
                if "current_state" in user_data:
                    state_machine.current_state = CoachingState[user_data["current_state"]]
                
                if "user_data" in user_data:
                    for key, value in user_data["user_data"].items():
                        context_manager.update_user_data(key, value)
                
                if "consolidated_summary" in user_data:
                    context_manager.consolidated_summary = user_data["consolidated_summary"]
            
            # Create action executor
            action_executor = ActionExecutor(context_manager, state_machine, self.db_service)
            
            # Store session
            self.user_sessions[user_id] = {
                "state_machine": state_machine,
                "prompt_manager": prompt_manager,
                "context_manager": context_manager,
                "action_executor": action_executor
            }
        
        return self.user_sessions[user_id]
    
    def _create_action_instructions(self, allowed_actions: list[str]) -> str:
        """Create instructions for the LLM about available actions."""
        instructions = """
        INSTRUCTIONS FOR ACTIONS:
        You can perform the following actions by using the format:
        [ACTION:ACTION_NAME]{"param1": "value1", "param2": "value2"}[/ACTION]
        
        Available actions:
        """
        
        for action in allowed_actions:
            instructions += f"- {action}\n"
            
        return instructions
    
    def _process_llm_response(self, response: str) -> tuple[str, list[dict]]:
        """Process the LLM response to extract display message and actions."""
        # Separate actions from display message
        display_message = response
        
        # Parse actions using the action executor's method
        # Assuming we have access to an action executor instance
        actions = []
        for session in self.user_sessions.values():
            action_executor = session["action_executor"]
            actions = action_executor.parse_actions_from_response(response)
            break
            
        # Remove action blocks from display message
        action_pattern = r'\[ACTION:([A-Z_]+)\](.*?)\[/ACTION\]'
        display_message = re.sub(action_pattern, '', display_message, flags=re.DOTALL)
        
        # Clean up extra whitespace
        display_message = re.sub(r'\n{3,}', '\n\n', display_message).strip()
        
        return display_message, actions
        