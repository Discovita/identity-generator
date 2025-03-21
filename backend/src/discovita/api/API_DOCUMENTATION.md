# Discovita API Documentation

This document provides detailed API specifications for the Discovita Identity Generator backend.

## Base URL

```
https://api.discovita.com/
```

## Authentication

The API currently relies on service-level API keys configured in the application settings. Client authentication would be implemented at a higher level in the application.

## Error Responses

All endpoints may return the following error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - The request was invalid or cannot be served |
| 401 | Unauthorized - Authentication is required and has failed |
| 403 | Forbidden - The request is not allowed |
| 404 | Not Found - The requested resource does not exist |
| 422 | Validation Error - Request validation failed |
| 500 | Server Error - An error occurred on the server |

Error responses have the following format:

```json
{
  "detail": "Description of the error"
}
```

## Health Check

### GET /health

Checks the health status of the API.

**Response**

```json
{
  "status": "healthy"
}
```

## Image Generation

### POST /generate

Generates an image based on user criteria using OpenAI's DALL-E model.

**Request Body**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| setting | string | Yes | The scene or location setting for the image |
| outfit | string | Yes | The clothing or outfit description |
| emotion | string | Yes | The emotional tone for the image |
| userDescription | string | No | Clean description of the user's headshot |
| previousAugmentedPrompt | string | No | Previous prompt used, for refinement |
| userFeedback | string | No | User feedback on previous generations |

**Example Request**

