#!/bin/bash
set -e  # Exit on any error

# Function to clean up on script exit
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Function to check and install Python dependencies
setup_python() {
    echo "Setting up Python environment..."
    # Remove existing venv if it exists
    rm -rf backend/venv
    # Create fresh venv
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install --upgrade pip
    cd backend
    pip install -r requirements.txt
    pip install -e .
    cd ..
}

# Function to check and install Node dependencies
setup_node() {
    local app=$1
    echo "Setting up Node.js environment for $app..."
    cd frontend
    rm -rf node_modules
    npm ci  # Uses package-lock.json for exact versions
    cd ..
}

# Function to build frontend
build_frontend() {
    local app="$1"
    echo "Building frontend for $app..."
    cd frontend
    # Ensure we're using the exact app name for the build script
    if [ "$app" = "face-swapper" ]; then
        PUBLIC_URL="/face-swapper" REACT_APP_APP_TYPE=face-swapper npm run build
    elif [ "$app" = "coach" ]; then
        PUBLIC_URL="/coach" REACT_APP_APP_TYPE=coach npm run build
    else
        echo "Error: Unknown app type: $app" >&2
        exit 1
    fi
    cd ..
}

# Function to copy frontend build to backend
setup_backend_public() {
    local app=$1
    echo "Setting up backend public directory for $app..."
    rm -rf backend/public
    mkdir -p "backend/public/$app"
    cp -r frontend/build/* "backend/public/$app/"
    # Copy index.html to root for direct access
    cp "backend/public/$app/index.html" backend/public/
}

# Function to prompt for app selection if not provided
select_app() {
    local selected_app="$1"
    if [ -z "$selected_app" ]; then
        echo "Which app would you like to run?"
        select choice in "face-swapper" "coach"; do
            case $choice in
                face-swapper|coach)
                    selected_app="$choice"
                    break
                    ;;
                *) echo "Invalid selection. Please choose 1 or 2.";;
            esac
        done
    fi
    
    # Validate app selection
    case "$selected_app" in
        face-swapper|coach)
            echo "$selected_app"
            return 0
            ;;
        *)
            echo "Invalid app name: $selected_app. Must be either 'face-swapper' or 'coach'" >&2
            exit 1
            ;;
    esac
}

# Main script
main() {
    # Get and validate app selection
    local app
    app=$(select_app "$1")
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    echo "Preparing to run $app..."
    
    # Setup dependencies
    setup_python
    setup_node "$app"
    
    # Build and deploy
    build_frontend "$app"
    setup_backend_public "$app"
    
    echo "Starting server for $app..."
    cd backend
    python -m uvicorn src.discovita.app:app --reload
}

# Run main with first argument (app name) if provided
main "$1"
