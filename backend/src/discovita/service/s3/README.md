# S3 Service Documentation

## Overview
The S3 Service is a Python module that provides a clean and type-safe interface for uploading files to Amazon S3. It's designed to be used within the Discovitas identity-generator backend application.

## Components

### 1. Models (`models.py`)
The service uses Pydantic models for type-safe data handling:

- `FileUploadRequest`: A data model for file upload operations
  - `filename`: Original name of the file
  - `content_type`: MIME type of the file (e.g., "image/jpeg")
  - `content`: The actual file content as bytes

### 2. Service Implementation (`service.py`)
The `S3Service` class handles all S3-related operations:

#### Key Features:
- Automatic unique filename generation using UUID4
- Configurable S3 bucket and region
- Secure AWS credentials management
- Returns public URLs for uploaded files

#### File Storage Structure:
- All files are stored in an `uploads/` directory in the S3 bucket
- Files are renamed using UUID4 to prevent naming conflicts while preserving original extensions

## Usage Example

```python
from discovita.service.s3 import S3Service, FileUploadRequest
from discovita.config import Settings

# Initialize the service
settings = Settings()  # Your application settings
s3_service = S3Service(settings)

# Create an upload request
upload_request = FileUploadRequest(
    filename="example.jpg",
    content_type="image/jpeg",
    content=b"your_file_bytes_here"
)

# Upload the file
public_url = s3_service.upload(upload_request)
print(f"File uploaded successfully: {public_url}")
```

## Configuration Requirements
The service requires the following settings to be configured:

- `aws_access_key_id`: Your AWS access key
- `aws_secret_access_key`: Your AWS secret key
- `aws_region`: AWS region (e.g., "us-east-1")
- `s3_bucket`: Name of your S3 bucket

These settings should be provided through the application's `Settings` class.

## Security Considerations
- AWS credentials are never hardcoded and must be provided through the settings
- File names are automatically randomized to prevent conflicts and potential security issues
- The service uses boto3's secure configuration practices

## Dependencies
- boto3: AWS SDK for Python
- pydantic: Data validation using Python type annotations
- Python 3.6+

## Best Practices
1. Always handle the returned URL appropriately - it contains the public path to your uploaded file
2. Consider implementing file type restrictions if needed
3. Implement proper error handling when using the service
4. Monitor your S3 bucket usage and implement cleanup strategies as needed

## Internal Implementation Details

### File Upload Process
1. The service receives a `FileUploadRequest` with file details
2. Generates a unique filename using UUID4 while preserving the original extension
3. Constructs the S3 key with the "uploads/" prefix
4. Uploads the file using boto3's put_object method
5. Returns a publicly accessible URL for the uploaded file

### URL Format
The returned URL follows the format:
`https://{bucket}.s3.{region}.amazonaws.com/uploads/{uuid4}{extension}` 