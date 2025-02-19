#!/bin/bash
set -e

check_dependencies() {
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 is required but not installed."
        exit 1
    fi

    # Check pip
    if ! command -v pip &> /dev/null; then
        echo "pip is required but not installed."
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

    # Check/setup Python virtual environment
    cd backend
    if [ ! -d ".venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    if [[ "$VIRTUAL_ENV" != *"/backend/.venv" ]]; then
        echo "Activating virtual environment..."
        . .venv/bin/activate
        python -m pip install --upgrade pip
    fi
    cd ..
}

# Get app name from argument or prompt
get_app_name() {
    if [ $# -eq 1 ]; then
        APP_NAME=$1
    else
        echo "Which app would you like to run?"
        echo "1) face-swapper"
        echo "2) coach"
        read -p "Enter 1 or 2: " choice
        case $choice in
            1) APP_NAME="face-swapper" ;;
            2) APP_NAME="coach" ;;
            *) echo "Invalid choice. Please enter 1 or 2."; exit 1 ;;
        esac
    fi

    if [ "$APP_NAME" != "face-swapper" ] && [ "$APP_NAME" != "coach" ]; then
        echo "Error: Invalid app name. Must be either 'face-swapper' or 'coach'"
        exit 1
    fi
}

# Main script execution
echo "Checking dependencies..."
check_dependencies

# Get app name
get_app_name "$@"

echo "Starting $APP_NAME app..."

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

echo "Installing Python dependencies..."
cd backend
. .venv/bin/activate
python -m pip install -e .
cd ..

echo "Building frontend..."
cd frontend
npm install
npm run install:$APP_NAME
npm run build:$APP_NAME
cd ..

echo "Setting up backend public directory..."
rm -rf backend/public/*
cp -r frontend/apps/$APP_NAME/build/* backend/public/

echo "Starting server..."
cd backend
. .venv/bin/activate
uvicorn discovita.app:app --reload
