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
uvicorn discovita.app:app --reload
