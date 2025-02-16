import logging
from datetime import datetime

from discovita.service.adalo import AdaloClient, AdaloUser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def find_available_email(client: AdaloClient, start_n: int = 4) -> str:
    n = start_n
    while True:
        test_email = f"test{n}@example.com"
        users = client.get_users(limit=1, email=test_email)
        if not users.records:
            return test_email
        n += 1

def main():
    with AdaloClient() as client:
        # Find first available email
        email = find_available_email(client)
        logging.info(f"Found available email: {email}")
        
        # Create new user
        new_user = AdaloUser(**{
            "Email": email,
            "Username": f"testuser{email.split('@')[0][4:]}",
            "Full Name": "Test User",
            "Admin": True,
            "Daily Reminder, true": True,
            "show identity, true?": True,
            "Download identity count.": 0,
            "Turn On": datetime.utcnow().isoformat() + "Z",
            "AI Image Copy": "string"
        })
        
        created_user = client.create_user(new_user)
        logging.info(f"Created user: {created_user.dict()}")
        
        # Verify we can fetch the created user
        fetched_users = client.get_users(limit=1, email=email)
        if not fetched_users.records:
            error_msg = f"Failed to fetch newly created user with email: {email}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
        
        fetched_user = fetched_users.records[0]
        logging.info(f"Successfully fetched created user: {fetched_user.dict()}")

if __name__ == "__main__":
    main()
