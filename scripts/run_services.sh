#!/bin/bash
set -e  # Exit on any error

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

# Function to clean up on script exit
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Build frontend and copy to backend/public
./scripts/build.sh

# Activate the virtual environment
source backend/venv/bin/activate

echo "Starting API server..."
cd backend
# Use the venv's Python to run uvicorn
python -m uvicorn src.discovita.app:app --reload
