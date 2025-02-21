#!/bin/bash

check_dependencies() {
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 is required but not installed."
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

setup_python_env() {
    cd backend
    if [ ! -d "venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    python -m pip install --upgrade pip
    cd ..
}
