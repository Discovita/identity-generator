# Adalo Service

## Overview

The Adalo Service is a client library for interacting with Adalo's API in the Discovitas Identity Generator application. Adalo is a no-code platform used for building and managing mobile and web applications, and this service provides a clean, organized interface to interact with Adalo's REST API.

The service allows you to:

1. Manage user accounts (create, read, update, delete)
2. Manage identities (create, read, update, delete)
3. Handle pagination for multiple records

## Architecture

The service is structured with the following components:

### Models

- `base.py`: Contains base models that other models inherit from
  - `AdaloRecord`: Base model for records in Adalo (with id, created_at, updated_at fields)
  - `GetRecordsResponse`: Base model for API responses that return multiple records

- `user.py`: Models for user-related operations
  - `ProfilePhoto`: Model for profile photo information
  - `AdaloUser`: Model for user data with fields matching Adalo's user collection
  - `GetUsersResponse`: Model for responses from user listing endpoint

- `identity.py`: Models for identity-related operations
  - `AdaloIdentity`: Model for identity data with fields matching Adalo's identity collection
  - `GetIdentitiesResponse`: Model for responses from identity listing endpoint

### Client

- `base.py`: Contains the `BaseAdaloClient` class that implements core API operations:
  - Get records (with pagination and filtering)
  - Create records
  - Get a single record by ID
  - Update records
  - Delete records

- `users.py`: Contains the `UsersClient` class for user-specific operations:
  - Get users (with optional email filtering)
  - Create user
  - Get user by ID
  - Update user
  - Delete user

- `identities.py`: Contains the `IdentitiesClient` class for identity-specific operations:
  - Get identities
  - Create identity
  - Get identity by ID
  - Update identity
  - Delete identity

- `__init__.py`: Exports a main `AdaloClient` class that wraps both the user and identity clients

### Logging

- `logging.py`: Sets up a dedicated logger for the Adalo client that writes to `logs/adalo.log`

## Configuration

The service requires configuration through environment variables or direct parameter passing:

- `ADALO_APP_ID`: Your Adalo application ID
- `ADALO_API_KEY`: Your Adalo API key

This information is loaded through the `Settings` class from `discovita.config`.

## Usage Examples

### Basic Usage

```python
from discovita.service.adalo import AdaloClient
from discovita.service.adalo import AdaloUser, AdaloIdentity

# Create a client
client = AdaloClient()

# Use with context manager to ensure proper resource cleanup
with AdaloClient() as client:
    # Get all users
    users_response = client.get_users()
    
    for user in users_response.records:
        print(f"User ID: {user.id}, Name: {user.Full_Name}")
    
    # Get users with pagination
    more_users = client.get_users(offset=100, limit=50)
    
    # Filter users by email
    filtered_users = client.get_users(email="example@example.com")
    
    # Create a new user
    new_user = AdaloUser(
        Email="newuser@example.com",
        Username="newuser",
        Password="securepassword",
        Full_Name="New User"
    )
    created_user = client.create_user(new_user)
    
    # Get a specific user
    user = client.get_user(123)
    
    # Update a user
    user.Full_Name = "Updated Name"
    updated_user = client.update_user(user.id, user)
    
    # Delete a user
    client.delete_user(123)
    
    # Similar operations for identities
    identities = client.get_identities()
    
    new_identity = AdaloIdentity(
        Name="Example Identity",
        I_am_statement="I am confident"
    )
    created_identity = client.create_identity(new_identity)
```

### Advanced Configuration

```python
# Manually specify app ID and API key
client = AdaloClient(
    app_id="your-app-id",
    api_key="your-api-key"
)
```

## Collection IDs

The service uses specific Adalo collection IDs:

- Users Collection: `t_8200ffc0140b491aaac8db5b6d8d5ded`
- Identities Collection: `t_0lnnuplpppxwik9nor4e5n5w7`

## Error Handling

The client uses `httpx.Client` for HTTP requests and will raise appropriate exceptions for API errors. Common errors include:

- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Invalid API key
- `404 Not Found`: Record not found
- `429 Too Many Requests`: API rate limit exceeded

## Logging

The service logs detailed information about API requests and responses to `logs/adalo.log`. This is useful for debugging and monitoring API interactions.

## Type Safety

This service uses Python type annotations and Pydantic models for type safety, ensuring that data is properly validated and structured according to Adalo's API requirements.

## Dependencies

- `httpx`: For HTTP requests
- `pydantic`: For data validation and serialization
- `typing`: For type annotations

## Notes

- The Adalo API has rate limits which are not explicitly handled in this client. Consider implementing retry logic for production use.
- The client supports pagination with the `offset` and `limit` parameters.
- The user model includes fields for AI-generated profile pictures, indicating integration with AI image generation capabilities. 