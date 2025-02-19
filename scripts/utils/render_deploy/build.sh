#!/bin/bash
set -e

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
CI=false npm run build
cd ..

echo "Setting up backend public directory..."
mkdir -p backend/public
rm -rf backend/public/*
cp -r frontend/build/* backend/public/

echo "Build complete!"
