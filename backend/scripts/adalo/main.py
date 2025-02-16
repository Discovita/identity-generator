from datetime import datetime
import logging

from discovita.service.adalo import AdaloClient, AdaloUser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    with AdaloClient() as client:
        logging.info("Fetching users...")
        users_response = client.get_users(limit=2)
        logging.info(f"Found {len(users_response.records)} users")

        test_email = "test3@example.com"
        new_user = AdaloUser(**{
            "Email": test_email,
            "Username": "testuser",
            "Full Name": "Test User",
            "Admin": True,
            "Daily Reminder, true": True,
            "show identity, true?": True,
            "Download identity count.": 0,
            "Turn On": "2025-02-07T14:15:22Z",
            "AI Image Copy": "string"
        })
        
        # Check if user already exists
        existing_users = client.get_users(limit=1, email=test_email)
        
        if existing_users.records:
            user = existing_users.records[0]
            logging.info(f"Found existing user: {user.dict()}")
        else:
            logging.info("Creating new user...")
            user = client.create_user(new_user)
            logging.info(f"Created user with email: {user.Email}")
        
        logging.info("Fetching single user...")
        # Get the first user from our list
        first_user_id = users_response.records[0].id
        user = client.get_user(first_user_id)
        logging.info(f"Retrieved user: {user.Full_Name}")

if __name__ == "__main__":
    main()
