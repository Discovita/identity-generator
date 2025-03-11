"""Mock response and request classes for testing Icons8 client."""

from dataclasses import dataclass
from typing import Optional, Dict, List, Any

@dataclass
class MockRequest:
    """Mock implementation of httpx.Request."""
    url: str
    method: str = "POST"
    content: Optional[bytes] = None

    def decode(self) -> str:
        """Decode content to string."""
        return self.content.decode() if self.content else ""

class BaseMockResponse:
    """Base mock implementation of httpx.Response."""
    
    def __init__(self, status_code: int = 200, url: str = "https://api.icons8.com"):
        self.status_code = status_code
        # Add required Response attributes
        self.http_version = "1.1"
        self.headers = {}
        self.is_closed = True
        self.is_stream_consumed = True
        self.next_request = None
        # Add request attribute required for logging
        self.request = MockRequest(url=url)

    def read(self) -> bytes:
        """Mock read method."""
        return b""

    async def aread(self) -> bytes:
        """Mock async read method."""
        return b""

    def close(self) -> None:
        """Mock close method."""
        pass

    async def aclose(self) -> None:
        """Mock async close method."""
        pass

class MockLandmarksResponse(BaseMockResponse):
    """Mock response for the get_landmarks endpoint."""
    
    def __init__(self, data: List[Dict[str, Any]], status_code: int = 200, url: str = "https://api.icons8.com"):
        super().__init__(status_code, url)
        self._data = data
        self.text = str(data)

    def json(self) -> List[Dict[str, Any]]:
        """Return mock response data."""
        return self._data

class MockSwapResponse(BaseMockResponse):
    """Mock response for the process_image endpoint."""
    
    def __init__(self, data: Dict[str, Any], status_code: int = 200, url: str = "https://api.icons8.com"):
        super().__init__(status_code, url)
        self._data = data
        self.text = str(data)

    def json(self) -> Dict[str, Any]:
        """Return mock response data."""
        return self._data
