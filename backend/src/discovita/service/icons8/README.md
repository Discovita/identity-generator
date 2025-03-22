# Icons8 Face Swap Service

This service provides a robust interface for performing face swap operations using the Icons8 API. The service is designed with asynchronous operations, strong type safety, and comprehensive error handling.

## Architecture Overview

The service is composed of four main components:

### 1. Models (`models.py`)
Contains all data models used for API interactions and internal operations:

- **Core Types**:
  - `ImageId`: Type for unique image identifiers
  - `ProcessStatus`: Enum for tracking job status (QUEUE, PROCESSING, READY, ERROR, FAILED)
  - `Icons8Error`: Custom exception for API errors

- **Request/Response Models**:
  - `BoundaryAdjustments`: Face swap adjustment parameters
  - `FaceTask`: Configuration for individual face swap tasks
  - `ProcessedImage`: Processed image details
  - `FaceSwapResponse`: Complete face swap operation response
  - `GetBboxRequest/Response`: Models for bounding box operations
  - `ImageFaces`: Container for face detection results

### 2. Face Selection (`face_selection.py`)
Handles face detection and selection logic:

- `BoundingBox`: Represents detected face regions with:
  - Coordinates (x_min, y_min, x_max, y_max)
  - Confidence score
  - Helper methods for width, height, and relevance calculations
- `select_primary_face()`: Algorithm for selecting the most relevant face based on size and confidence

### 3. Client Module (`client/`)
Handles direct interactions with the Icons8 API:

- **Main Components**:
  - `Icons8Client`: Core client class with API endpoint implementations
  - `operations.py`: Low-level API operations implementation
  - `logging.py`: Request/response logging utilities

- **Key Operations**:
  - `get_landmarks()`: Fetch face landmarks for given images
  - `swap_faces()`: Submit and process face swap operations
  - `get_job_status()`: Check status of ongoing operations
  - `list_jobs()`: Retrieve all face swap jobs

- **Features**:
  - Automatic URL validation
  - Configurable timeouts (default: 90 seconds)
  - Detailed request/response logging
  - Error handling with custom exceptions

### 4. Service Layer (`icons8_service.py`)
Main service interface implementing face swap operations:

- `Icons8Service`: Core service class with:
  - Configurable polling parameters
  - Asynchronous face swap operations
  - Robust error handling and timeout management

## Usage

### Basic Face Swap Operation

```python
from discovita.service.icons8 import Icons8Service, Icons8Client

# Initialize the client and service
client = Icons8Client(
    api_key="your_api_key",
    base_url="https://api.icons8.com/api/v2"
)
service = Icons8Service(client)

# Perform face swap
result = await service.swap_faces(
    source_url="https://example.com/source.jpg",
    target_url="https://example.com/target.jpg"
)
```

### Advanced Usage

```python
# Get face landmarks for multiple images
landmarks = await client.get_landmarks([
    "https://example.com/face1.jpg",
    "https://example.com/face2.jpg"
])

# Check status of a specific job
status = await client.get_job_status("job_id_here")

# List all face swap jobs
jobs = await client.list_jobs()
```

### Response Format
The service returns a dictionary with:
- `url`: URL of the processed image
- `status`: Current status of the operation

### Error Handling
The service handles various error cases:
- API errors (with status codes and details)
- Timeouts (default 60 seconds max polling time)
- Processing failures
- Invalid face detection results
- URL validation errors

## Configuration

### Service Configuration
Key configuration parameters in `Icons8Service`:
- `max_polling_time`: Maximum time to wait for job completion (default: 60 seconds)
- `polling_interval`: Time between status checks (default: 2 seconds)

### Client Configuration
Parameters for `Icons8Client`:
- `api_key`: Required Icons8 API key
- `base_url`: API endpoint URL
- `timeout`: HTTP request timeout (default: 90 seconds)

## Implementation Details

### Face Selection Algorithm
The service uses a sophisticated face selection algorithm that:
1. Detects all faces in the image
2. Calculates relevance scores based on:
   - Face bounding box area
   - Detection confidence
3. Selects the face with the highest relevance score

### Asynchronous Processing
The service implements asynchronous processing using:
- Async/await patterns
- Efficient polling with configurable intervals
- Proper resource management
- Timeout handling

### Type Safety
- Comprehensive Pydantic models for request/response validation
- Strong typing throughout the codebase
- Explicit error types and handling
- URL validation using Pydantic's AnyHttpUrl

## Error Codes

Common error status codes:
- `504`: Operation timeout
- `500`: Processing failure
- `400`: Invalid request (e.g., invalid URLs)
- Other codes as returned by the Icons8 API

## Best Practices

When using this service:
1. Always handle potential exceptions
2. Consider implementing retry logic for transient failures
3. Monitor long-running operations
4. Validate input URLs before submission
5. Implement appropriate timeouts for your use case
6. Use the logging functionality for debugging
7. Keep API keys secure and never hardcode them 