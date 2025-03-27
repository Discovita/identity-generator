#!/bin/bash
set -e

check_dependencies() {
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 is required but not installed."
        exit 1
    fi

    # Check Poetry
    if ! command -v poetry &> /dev/null; then
        echo "Poetry is required but not installed."
        echo "Install with: curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "Node.js is required but not installed."
        exit 1
    fi

    # Check npm
    if ! command -v npm &> /dev/null; then
        echo "npm is required but not installed."
        exit 1
    fi
}

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

# Main script execution
echo "Checking dependencies..."
check_dependencies

echo "Building $APP_NAME app..."

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

echo "Installing Python dependencies with Poetry..."
cd backend
# Configure poetry to create virtual environment in the project directory
poetry config virtualenvs.in-project true --local
# Install dependencies
poetry install
cd ..

echo "Building frontend..."
cd frontend
mkdir -p apps/$APP_NAME/build
npm install
npm run install:$APP_NAME
npm run build:$APP_NAME
cd ..

echo "Setting up backend public directory..."
mkdir -p backend/public
rm -rf backend/public/*
cp -r frontend/apps/$APP_NAME/build/* backend/public/

echo "Build complete!"
