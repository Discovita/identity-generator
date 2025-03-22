# Discovita API Module

This README provides a comprehensive guide to the API implementation in the Discovita Identity Generator backend.

## Overview

The API module is a FastAPI-based implementation that provides various endpoints for:
- Image generation using OpenAI's DALL-E
- Face swapping using Icons8's service
- Image description using OpenAI's vision models
- File uploads to S3
- Interactive coaching functionality

## Structure

```
api/
├── dependencies.py    # FastAPI dependency injection functions
├── router.py         # Main API router configuration
└── routes/           # Individual endpoint implementations
    ├── coach.py
    ├── face_swap.py
    ├── image_description.py
    ├── image_generation.py
    └── upload.py
```

## API Dependencies

The `dependencies.py` file provides dependency injection functions for FastAPI routes. These functions create and return service instances that handle business logic:

- **get_openai_client**: Creates an OpenAI client instance using API keys from settings
- **get_image_description_service**: Returns an ImageDescriptionService for analyzing images
- **get_image_generation_service**: Returns an ImageGenerationService for creating images with DALL-E
- **get_coach_service**: Returns a CoachService for interactive coaching functionality

## Router Configuration

The `router.py` file configures the main API router and includes all route modules:

- Provides a `/health` endpoint for health checks
- Includes all route modules with appropriate tags for API documentation
- Organizes routes with logical prefixes

## Route Endpoints

### Image Generation (`image_generation.py`)

- **POST /generate**: Generates images based on user criteria
  - Takes settings, outfit, emotion, and optional user description/feedback
  - Returns generated image URL and the augmented prompt used

### Face Swap (`face_swap.py`)

- **POST /swap**: Performs face swap operations using Icons8's service
  - Takes source and target image URLs
  - Returns job status and result URL when complete

### Image Description (`image_description.py`)

- **POST /describe**: Generates clean descriptions of input images
  - Takes an image URL
  - Returns a text description of the image content

### File Upload (`upload.py`)

- **POST /upload**: Handles file uploads to S3 storage
  - Takes file data with proper validation
  - Returns a public URL to the uploaded file

### Coach (`coach.py`)

- **POST /coach/user_input**: Provides interactive coaching responses
  - Takes user input in a structured format
  - Returns personalized coaching responses

## Data Models

The API uses Pydantic models (defined in `models.py`) for request/response validation:

- **DescribeImageRequest/Response**: For image description operations
- **GenerateImageRequest/Response**: For image generation operations
- **SwapFaceRequest**: For face swap operations
- **SwapFaceResult**: For face swap results, including processing status

## Usage Examples

### Generating an Image

```python
import requests

response = requests.post(
    "https://api.example.com/generate",
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
    "https://api.example.com/swap",
    json={
        "source_url": "https://example.com/source_face.jpg",
        "target_url": "https://example.com/target_image.jpg"
    }
)
result = response.json()
swapped_image_url = result["url"]
```

### Uploading a File

```python
import requests

files = {"file": open("user_photo.jpg", "rb")}
response = requests.post("https://api.example.com/upload", files=files)
uploaded_url = response.json()["url"]
```

## Service Dependencies

The API relies on several service implementations:

- **OpenAI Services**: For image generation and description
- **Icons8 Service**: For face swapping functionality
- **S3 Service**: For file storage
- **Coach Service**: For interactive coaching responses

## Error Handling

All endpoints include appropriate error handling:

- Input validation through Pydantic models
- HTTP exception handling with appropriate status codes
- Service-level error handling with clean error messages passed to clients

## Authentication

The API endpoints rely on service-level API keys configured through the application settings:

- OpenAI API key for image generation and description
- Icons8 API key for face swapping
- AWS credentials for S3 operations

Client authentication would be implemented at a higher level in the application. 