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
class MockContentFilter:
    """Mock implementation of OpenAI content filter."""
    is_violating: bool
    category: str | None = None
    explanation_if_violating: str | None = None

@dataclass
class MockChatResponse:
    """Mock implementation of OpenAI chat completion response."""
    choices: List[MockChoice]
    content_filter: MockContentFilter | None = None
    id: str = "mock-response"
    created: int = 1613779763
    model: str = "gpt-4"
    object: str = "chat.completion"

    def model_dump(self):
        """Make response JSON serializable."""
        response = {
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
        if self.content_filter:
            response["content_filter"] = {
                "is_violating": self.content_filter.is_violating,
                "category": self.content_filter.category,
                "explanation_if_violating": self.content_filter.explanation_if_violating
            }
        return response
