#!/bin/bash
set -e

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

cd backend
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found. Please run build.sh first."
    exit 1
fi

. .venv/bin/activate

# If PORT is set, bind to 0.0.0.0 for production
if [ -n "${PORT}" ]; then
    uvicorn discovita.app:app --host 0.0.0.0 --port "${PORT}"
else
    uvicorn discovita.app:app --reload --port 8000
fi