```json
{
  "setting": "beach sunset",
  "outfit": "casual summer dress",
  "emotion": "happy",
  "userDescription": "Woman with blonde hair and blue eyes"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| imageUrl | string | URL to the generated image |
| augmentedPrompt | string | The full prompt used to generate the image |

**Example Response**

```json
{
  "imageUrl": "https://storage.discovita.com/generated/image-123.jpg",
  "augmentedPrompt": "A photorealistic image of a woman with blonde hair and blue eyes, wearing a casual summer dress, standing on a beach at sunset, looking happy."
}
```

**Error Responses**

In addition to standard errors, this endpoint may return:

| Status Code | Description |
|-------------|-------------|
| 500 | Generation failed - Details provided in error message |

## Face Swap

### POST /swap

Submits a face swap request and returns the result.

**Request Body**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source_url | string (URL) | Yes | URL to the source face image |
| target_url | string (URL) | Yes | URL to the target image where face will be placed |

**Example Request**

```json
{
  "source_url": "https://example.com/source_face.jpg",
  "target_url": "https://example.com/target_image.jpg"
}
```

**Response**

The response varies based on the processing status:

When processing is complete:
```json
{
  "url": "https://storage.discovita.com/processed/image-123.jpg",
  "status": "complete"
}
```

When processing is in progress:
```json
{
  "url": "",
  "status": "processing"
}
```

When processing fails:
```json
{
  "url": "",
  "status": "error"
}
```

## Image Description

### POST /describe

Generates a clean description of an uploaded image using OpenAI's vision models.

**Request Body**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_url | string (URL) | Yes | URL to the image to be described |

**Example Request**

```json
{
  "image_url": "https://example.com/my_image.jpg"
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| description | string | A textual description of the image content |

**Example Response**

```json
{
  "description": "A woman with blonde hair wearing sunglasses and a white blouse, standing in front of a brick wall"
}
```

## File Upload

### POST /upload

Uploads a file to S3 storage and returns the public URL.

**Request Body**

Multipart form data with a file field.

**Example Request**

```
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="profile.jpg"
Content-Type: image/jpeg

(binary data)
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| url | string | Public URL to the uploaded file |

**Example Response**

```json
{
  "url": "https://storage.discovita.com/uploads/profile-123.jpg"
}
```

**Error Responses**

In addition to standard errors, this endpoint may return:

| Status Code | Description |
|-------------|-------------|
| 400 | Missing filename or content type |

## Coach

### POST /coach/user_input

Provides interactive coaching responses based on user input.

**Request Body**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | The user's input or question |
| context | object | No | Additional context for the coach |
| history | array | No | Previous conversation history |

**Example Request**

```json
{
  "prompt": "How can I improve my self-confidence?",
  "context": {
    "user_goal": "personal growth",
    "user_style": "direct and practical"
  },
  "history": [
    {"role": "user", "content": "I want to become more confident"},
    {"role": "coach", "content": "That's a great goal. What specific areas do you want to focus on?"}
  ]
}
```

**Response**

| Field | Type | Description |
|-------|------|-------------|
| response | string | The coach's response to the user |
| suggestions | array | Optional array of suggested next steps |

**Example Response**

```json
{
  "response": "Building self-confidence takes practice and consistent effort. Start by identifying your strengths and celebrating small wins. Try setting one small goal each day that pushes you slightly out of your comfort zone.",
  "suggestions": [
    "Practice positive self-talk",
    "Set and achieve small goals",
    "Focus on your strengths"
  ]
}
```

## Usage Examples

### Python Example: Complete Workflow

This example demonstrates a typical workflow using multiple endpoints:

```python
import requests
import json

# Base URL for the API
base_url = "https://api.discovita.com"

# Step 1: Upload a user's photo
with open("user_photo.jpg", "rb") as f:
    files = {"file": f}
    upload_response = requests.post(f"{base_url}/upload", files=files)

if upload_response.status_code != 200:
    print(f"Upload failed: {upload_response.text}")
    exit(1)

user_photo_url = upload_response.json()["url"]

# Step 2: Get a description of the user
describe_response = requests.post(
    f"{base_url}/describe",
    json={"image_url": user_photo_url}
)

if describe_response.status_code != 200:
    print(f"Description failed: {describe_response.text}")
    exit(1)

user_description = describe_response.json()["description"]

# Step 3: Generate an image with the user in it
generate_response = requests.post(
    f"{base_url}/generate",
    json={
        "setting": "modern office",
        "outfit": "professional business suit",
        "emotion": "confident",
        "userDescription": user_description
    }
)

if generate_response.status_code != 200:
    print(f"Generation failed: {generate_response.text}")
    exit(1)

generated_image_url = generate_response.json()["imageUrl"]
prompt_used = generate_response.json()["augmentedPrompt"]

# Step 4: Swap the user's face onto the generated image
swap_response = requests.post(
    f"{base_url}/swap",
    json={
        "source_url": user_photo_url,
        "target_url": generated_image_url
    }
)

if swap_response.status_code != 200:
    print(f"Face swap failed: {swap_response.text}")
    exit(1)

result = swap_response.json()

# Check if processing is complete
if result["status"] == "complete":
    final_image_url = result["url"]
    print(f"Final image created: {final_image_url}")
else:
    print(f"Face swap status: {result['status']}")

# Step 5: Get coaching advice about professional presence
coaching_response = requests.post(
    f"{base_url}/coach/user_input",
    json={
        "prompt": "How can I improve my professional presence in this image?",
        "context": {
            "image_url": final_image_url if result["status"] == "complete" else generated_image_url
        }
    }
)

if coaching_response.status_code != 200:
    print(f"Coaching failed: {coaching_response.text}")
    exit(1)

coaching_advice = coaching_response.json()["response"]
print(f"Coaching advice: {coaching_advice}")
```

## Rate Limits

The API implements rate limiting to ensure fair usage. Current limits are:

- 10 requests per minute for `/generate` endpoint
- 20 requests per minute for `/swap` endpoint
- 50 requests per minute for other endpoints

Exceeding these limits will result in a 429 Too Many Requests response.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) for frontend applications from approved domains.

## Versioning

The current API version is v1. All endpoints should be prefixed with `/v1` to ensure compatibility with future API versions.

Example: `https://api.discovita.com/v1/generate` 