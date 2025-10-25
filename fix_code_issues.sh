#!/bin/bash
# RelayPoint Elite - Code Quality Fixer Script
# This script automatically fixes common code quality issues across the codebase

echo -e "\033[36m
===============================================
  RelayPoint Elite - Code Quality Fixer
===============================================
\033[0m"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "\033[31mError: Docker is not running. Please start Docker and try again.\033[0m"
    exit 1
fi

# Function to display progress
show_progress() {
    echo -e "\033[33m→ $1\033[0m"
}

# Start the development environment if not already running
show_progress "Checking if development environment is running..."
if ! docker ps --filter "name=relaypoint_backend_dev" --format "{{.Names}}" | grep -q "relaypoint_backend_dev"; then
    show_progress "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up -d
fi

# Fix frontend code issues
show_progress "Fixing frontend code issues..."
echo -e "\033[36mRunning ESLint with auto-fix...\033[0m"
docker-compose -f docker-compose.dev.yml exec frontend npm run lint:fix

echo -e "\033[36mRunning Prettier to format code...\033[0m"
docker-compose -f docker-compose.dev.yml exec frontend npm run format

echo -e "\033[36mRunning TypeScript type checking...\033[0m"
docker-compose -f docker-compose.dev.yml exec frontend npm run typecheck

# Fix backend code issues
show_progress "Fixing backend code issues..."
echo -e "\033[36mRunning Black formatter...\033[0m"
docker-compose -f docker-compose.dev.yml exec backend black app tests

echo -e "\033[36mRunning isort to organize imports...\033[0m"
docker-compose -f docker-compose.dev.yml exec backend isort app tests

echo -e "\033[36mRunning Ruff linter with auto-fix...\033[0m"
docker-compose -f docker-compose.dev.yml exec backend ruff check --fix app tests

echo -e "\033[36mRunning MyPy type checker...\033[0m"
docker-compose -f docker-compose.dev.yml exec backend mypy app

# Fix Docker files
show_progress "Checking Docker files..."
echo -e "\033[36mRunning Hadolint on Dockerfiles...\033[0m"
docker run --rm -i hadolint/hadolint < ./backend/Dockerfile
docker run --rm -i hadolint/hadolint < ./frontend/Dockerfile

# Fix Kubernetes manifests
show_progress "Checking Kubernetes manifests..."
echo -e "\033[36mRunning kubeval on Kubernetes manifests...\033[0m"
docker run --rm -v $(pwd):/workdir garethr/kubeval k8s/production/*.yaml

# Run tests to verify fixes
show_progress "Running tests to verify fixes..."
echo -e "\033[36mRunning backend tests...\033[0m"
docker-compose -f docker-compose.dev.yml exec backend pytest

echo -e "\033[36mRunning frontend tests...\033[0m"
docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false

echo -e "\033[32m
===============================================
  Code Quality Fixes Completed!
===============================================
\033[0m"

echo -e "\033[32mThe script has attempted to fix all code quality issues.\033[0m"
echo -e "\033[32mPlease review the changes and commit them if they look good.\033[0m"
echo -e "\033[33mIf there are still issues, you may need to fix some manually.\033[0m"