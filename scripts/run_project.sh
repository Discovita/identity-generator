#!/bin/bash
set -e

# Source utility scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils/dependency_checker.sh"
source "$SCRIPT_DIR/utils/app_selector.sh"
source "$SCRIPT_DIR/utils/run_modes.sh"

# Default to development mode
PROD_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            PROD_MODE=true
            shift
            ;;
        *)
            break
            ;;
    esac
done

# Check basic dependencies first
check_dependencies

# Get app name from remaining args
if [ -n "$1" ]; then
    APP_NAME="$1"
    # Validate app name
    if [ "$APP_NAME" != "face-swapper" ] && [ "$APP_NAME" != "coach" ]; then
        echo "Error: Invalid app name. Must be either 'face-swapper' or 'coach'"
        exit 1
    fi
else
    # Interactive selection
    get_app_name
    read choice
    case $choice in
        1) APP_NAME="face-swapper" ;;
        2) APP_NAME="coach" ;;
        *) echo "Error: Invalid choice. Please enter 1 or 2."; exit 1 ;;
    esac
fi

echo "Starting $APP_NAME app in $([ "$PROD_MODE" = true ] && echo 'production' || echo 'development') mode..."

# Setup Python environment
setup_python_env

# Install dependencies
install_dependencies "$APP_NAME"

# Run in selected mode
if [ "$PROD_MODE" = true ]; then
    run_prod_mode "$APP_NAME"
else
    run_dev_mode "$APP_NAME"
fi
