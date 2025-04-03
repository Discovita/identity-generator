# OpenAI Service Test Suite

This directory contains a comprehensive test suite for the OpenAI Service. The tests cover all aspects of the service's functionality, including initialization, message creation, chat completions, structured outputs, image generation, and utility functions.

## Testing Strategy

The testing strategy for the OpenAI Service is designed to ensure:

1. **High Test Coverage:** Aim for 100% code coverage (or as close as possible) of all public APIs and critical internal functions.
2. **Isolation from Dependencies:** Most tests use mocking to avoid making actual API calls, allowing tests to run quickly and reliably without incurring costs.
3. **Comprehensive Testing:** Cover all features, edge cases, and error conditions the service might encounter.
4. **Maintainable Test Code:** Well-structured test code with clear documentation to make it easy to understand and maintain.

## Test Organization

The tests are organized into several modules, each covering a specific aspect of the service:

- `conftest.py`: Common fixtures and utilities for all tests
- `test_service_init.py`: Tests for service initialization and configuration
- `test_message_creation.py`: Tests for message creation functionality
- `test_chat_completion.py`: Tests for basic chat completion functionality
- `test_structured_outputs.py`: Tests for JSON mode and structured outputs
- `test_structured_completion.py`: Tests for structured completion with Pydantic models
- `test_ai_models.py`: Tests for model and provider enums and features
- `test_utils.py`: Tests for utility functions
- `test_image_generation.py`: Tests for DALL-E image generation functionality
- `test_streaming.py`: Tests for streaming responses
- `test_live_integration.py`: Live integration tests (disabled by default)

## Running the Tests

To run the entire test suite (excluding API-dependent tests):

```bash
pytest
```

To run a specific test module:

```bash
pytest tests/test_ai_models.py
```

To run with coverage report:

```bash
pytest --cov=discovita.service.openai_service
```

## API-Dependent Tests

The test suite includes tests that depend on the OpenAI API. These tests are marked with `@pytest.mark.requires_api` and are skipped by default to avoid incurring costs and potential API rate limits. 

There are two types of API-dependent tests:
1. **Integration tests with mocks**: These simulate API interaction but don't make actual API calls
2. **Live integration tests**: These make actual API calls to OpenAI

To run all API-dependent tests:

```bash
# Set your API key first (required for live tests)
export OPENAI_API_KEY=your_api_key_here

# Then run the tests with the special flag
pytest --run-api-tests
```

To run only a specific API-dependent test file:

```bash
pytest test_live_integration.py --run-api-tests
```

## Test Coverage Summary

The test suite covers the following areas:

### Core Functionality
- Service initialization and configuration
- API key and organization handling
- Dependency version checking

### Message Creation
- Text message creation
- System message handling
- Image input handling
- Multimodal message creation

### Chat Completion
- Basic text completions
- Parameter handling
- Model selection
- Temperature and token limit handling
- Streaming responses

### Structured Outputs
- JSON mode
- Schema validation
- Pydantic model integration
- Function calling

### Image Generation
- Parameter validation and processing
- Model-specific parameter handling (DALL-E 2 vs DALL-E 3)
- Response format options
- Response processing
- Image saving functionality
- Error handling

### Model Utilities
- Model identification
- Feature detection
- Parameter validation
- Token parameter naming

### Image Utilities
- Image encoding
- Format validation
- URL handling

## Adding New Tests

When adding new functionality to the service, please also add corresponding tests to maintain test coverage. Tests should be:

1. Well-documented with clear docstrings explaining what is being tested
2. Independent of external state or resources
3. Fast and reliable to execute

For tests that require API access:
1. Mark them with the `@pytest.mark.requires_api` decorator
2. Ensure they can run with a valid API key
3. Add appropriate checks to handle API errors gracefully

Each test file includes examples of how to structure and write tests for different parts of the service. 

## Test Structure for Image Generation

The image generation tests demonstrate a modular testing approach:

1. **Validation Tests:** Testing parameter validation and processing logic in isolation
2. **Response Processing Tests:** Verifying correct handling of API responses
3. **Utility Tests:** Testing image saving and encoding functionality
4. **Mixin Tests:** Testing the core mixin class functionality with mocked dependencies
5. **Integration Tests:** End-to-end tests with mocked API responses (requires `--run-api-tests`)
6. **Live API Tests:** Optional tests that run against the real OpenAI API (requires API key and `--run-api-tests`)

This structure allows for comprehensive testing of each component while maintaining test isolation and avoiding actual API calls during normal test runs. 