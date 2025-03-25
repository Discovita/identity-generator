# Discovita Identity Generator Logger

The `discovita.utils.logger` module provides an enhanced logging system with custom log levels, colored console output, and optional file logging. This guide explains how to use the logger in the Discovita Identity Generator project.

## Features

- **Custom log levels** (FINE, STEP, SUCCESS) in addition to standard Python log levels
- **Colored console output** with level-specific formatting
- **Contextual logging** that automatically shows file, class, and function information
- **Detailed file logging** with rotation
- **Environment variable configuration** for log levels and context display options
- **Simple API** to quickly set up logging in any module

## Basic Usage

Here's how to use the logger in your Discovita modules:

```python
from discovita.utils.logger import configure_logging

# Configure logging for this module
log = configure_logging(__name__)

# Use standard log levels
log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")
log.critical("Critical message")

# Use custom log levels
log.fine("Fine-level message")
log.step("Step-level message")
log.success("Success message")
```

## Creating Custom Log Files

You can customize the log filename and location when configuring the logger:

```python
from discovita.utils.logger import configure_logging

# Create a logger with a custom log filename
logger = configure_logging(
    logger_name="my_module",
    keep_logs=True,
    log_dir="logs",
    log_filename="my_custom_file.log"  # Will create logs/my_custom_file.log
)
```

### Examples of Log File Organization

Here are some examples of how to organize your log files in the Discovita project:

#### 1. Component-Specific Log Files

```python
# API Logger
api_logger = configure_logging(
    logger_name="api",
    keep_logs=True,
    log_dir="logs",
    log_filename="api.log"  # Creates logs/api.log
)

# OpenAI Service Logger
openai_logger = configure_logging(
    logger_name="openai",
    keep_logs=True,
    log_dir="logs",
    log_filename="openai.log"  # Creates logs/openai.log
)

# Database Logger
db_logger = configure_logging(
    logger_name="database",
    keep_logs=True,
    log_dir="logs",
    log_filename="database.log"  # Creates logs/database.log
)
```

#### 2. Feature-Specific Log Files in Subdirectories

```python
# Identity generation logs
identity_logger = configure_logging(
    logger_name="identity",
    keep_logs=True,
    log_dir="logs/features",
    log_filename="identity_generation.log"  # Creates logs/features/identity_generation.log
)

# User authentication logs
auth_logger = configure_logging(
    logger_name="auth",
    keep_logs=True,
    log_dir="logs/features",
    log_filename="authentication.log"  # Creates logs/features/authentication.log
)
```

### Creating Utility Functions for Logging

For better organization, you can create utility functions for specific components:

```python
# In src/discovita/utils/logging_helpers.py
from discovita.utils.logger import configure_logging

def setup_service_logger(module_name, service_name):
    """Configure a logger for a specific service."""
    return configure_logging(
        logger_name=module_name, 
        keep_logs=True,
        log_dir="logs",
        log_filename=f"{service_name}.log"  # Creates logs/{service_name}.log
    )
```

Then in your service modules:

```python
# In src/discovita/service/openai/client.py
from discovita.utils.logging_helpers import setup_service_logger

logger = setup_service_logger(__name__, "openai")
logger.info("OpenAI client initialized")
```

## Log Levels

The logger provides three custom log levels in addition to Python's standard levels:

| Level       | Value  | Description                                                                           |
| ----------- | ------ | ------------------------------------------------------------------------------------- |
| DEBUG       | 10     | Detailed debugging information                                                        |
| **FINE**    | **15** | Less verbose than DEBUG, but more detailed than INFO                                  |
| INFO        | 20     | Confirmation that things are working as expected                                      |
| **SUCCESS** | **22** | Successful operations (with green formatting)                                         |
| **STEP**    | **25** | Major steps in program execution (with purple formatting)                             |
| WARNING     | 30     | Indication that something unexpected happened                                         |
| ERROR       | 40     | Due to a more serious problem, the software hasn't been able to perform a function    |
| CRITICAL    | 50     | A serious error, indicating that the program itself may be unable to continue running |

The custom levels provide more granularity for your logging needs.

## Configuration Options

### Basic Configuration

The `configure_logging` function accepts several parameters:

```python
from discovita.utils.logger import configure_logging

# Basic configuration with default settings
log = configure_logging(__name__)

# Configure with explicit log level
import logging
log = configure_logging(__name__, log_level=logging.INFO)

# Enable file logging
log = configure_logging(__name__, keep_logs=True)

# Specify custom log directory and filename
log = configure_logging(__name__, keep_logs=True, log_dir="my_logs", log_filename="app.log")
```

