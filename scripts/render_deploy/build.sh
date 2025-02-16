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

echo "Building $APP_NAME app..."

echo "Installing Python dependencies..."
cd backend
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
cd ..

echo "Building frontend..."
cd frontend
npm install
npm run install:$APP_NAME
CI=false npm run build:$APP_NAME
cd ..

echo "Setting up backend public directory..."
mkdir -p backend/public
rm -rf backend/public/*
cp -r frontend/apps/$APP_NAME/build/* backend/public/

echo "Build complete!"
