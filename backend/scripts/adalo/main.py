from datetime import datetime
import logging
import os

from client import AdaloClient
from models import AdaloUser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    app_id = os.environ.get("ADALO_APP_ID")
    api_key = os.environ.get("ADALO_API_KEY")
    
    assert app_id, "ADALO_APP_ID environment variable is required"
    assert api_key, "ADALO_API_KEY environment variable is required"
    
    client = AdaloClient(app_id, api_key)
    
    logging.info("Fetching users...")
    users_response = client.get_users(limit=2)
    logging.info(f"Found {len(users_response.records)} users")
    
    new_user = AdaloUser(
        Email="test@example.com",
        Username="testuser",
        Full_Name="Test User",
        Admin=False,
        Daily_Reminder=True,
        show_identity=True,
        Download_identity_count=0,
        Turn_On=datetime.now(),
        AI_Image_Copy=""
    )
    
    logging.info("Creating new user...")
    created_user = client.create_user(new_user)
    logging.info(f"Created user with email: {created_user.Email}")
    
    logging.info("Fetching single user...")
    user = client.get_user(1)
    logging.info(f"Retrieved user: {user.Full_Name}")

if __name__ == "__main__":
    main()