### Full Configuration Options

```python
def configure_logging(
    logger_name="root",      # Name of the logger (typically __name__)
    log_level=None,          # Log level (if None, reads from environment)
    keep_logs=False,         # Whether to write logs to file
    log_dir="logs",          # Directory for log files
    log_filename="logs.log"  # Name of the log file
):
    """Configure and return a logger with custom formatting."""
    # ...
```

## Environment Variables

The logger respects the following environment variables:

- `LOG_LEVEL`: Numeric log level (default: 15 for FINE)
- `CONTEXT_DISPLAY`: Controls how contextual information is displayed in logs:
  - `none`: No contextual information (default)
  - `function`: Shows only the function name - `[function_name()]`
  - `class_function`: Shows class and function name - `[ClassName.function_name()]`
  - `full`: Shows complete context - `[ClassName.function_name() in module.py:42]`

Example `.env` file for the Discovita project:

```
LOG_LEVEL=10
CONTEXT_DISPLAY=class_function
```

## Colored Console Output

The logger automatically formats console output with color-coded levels:

- **DEBUG**: Gray
- **FINE**: Blue
- **INFO**: Green
- **SUCCESS**: Green with ★ symbol (includes separator lines)
- **STEP**: Purple
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Bold Red

## File Logging

When `keep_logs=True`, the logger writes detailed logs to files:

- Logs are stored in the specified `log_dir` (default: "logs")
- The log filename can be specified with the `log_filename` parameter (default: "logs.log")
- Log files include full timestamps, level names, and source information
- Files rotate when they reach 5MB (keeping 3 backup files)

The file format is:

```
2025-03-09 14:35:22 [INFO] module_name: Log message (file.py:123)
```

## Direct Logger Access

If you need to access a logger that's already been configured:

```python
import logging

# Get a preconfigured logger
log = logging.getLogger(__name__)
```

## Complete Example

Here's a complete example showing how to use the logger in the Discovita project:

```python
# src/discovita/service/identity_generator.py
from discovita.utils.logger import configure_logging

log = configure_logging(
    __name__, 
    keep_logs=True, 
    log_dir="logs", 
    log_filename="identity_generator.log"
)

def generate_identity(user_id, template_id):
    log.fine(f"Starting identity generation for user: {user_id}")

    try:
        # Log a major step
        log.step("Preparing template image")
        # ... template preparation code ...
        
        log.step("Applying face swapping")
        # ... face swap processing code ...

        # Log success
        log.success(f"Identity successfully generated using template {template_id}")
        return identity_id
    except Exception as e:
        log.error(f"Failed to generate identity: {str(e)}")
        raise
```

## Contextual Logging

The logger can automatically include contextual information about where each log message originates. This is particularly useful for tracking the flow of operations in the Discovita Identity Generator.

For example, with `CONTEXT_DISPLAY=class_function`:

```python
# In the identity service class
class IdentityService:
    def generate(self, user_data):
        logger.info("Generating new identity...")  # Will show: INFO: Generating new identity... [IdentityService.generate()]
```

## Best Practices for Discovita Project

1. **Use consistent logging across modules**: Consider creating a central logging utility module.

2. **Use meaningful log filenames**: Use descriptive filenames that indicate the component or feature being logged.

3. **Use appropriate log levels**:
   - DEBUG/FINE for development details
   - INFO for normal operations
   - STEP for major processing phases
   - SUCCESS for completed operations
   - WARNING for non-critical issues
   - ERROR/CRITICAL for serious problems

4. **Log key operations in identity generation process**:
   ```python
   logger.step("Starting face swap operation")
   logger.fine(f"Using template: {template_id}")
   # ... processing ...
   logger.success(f"Identity generated successfully: {identity_id}")
   ```

5. **Include context in error logs**:
   ```python
   except Icons8ApiError as e:
       logger.error(f"Face swap API error: {str(e)}", exc_info=True)
   ```

6. **Use structured logging for complex operations**:
   ```python
   logger.info(f"Processing user request: user_id={user_id}, template={template}, options={options}")
   ```

## Troubleshooting

**Problem**: No console output is visible.  
**Solution**: Check that your log level is not set too high. If LOG_LEVEL is set to 30, debug/fine/info messages won't show.

**Problem**: Colors don't appear in console output.  
**Solution**: Some terminals don't support ANSI color codes. Try running in a different terminal.

**Problem**: Log files aren't being created.  
**Solution**: Ensure you've set `keep_logs=True` and that the application has write permission to the log directory.
