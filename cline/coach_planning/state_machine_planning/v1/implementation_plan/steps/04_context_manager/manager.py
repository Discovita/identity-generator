from typing import Dict, Any, List, Optional, Set
from discovita.service.coach.models import CoachContext, ChatMessage, UserProfile, CoachingState
from discovita.service.openai.client.client import OpenAIClient

class ContextManager:
    """Manages conversation context for the coaching system."""
    
    def __init__(
        self, 
        llm_client: OpenAIClient,
        max_recent_messages: int = 10
    ):
        """Initialize the context manager."""
        self.llm_client = llm_client
        self.max_recent_messages = max_recent_messages
    
    async def load_context(self, user_id: str) -> CoachContext:
        """Load or create context for a user."""
        # Try to load existing context from persistence
        context = await self._load_from_persistence(user_id)
        
        # If no existing context, create a new one
        if not context:
            context = CoachContext(
                user_id=user_id,
                current_state=CoachingState.INTRODUCTION,
                conversation_history=[],
                consolidated_summary="",
                user_profile=None,
                metadata={}
            )
        
        return context
    
    async def add_message(
        self, 
        context: CoachContext, 
        role: str, 
        content: str
    ) -> CoachContext:
        """Add a message to the conversation history."""
        # Create a new message
        message = ChatMessage(role=role, content=content)
        
        # Add to conversation history
        context.conversation_history.append(message)
        
        # If we exceed the max messages, consolidate
        if len(context.conversation_history) > self.max_recent_messages:
            context = await self._consolidate_context(context)
        
        # Save the updated context
        await self._save_to_persistence(context)
        
        return context
    
    async def update_user_profile(
        self, 
        context: CoachContext, 
        profile: UserProfile
    ) -> CoachContext:
        """Update the user profile in the context."""
        context.user_profile = profile
        
        # Save the updated context
        await self._save_to_persistence(context)
        
        return context
    
    async def update_metadata(
        self, 
        context: CoachContext, 
        key: str, 
        value: Any
    ) -> CoachContext:
        """Update a metadata value in the context."""
        context.metadata[key] = value
        
        # Save the updated context
        await self._save_to_persistence(context)
        
        return context
    
    async def _consolidate_context(self, context: CoachContext) -> CoachContext:
        """Consolidate older messages into a summary."""
        # Get messages to consolidate (keeping the most recent ones)
        messages_to_keep = context.conversation_history[-self.max_recent_messages//2:]
        messages_to_consolidate = context.conversation_history[:-self.max_recent_messages//2]
        
        # If there are no messages to consolidate, return unchanged
        if not messages_to_consolidate:
            return context
        
        # Format messages for the consolidation prompt
        messages_text = "\n\n".join([
            f"{msg.role.capitalize()}: {msg.content}" 
            for msg in messages_to_consolidate
        ])
        
        # Create the consolidation prompt
        consolidation_prompt = f"""
        Summarize the key information from this conversation:
        
        {messages_text}
        
        Previous summary: {context.consolidated_summary}
        
        Extract and update any important information about the user, their goals, challenges, and progress.
        Focus on information that would be relevant for continuing the coaching conversation.
        """
        
        # Get summary from LLM
        summary_response = await self.llm_client.get_completion(
            messages=[{"role": "user", "content": consolidation_prompt}]
        )
        summary = summary_response.choices[0].message.content
        
        # Update the context
        if context.consolidated_summary:
            context.consolidated_summary = f"{context.consolidated_summary}\n\nUpdated information: {summary}"
        else:
            context.consolidated_summary = summary
        
        # Update the conversation history to only keep recent messages
        context.conversation_history = messages_to_keep
        
        return context
    
    async def _load_from_persistence(self, user_id: str) -> Optional[CoachContext]:
        """Load context from persistence."""
        # This will be implemented in the persistence layer
        # For now, return None to indicate no existing context
        return None
    
    async def _save_to_persistence(self, context: CoachContext) -> None:
        """Save context to persistence."""
        # This will be implemented in the persistence layer
        pass
