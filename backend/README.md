# Backend

Backend service for the Identity Generator application.

## Overview

This is the backend component of the Identity Generator application, providing API endpoints and services for the frontend applications.

## Project Structure

- `src/discovita/`: Main application code

  - `api/`: API endpoints and routes
  - `service/`: Business logic and services
  - `models.py`: Data models
  - `config.py`: Configuration settings
  - `app.py`: Main application entry point

- `test/`: Test files
- `scripts/`: Utility scripts

## Development

For development setup and workflow instructions, please refer to the project documentation

## Poetry

### Installation

```bash
# Globally install Poetry using the official installer
curl -sSL https://install.python-poetry.org | python3 -
```

For more installation options, see the [official installation documentation](https://python-poetry.org/docs/#installation).

### Virtual Environment Management

#### Default Behavior

By default, Poetry creates virtual environments in a centralized location:

- Linux/macOS: `~/.cache/pypoetry/virtualenvs/`
- Windows: `%APPDATA%\pypoetry\virtualenvs/`

#### Local Virtual Environment (Optional)

If you prefer having the virtual environment in your project directory (this is a global setting for all projects using Poetry):

```bash
# Configure Poetry to create virtualenvs in the project directory
poetry config virtualenvs.in-project true
```

This creates a `.venv` folder in your project directory when you run `poetry install`.

For more information, see [Managing environments](https://python-poetry.org/docs/managing-environments/).

## Key Commands

| Command                            | Description                                           |
| ---------------------------------- | ----------------------------------------------------- |
| `poetry install`                   | Creates virtual environment and installs dependencies |
| `poetry add <package>`             | Adds a new dependency                                 |
| `poetry add <package> --group dev` | Adds a development dependency                         |
| `poetry remove <package>`          | Removes a dependency                                  |
| `poetry update`                    | Updates dependencies to their latest versions         |
| `poetry shell`                     | Activates the virtual environment                     |
| `poetry run <command>`             | Runs a command within the virtual environment         |
| `poetry lock`                      | Updates the lock file without installing packages     |
| `poetry env info`                  | Shows information about the virtual environment       |

For a complete list of commands, see the [Poetry commands documentation](https://python-poetry.org/docs/cli/).

#### First-Time Project Setup

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install dependencies
poetry install
```

This single command creates a virtual environment and installs all dependencies.

### Additional Resources

- [Official Poetry Documentation](https://python-poetry.org/docs/)
