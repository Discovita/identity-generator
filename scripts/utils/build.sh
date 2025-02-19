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

echo "Setting up Python environment..."
# Remove existing venv if it exists
rm -rf backend/venv
# Create fresh venv
python3 -m venv backend/venv
source backend/venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
cd backend
# Install exact versions from requirements.txt
pip install -r requirements.txt
# Install the local package in editable mode
pip install -e .
cd ..

echo "Building frontend..."
cd frontend
# Clean install npm dependencies
rm -rf node_modules
npm ci  # Uses package-lock.json for exact versions
npm run build

echo "Copying frontend build to backend/public..."
rm -rf ../backend/public
mkdir -p ../backend/public
cp -r build/* ../backend/public/

echo "Build complete!"
