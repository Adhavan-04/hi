#!/usr/bin/env bash
# Build script for Render deployment

set -e  # Exit on error

echo "Starting build process..."

# Upgrade pip and install build tools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

echo "Build completed successfully!"
