from typing import Dict, Any, Optional
import json
from pathlib import Path
import asyncio
import os

from discovita.service.coach.models import CoachContext

class ContextPersistence:
    """Interface for context persistence."""
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context for a user."""
        raise NotImplementedError
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context for a user."""
        raise NotImplementedError

class FileContextPersistence(ContextPersistence):
    """File-based implementation of context persistence."""
    
    def __init__(self, data_dir: str = None):
        """Initialize with the data directory."""
        if data_dir is None:
            # Default to a data directory in the package
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        # Create the data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context from a file."""
        file_path = self._get_file_path(user_id)
        
        if not file_path.exists():
            return None
        
        # Use asyncio to read the file without blocking
        try:
            context_data = await asyncio.to_thread(self._read_file, file_path)
            return CoachContext.model_validate(context_data)
        except Exception as e:
            # Log the error
            print(f"Error loading context for user {user_id}: {e}")
            return None
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context to a file."""
        file_path = self._get_file_path(context.user_id)
        
        # Use asyncio to write the file without blocking
        try:
            await asyncio.to_thread(
                self._write_file, 
                file_path, 
                context.model_dump()
            )
        except Exception as e:
            # Log the error
            print(f"Error saving context for user {context.user_id}: {e}")
    
    def _get_file_path(self, user_id: str) -> Path:
        """Get the file path for a user's context."""
        return self.data_dir / f"{user_id}.json"
    
    def _read_file(self, file_path: Path) -> Dict[str, Any]:
        """Read and parse a JSON file."""
        with open(file_path, "r") as f:
            return json.load(f)
    
    def _write_file(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Write data to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

class DatabaseContextPersistence(ContextPersistence):
    """Database implementation of context persistence."""
    
    def __init__(self, db_client):
        """Initialize with a database client."""
        self.db_client = db_client
    
    async def load_context(self, user_id: str) -> Optional[CoachContext]:
        """Load context from the database."""
        # Query the database for the user's context
        context_data = await self.db_client.get_context(user_id)
        
        if not context_data:
            return None
        
        return CoachContext.model_validate(context_data)
    
    async def save_context(self, context: CoachContext) -> None:
        """Save context to the database."""
        # Save the context to the database
        await self.db_client.save_context(
            context.user_id, 
            context.model_dump()
        )
