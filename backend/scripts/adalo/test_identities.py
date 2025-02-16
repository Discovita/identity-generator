from datetime import datetime
import logging

from discovita.service.adalo.client import AdaloClient
from discovita.service.adalo.models.identity import AdaloIdentity

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    with AdaloClient() as client:
        # List existing identities
        logging.info("Fetching identities...")
        identities_response = client.get_identities(limit=2)
        logging.info(f"Found {len(identities_response.records)} identities")

        # Create a new identity
        new_identity = AdaloIdentity(**{
            "Name": "Test Identity",
            "show shadows, true?": True,
            "Today's Healthscore": 85,
            "Show I AM, true?": True,
            "Order #": 1,
            "Safety phrase": "Test safety phrase",
            "Actions completed count": 0,
            "Show, safety phrase, true": True,
            "Health Score": 90,
            "I am statement": "I am a test identity"
        })
        
        logging.info("Creating new identity...")
        created_identity = client.create_identity(new_identity)
        logging.info(f"Created identity with name: {created_identity.Name}")
        
        # Get the created identity
        logging.info(f"Fetching created identity {created_identity.id}...")
        fetched_identity = client.get_identity(created_identity.id)
        logging.info(f"Retrieved identity: {fetched_identity.Name}")
        
        # Update the identity
        fetched_identity.Health_Score = 95
        logging.info(f"Updating identity {fetched_identity.id}...")
        updated_identity = client.update_identity(fetched_identity.id, fetched_identity)
        logging.info(f"Updated identity health score: {updated_identity.Health_Score}")
        
        # Delete the identity
        logging.info(f"Deleting identity {updated_identity.id}...")
        client.delete_identity(updated_identity.id)
        logging.info("Identity deleted")

if __name__ == "__main__":
    main()
