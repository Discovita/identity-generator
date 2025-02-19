"""Coaching service implementation."""

from typing import List
from .models import ChatMessage, CoachResponse
from ..openai.client.client import OpenAIClient

SYSTEM_PROMPT = """You are a professional life coach. Your role is to help users achieve their personal and professional goals through supportive dialogue, insightful questions, and actionable guidance. Focus on being empathetic while maintaining professional boundaries. Guide users to discover their own solutions rather than giving direct advice."""

class CoachService:
    """Service for handling coaching interactions."""
    
    def __init__(self, client: OpenAIClient):
        self.client = client
    
    async def get_response(
        self,
        message: str,
        context: List[ChatMessage]
    ) -> CoachResponse:
        """Get a response from the coach."""
        messages = [
            ChatMessage(role="system", content=SYSTEM_PROMPT),
            *context,
            ChatMessage(role="user", content=message)
        ]
        
        prompt = "\n".join(f"{msg.role}: {msg.content}" for msg in messages)
        response = await self.client.get_completion(prompt)
        
        return CoachResponse(message=response)
