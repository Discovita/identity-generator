import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration
API_KEY = os.getenv("OPENAI_API_KEY")
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
PORT = int(os.getenv("PORT", "8000"))

async def main():
    # Initialize services
    llm_service = LLMService(API_KEY)
    db_service = DBService(DB_CONNECTION_STRING)
    await db_service.initialize()
    
    # Create and start the API
    coach_api = CoachAPI(llm_service, db_service)
    
    # Start FastAPI using uvicorn
    import uvicorn
    config = uvicorn.Config(coach_api.app, host="0.0.0.0", port=PORT)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
    