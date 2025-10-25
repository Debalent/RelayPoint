# RelayPoint Elite - Code Quality Fixer Script
# This script automatically fixes common code quality issues across the codebase

Write-Host "
===============================================
  RelayPoint Elite - Code Quality Fixer
===============================================
" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
}
catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Function to display progress
function Show-Progress {
    param (
        [string]$message
    )
    Write-Host "→ $message" -ForegroundColor Yellow
}

# Start the development environment if not already running
Show-Progress "Checking if development environment is running..."
$running = docker ps --filter "name=relaypoint_backend_dev" --format "{{.Names}}" | Select-String -Pattern "relaypoint_backend_dev"
if (-not $running) {
    Show-Progress "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up -d
}

# Fix frontend code issues
Show-Progress "Fixing frontend code issues..."
Write-Host "Running ESLint with auto-fix..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec frontend npm run lint:fix

Write-Host "Running Prettier to format code..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec frontend npm run format

Write-Host "Running TypeScript type checking..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec frontend npm run typecheck

# Fix backend code issues
Show-Progress "Fixing backend code issues..."
Write-Host "Running Black formatter..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec backend black app tests

Write-Host "Running isort to organize imports..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec backend isort app tests

Write-Host "Running Ruff linter with auto-fix..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec backend ruff check --fix app tests

Write-Host "Running MyPy type checker..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec backend mypy app

# Fix Docker files
Show-Progress "Checking Docker files..."
Write-Host "Running Hadolint on Dockerfiles..." -ForegroundColor Cyan
docker run --rm -i hadolint/hadolint < ./backend/Dockerfile
docker run --rm -i hadolint/hadolint < ./frontend/Dockerfile

# Fix Kubernetes manifests
Show-Progress "Checking Kubernetes manifests..."
Write-Host "Running kubeval on Kubernetes manifests..." -ForegroundColor Cyan
docker run --rm -v ${PWD}:/workdir garethr/kubeval k8s/production/*.yaml

# Run tests to verify fixes
Show-Progress "Running tests to verify fixes..."
Write-Host "Running backend tests..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec backend pytest

Write-Host "Running frontend tests..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false

Write-Host "
===============================================
  Code Quality Fixes Completed!
===============================================
" -ForegroundColor Green

Write-Host "The script has attempted to fix all code quality issues." -ForegroundColor Green
Write-Host "Please review the changes and commit them if they look good." -ForegroundColor Green
Write-Host "If there are still issues, you may need to fix some manually." -ForegroundColor Yellow