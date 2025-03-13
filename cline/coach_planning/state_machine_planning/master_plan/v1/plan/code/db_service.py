from typing import Dict, Any, List, Optional
import asyncpg

class DBService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None
    
    async def initialize(self) -> None:
        """Initialize database connection pool."""
        self.pool = await asyncpg.create_pool(self.connection_string)
    
    async def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get all data for a user."""
        async with self.pool.acquire() as connection:
            # Get basic user info
            user = await connection.fetchrow(
                "SELECT * FROM users WHERE id = $1",
                user_id
            )
            
            if not user:
                return None
            
            # Get identities
            identities = await connection.fetch(
                "SELECT * FROM identities WHERE user_id = $1",
                user_id
            )
            
            # Get actions
            actions = await connection.fetch(
                "SELECT * FROM actions WHERE user_id = $1",
                user_id
            )
            
            # Convert to dictionary
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "current_state": user["current_state"],
                "consolidated_summary": user["consolidated_summary"],
                "user_data": json.loads(user["user_data"]),
                "identities": [dict(identity) for identity in identities],
                "actions": [dict(action) for action in actions]
            }
    
    async def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Update a specific piece of user data."""
        async with self.pool.acquire() as connection:
            # Check if user exists
            user = await connection.fetchrow(
                "SELECT user_data FROM users WHERE id = $1",
                user_id
            )
            
            if not user:
                # Create user if they don't exist
                await connection.execute(
                    "INSERT INTO users (id, user_data) VALUES ($1, $2)",
                    user_id, json.dumps({key: value})
                )
                return
            
            # Update existing user data
            user_data = json.loads(user["user_data"])
            user_data[key] = value
            
            await connection.execute(
                "UPDATE users SET user_data = $1 WHERE id = $2",
                json.dumps(user_data), user_id
            )
    
    async def save_identity(self, user_id: str, identity: str, description: str) -> None:
        """Save a new identity for a user."""
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO identities (user_id, name, description)
                VALUES ($1, $2, $3)
                """,
                user_id, identity, description
            )
    
    async def update_state(self, user_id: str, state: str) -> None:
        """Update the current state for a user."""
        async with self.pool.acquire() as connection:
            await connection.execute(
                "UPDATE users SET current_state = $1 WHERE id = $2",
                state, user_id
            )
    
    async def save_action(self, user_id: str, action: str, identity_id: Optional[int] = None) -> None:
        """Save a new action for a user."""
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO actions (user_id, description, identity_id)
                VALUES ($1, $2, $3)
                """,
                user_id, action, identity_id
            )
            