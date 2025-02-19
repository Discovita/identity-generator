"""Mock response classes for testing OpenAI client."""

from dataclasses import dataclass
from typing import List


@dataclass
class MockMessage:
    """Mock implementation of OpenAI chat message."""
    content: str


@dataclass
class MockChoice:
    """Mock implementation of OpenAI choice."""
    message: MockMessage
    index: int = 0
    finish_reason: str = "stop"


@dataclass
class MockChatResponse:
    """Mock implementation of OpenAI chat completion response."""
    choices: List[MockChoice]
    id: str = "mock-response"
    created: int = 1613779763
    model: str = "gpt-4"
    object: str = "chat.completion"

    def model_dump(self):
        """Make response JSON serializable."""
        return {
            "id": self.id,
            "created": self.created,
            "model": self.model,
            "object": self.object,
            "choices": [
                {
                    "index": c.index,
                    "message": {"content": c.message.content},
                    "finish_reason": c.finish_reason
                }
                for c in self.choices
            ]
        }
