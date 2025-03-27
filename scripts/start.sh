#!/bin/bash
set -e

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

cd backend
# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Error: Poetry is required but not installed."
    echo "Install with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if the Poetry environment exists
if ! poetry env info &> /dev/null; then
    echo "Error: Poetry environment not found. Please run build.sh first."
    exit 1
fi

# If PORT is set, bind to 0.0.0.0 for production
if [ -n "${PORT}" ]; then
    # Run using Poetry environment
    poetry run uvicorn discovita.app:app --host 0.0.0.0 --port "${PORT}"
else
    # Run in development mode
    poetry run uvicorn discovita.app:app --reload --port 8000
fi
