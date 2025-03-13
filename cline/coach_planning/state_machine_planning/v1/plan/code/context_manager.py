from typing import Dict, Any, List, Optional
import json

class ContextManager:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.recent_messages: List[Dict[str, Any]] = []
        self.user_data: Dict[str, Any] = {}
        self.consolidated_summary: str = ""
    
    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation history."""
        self.recent_messages.append({"role": role, "content": content})
        if len(self.recent_messages) > self.max_messages:
            # When we exceed max messages, consolidate the older ones
            self._consolidate_context()
    
    def update_user_data(self, key: str, value: Any) -> None:
        """Update or add a piece of user data."""
        self.user_data[key] = value
    
    def get_context_for_prompt(self) -> Dict[str, Any]:
        """Prepare the context dictionary for prompt formatting."""
        return {
            "user_summary": self.consolidated_summary,
            "recent_messages": self._format_recent_messages(),
            "draft_identities": self.user_data.get("identities", []),
            # Add other context fields as needed
        }
    
    def _format_recent_messages(self) -> str:
        """Format recent messages for inclusion in prompts."""
        formatted = ""
        for msg in self.recent_messages:
            role_display = "User" if msg["role"] == "user" else "Coach"
            formatted += f"{role_display}: {msg['content']}\n\n"
        return formatted
    
    def _consolidate_context(self) -> None:
        """Consolidate older messages into a summary."""
        messages_to_consolidate = self.recent_messages[:-self.max_messages//2]
        self.recent_messages = self.recent_messages[-self.max_messages//2:]
        
        # Use LLM to create a summary
        consolidation_prompt = f"""
        Summarize the key information from this conversation:
        
        {self._format_recent_messages()}
        
        Previous summary: {self.consolidated_summary}
        
        Extract and update any important information about the user, their goals, challenges, and progress.
        """
        
        # This would call your LLM service
        summary = llm_service.get_response(consolidation_prompt)
        
        # Update the consolidated summary
        if self.consolidated_summary:
            self.consolidated_summary = f"{self.consolidated_summary}\n\nUpdated information: {summary}"
        else:
            self.consolidated_summary = summary
            