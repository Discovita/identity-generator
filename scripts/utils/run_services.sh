#!/bin/bash
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <app-name>"
    echo "Available apps: face-swapper, coach"
    exit 1
fi

APP_NAME=$1

if [ "$APP_NAME" != "face-swapper" ] && [ "$APP_NAME" != "coach" ]; then
    echo "Error: Invalid app name. Must be either 'face-swapper' or 'coach'"
    exit 1
fi

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

# Build frontend and copy to backend/public
./scripts/build.sh "$APP_NAME"

# Start the Python API server (which also serves frontend)
cd backend && uvicorn discovita.app:app --reload
