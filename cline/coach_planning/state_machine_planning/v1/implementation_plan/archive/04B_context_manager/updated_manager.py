from typing import Dict, Any, List, Optional, Set
from uuid import uuid4

from discovita.service.coach.models import CoachContext, ChatMessage, UserProfile, CoachingState
from discovita.service.coach.persistence import DatabaseInterface
from discovita.service.coach.persistence.models import ContextRecord
from discovita.service.openai.client.client import OpenAIClient

class ContextManager:
    """Manages conversation context for the coaching system."""
    
    def __init__(
        self, 
        llm_client: OpenAIClient,
        db: DatabaseInterface,
        max_recent_messages: int = 10
    ):
        """
        Initialize the context manager.
        
        Args:
            llm_client: OpenAI client for LLM operations
            db: Database interface from the persistence layer
            max_recent_messages: Maximum number of recent messages to keep in full
        """
        self.llm_client = llm_client
        self.db = db
        self.max_recent_messages = max_recent_messages
    
    async def load_context(self, user_id: str, session_id: str) -> CoachContext:
        """
        Load or create context for a user session.
        
        Args:
            user_id: The user ID
            session_id: The session ID
            
        Returns:
            The coach context for the user session
        """
        # Try to load existing context from persistence layer
        context_record = await self.db.get_context(user_id, session_id)
        
        # If no existing context, create a new one
        if not context_record:
            return self._create_new_context(user_id, session_id)
        
        # Convert from persistence model to domain model
        return self._convert_to_coach_context(context_record)
    
    def _create_new_context(self, user_id: str, session_id: str) -> CoachContext:
        """
        Create a new context for a user session.
        
        Args:
            user_id: The user ID
            session_id: The session ID
            
        Returns:
            A new coach context
        """
        return CoachContext(
            user_id=user_id,
            session_id=session_id,
            current_state=CoachingState.INTRODUCTION,
            conversation_history=[],
            consolidated_summary="",
            user_profile=None,
            metadata={}
        )
    
    async def add_message(
        self, 
        context: CoachContext, 
        role: str, 
        content: str
    ) -> CoachContext:
        """
        Add a message to the conversation history.
        
        Args:
            context: The coach context
            role: The message role (user or assistant)
            content: The message content
            
        Returns:
            The updated coach context
        """
        # Create a new message
        message = ChatMessage(role=role, content=content)
        
        # Add to conversation history
        context.conversation_history.append(message)
        
        # If we exceed the max messages, consolidate
        if len(context.conversation_history) > self.max_recent_messages:
            context = await self._consolidate_context(context)
        
        # Save the updated context
        await self.save_context(context)
        
        return context
    
    async def update_user_profile(
        self, 
        context: CoachContext, 
        profile: UserProfile
    ) -> CoachContext:
        """
        Update the user profile in the context.
        
        Args:
            context: The coach context
            profile: The user profile
            
        Returns:
            The updated coach context
        """
        context.user_profile = profile
        
        # Save the updated context
        await self.save_context(context)
        
        return context
    
    async def update_metadata(
        self, 
        context: CoachContext, 
        key: str, 
        value: Any
    ) -> CoachContext:
        """
        Update a metadata value in the context.
        
        Args:
            context: The coach context
            key: The metadata key
            value: The metadata value
            
        Returns:
            The updated coach context
        """
        context.metadata[key] = value
        
        # Save the updated context
        await self.save_context(context)
        
        return context
    
    async def save_context(self, context: CoachContext) -> None:
        """
        Save context to the persistence layer.
        
        Args:
            context: The coach context to save
        """
        # Convert from domain model to persistence model
        context_record = self._convert_to_context_record(context)
        
        # Save to persistence layer
        await self.db.save_context(context_record)
    
    async def _consolidate_context(self, context: CoachContext) -> CoachContext:
        """
        Consolidate older messages into a summary.
        
        Args:
            context: The coach context
            
        Returns:
            The updated coach context with consolidated messages
        """
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
    
    def _convert_to_coach_context(self, context_record: ContextRecord) -> CoachContext:
        """
        Convert a context record to a coach context.
        
        Args:
            context_record: The context record from the persistence layer
            
        Returns:
            The coach context
        """
        # Extract data from the context record
        data = context_record.data
        
        # Create a coach context from the data
        return CoachContext(
            user_id=context_record.user_id,
            session_id=context_record.session_id,
            current_state=data.get("current_state", CoachingState.INTRODUCTION),
            conversation_history=data.get("conversation_history", []),
            consolidated_summary=data.get("consolidated_summary", ""),
            user_profile=data.get("user_profile"),
            metadata=data.get("metadata", {})
        )
    
    def _convert_to_context_record(self, context: CoachContext) -> ContextRecord:
        """
        Convert a coach context to a context record.
        
        Args:
            context: The coach context
            
        Returns:
            The context record for the persistence layer
        """
        # Create a context record from the coach context
        return ContextRecord(
            user_id=context.user_id,
            session_id=context.session_id,
            data={
                "current_state": context.current_state,
                "conversation_history": context.conversation_history,
                "consolidated_summary": context.consolidated_summary,
                "user_profile": context.user_profile,
                "metadata": context.metadata
            }
        )
