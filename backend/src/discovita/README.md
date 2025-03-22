# Discovita Identity Generator Backend

## Overview

The Discovita Identity Generator is an AI-powered service that helps users explore and define new identities through guided coaching, image generation, and face swapping. This backend serves as the core of the system, providing a comprehensive set of APIs for identity transformation.

## Key Features

- **AI Coaching**: Interactive identity exploration through structured dialogue
- **Image Generation**: Create custom images based on identity contexts using DALL-E
- **Face Swapping**: Apply user faces to generated images using Icons8 API
- **Image Description**: Analyze and describe images using OpenAI's vision models
- **File Storage**: Secure file uploads to AWS S3
- **Adalo Integration**: Sync user data with Adalo no-code platform

## Project Structure

```
discovita/
├── api/                  # API endpoint implementations
│   ├── routes/           # Route modules for different API features
│   ├── dependencies.py   # FastAPI dependency injection
│   └── router.py         # Main API router configuration
├── db/                   # Database and state persistence
│   └── state_store.py    # Context persistence for coaching
├── service/              # Core business logic services
│   ├── adalo/            # Adalo no-code platform integration
│   ├── coach/            # Identity coaching implementation
│   ├── icons8/           # Face swap API client and services
│   ├── openai/           # OpenAI client for AI operations
│   └── s3/               # AWS S3 storage implementation
├── app.py                # FastAPI application factory
├── config.py             # Application configuration
├── dependencies.py       # Global dependencies
└── models.py             # Shared data models
```

## Core Components

### 1. API Layer

The API layer exposes HTTP endpoints using FastAPI:

- **Face Swap API**: Perform face swapping operations
- **Image Generation API**: Create AI-generated images with DALL-E
- **Image Description API**: Analyze images with GPT-4 Vision
- **Upload API**: Handle secure file uploads
- **Coach API**: Provide interactive coaching sessions

### 2. Service Layer

The service layer implements the core business logic:

- **OpenAI Service**: Type-safe client for OpenAI APIs (Chat, DALL-E, Vision)
- **Icons8 Service**: Robust client for face swap operations
- **Coach Service**: Identity coaching system with state management
- **S3 Service**: File upload and management
- **Adalo Service**: Integration with Adalo no-code platform

### 3. Data Models

The application uses Pydantic models for request/response validation:

- **Identity Models**: Represent user identities
- **Coach Models**: Support coaching conversations
- **API Models**: Validate API requests and responses

## Configuration

The application uses a `Settings` class to manage configuration from environment variables:

```python
# Required environment variables
FACESWAP_API_KEY=your_icons8_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
OPENAI_API_KEY=your_openai_api_key
ADALO_APP_ID=your_adalo_app_id
ADALO_API_KEY=your_adalo_api_key
```

## Installation and Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set environment variables (see Configuration)
4. Run the development server:
   ```
   uvicorn discovita.app:app --reload
   ```

## API Usage Examples

### Generating an Image

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "setting": "beach sunset",
        "outfit": "casual summer dress",
        "emotion": "happy",
        "userDescription": "Woman with blonde hair"
    }
)
result = response.json()
image_url = result["imageUrl"]
prompt_used = result["augmentedPrompt"]
```

### Swapping Faces

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/swap",
    json={
        "source_url": "https://example.com/source_face.jpg",
        "target_url": "https://example.com/target_image.jpg"
    }
)
result = response.json()
swapped_image_url = result["url"]
```

### Interactive Coaching

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/coach/user_input",
    json={
        "user_id": "user123",
        "message": "I want to explore my professional identity",
        "context": []  # Previous messages if any
    }
)
coaching_response = response.json()
coach_message = coaching_response["message"]
```

## Integration Features

### Face Swap Integration

The system uses Icons8's face swap API to apply user faces to generated images:

1. User uploads a selfie
2. System generates an identity-based image with DALL-E
3. Face swap applies the user's face to the generated image

### OpenAI Integration

The system leverages several OpenAI capabilities:

- **GPT-4/GPT-4o**: Powers the coaching dialogue
- **DALL-E**: Generates identity visualization images
- **Vision API**: Analyzes user photos for accurate descriptions

### Adalo Integration

The backend syncs user data with an Adalo no-code application:

- User accounts and information
- Identity records and preferences
- Generated images and face swaps

## Development Considerations

### Authentication and Security

- API keys are managed through environment variables
- S3 uploads use randomized filenames to prevent conflicts
- The API implements CORS protection

### Error Handling

- Comprehensive error handling in all services
- Structured error responses for clients
- Detailed logging for debugging

### Performance

- Asynchronous operations for I/O-bound tasks
- Efficient polling for long-running operations
- Configurable timeouts for external services

## Coaching Process

The coaching system implements a state-based approach:

1. **Identity Exploration**: Dialogue to explore potential identities
2. **Identity Proposal**: Present specific identity options 
3. **Identity Confirmation**: Confirm and refine chosen identities
4. **Visualization**: Generate visual representations of identities
5. **Embodiment**: Provide guidance for embodying the new identity

## Architecture Decisions

1. **Service-Based Design**: Clean separation of concerns
2. **Type Safety**: Comprehensive use of Pydantic models
3. **Async I/O**: Efficient handling of external API calls
4. **Stateful Coaching**: Maintaining conversation context
5. **Extensibility**: Modular design for adding new features

## Contributors

- Discovitas Team

## License

Proprietary - All rights reserved 