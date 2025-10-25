# RelayPoint Elite - Enhanced Development Environment Setup Script
# PowerShell script for Windows users

# Display banner
Write-Host "
===============================================
  RelayPoint Elite - Development Environment
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

# Function to display help
function Show-Help {
    Write-Host "Usage: ./dev.ps1 [command]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Core Commands:" -ForegroundColor Yellow
    Write-Host "  start       Start the development environment"
    Write-Host "  stop        Stop the development environment"
    Write-Host "  restart     Restart the development environment"
    Write-Host "  status      Show status of all services"
    Write-Host "  clean       Remove all development containers and volumes"
    Write-Host ""
    
    Write-Host "Service Commands:" -ForegroundColor Yellow
    Write-Host "  logs        Show logs from all services"
    Write-Host "  logs:backend Show logs from backend service"
    Write-Host "  logs:frontend Show logs from frontend service"
    Write-Host "  logs:worker  Show logs from Celery worker"
    Write-Host ""
    
    Write-Host "Database Commands:" -ForegroundColor Yellow
    Write-Host "  db          Open PostgreSQL CLI"
    Write-Host "  db:migrate  Run database migrations"
    Write-Host "  db:seed     Seed the database with sample data"
    Write-Host "  redis       Open Redis CLI"
    Write-Host ""
    
    Write-Host "Testing Commands:" -ForegroundColor Yellow
    Write-Host "  test        Run all tests"
    Write-Host "  test:backend Run backend tests"
    Write-Host "  test:frontend Run frontend tests"
    Write-Host "  lint        Run linters"
    Write-Host "  format      Run code formatters"
    Write-Host ""
    
    Write-Host "Monitoring Commands:" -ForegroundColor Yellow
    Write-Host "  monitor     Start monitoring stack (Prometheus, Grafana)"
    Write-Host "  monitor:stop Stop monitoring stack"
    Write-Host ""
    
    Write-Host "Utility Commands:" -ForegroundColor Yellow
    Write-Host "  shell:backend Open shell in backend container"
    Write-Host "  shell:frontend Open shell in frontend container"
    Write-Host "  help        Show this help message"
    Write-Host "  urls        Show all service URLs"
    Write-Host ""
}

# Function to display service URLs
function Show-ServiceUrls {
    Write-Host "Service URLs:" -ForegroundColor Cyan
    Write-Host "  Frontend:           http://localhost:3000" -ForegroundColor Green
    Write-Host "  Backend API:        http://localhost:8000" -ForegroundColor Green
    Write-Host "  API Documentation:  http://localhost:8000/docs" -ForegroundColor Green
    Write-Host "  Flower (Celery):    http://localhost:5555" -ForegroundColor Green
    Write-Host "  PgAdmin:            http://localhost:5050" -ForegroundColor Green
    Write-Host "  Redis Commander:    http://localhost:8081" -ForegroundColor Green
    Write-Host "  MailHog:            http://localhost:8025" -ForegroundColor Green
    
    if (docker ps --filter "name=relaypoint_prometheus_dev" --format "{{.Names}}" | Select-String -Pattern "relaypoint_prometheus_dev") {
        Write-Host "  Prometheus:         http://localhost:9090" -ForegroundColor Green
        Write-Host "  Grafana:            http://localhost:3001" -ForegroundColor Green
    }
}

# Process command line arguments
$command = $args[0]
if (-not $command) {
    Show-Help
    exit 0
}

switch ($command) {
    "start" {
        Write-Host "Starting development environment..." -ForegroundColor Green
        docker-compose -f docker-compose.dev.yml up -d
        Write-Host "Development environment started!" -ForegroundColor Green
        Show-ServiceUrls
    }
    "stop" {
        Write-Host "Stopping development environment..." -ForegroundColor Yellow
        docker-compose -f docker-compose.dev.yml down
        Write-Host "Development environment stopped!" -ForegroundColor Green
    }
    "restart" {
        Write-Host "Restarting development environment..." -ForegroundColor Yellow
        docker-compose -f docker-compose.dev.yml down
        docker-compose -f docker-compose.dev.yml up -d
        Write-Host "Development environment restarted!" -ForegroundColor Green
        Show-ServiceUrls
    }
    "status" {
        Write-Host "Development environment status:" -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml ps
    }
    "logs" {
        docker-compose -f docker-compose.dev.yml logs -f
    }
    "logs:backend" {
        docker-compose -f docker-compose.dev.yml logs -f backend
    }
    "logs:frontend" {
        docker-compose -f docker-compose.dev.yml logs -f frontend
    }
    "logs:worker" {
        docker-compose -f docker-compose.dev.yml logs -f celery_worker
    }
    "db" {
        Write-Host "Connecting to PostgreSQL CLI..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec postgres psql -U relaypoint -d relaypoint_elite
    }
    "db:migrate" {
        Write-Host "Running database migrations..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
        Write-Host "Migrations completed!" -ForegroundColor Green
    }
    "db:seed" {
        Write-Host "Seeding database with sample data..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend python -m app.scripts.seed_db
        Write-Host "Database seeded!" -ForegroundColor Green
    }
    "redis" {
        Write-Host "Connecting to Redis CLI..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec redis redis-cli -a devpassword
    }
    "test" {
        Write-Host "Running all tests..." -ForegroundColor Cyan
        
        Write-Host "Running backend tests..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend pytest
        
        Write-Host "Running frontend tests..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false
    }
    "test:backend" {
        Write-Host "Running backend tests..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend pytest $args[1..$args.Length]
    }
    "test:frontend" {
        Write-Host "Running frontend tests..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false $args[1..$args.Length]
    }
    "lint" {
        Write-Host "Running linters..." -ForegroundColor Cyan
        
        Write-Host "Linting backend code..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend ruff check app tests
        
        Write-Host "Linting frontend code..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec frontend npm run lint
    }
    "format" {
        Write-Host "Formatting code..." -ForegroundColor Cyan
        
        Write-Host "Formatting backend code..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend black app tests
        docker-compose -f docker-compose.dev.yml exec backend isort app tests
        
        Write-Host "Formatting frontend code..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec frontend npm run format
    }
    "monitor" {
        Write-Host "Starting monitoring stack..." -ForegroundColor Green
        docker-compose -f docker-compose.dev.yml --profile monitoring up -d
        Write-Host "Monitoring stack started!" -ForegroundColor Green
        Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Cyan
        Write-Host "Grafana: http://localhost:3001" -ForegroundColor Cyan
        Write-Host "Default Grafana credentials: admin / devpassword" -ForegroundColor Yellow
    }
    "monitor:stop" {
        Write-Host "Stopping monitoring stack..." -ForegroundColor Yellow
        docker-compose -f docker-compose.dev.yml --profile monitoring stop prometheus grafana
        Write-Host "Monitoring stack stopped!" -ForegroundColor Green
    }
    "shell:backend" {
        Write-Host "Opening shell in backend container..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec backend /bin/bash
    }
    "shell:frontend" {
        Write-Host "Opening shell in frontend container..." -ForegroundColor Cyan
        docker-compose -f docker-compose.dev.yml exec frontend /bin/sh
    }
    "clean" {
        Write-Host "Removing all development containers and volumes..." -ForegroundColor Yellow
        docker-compose -f docker-compose.dev.yml down -v --remove-orphans
        Write-Host "Development environment cleaned!" -ForegroundColor Green
    }
    "urls" {
        Show-ServiceUrls
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Unknown command: $command" -ForegroundColor Red
        Show-Help
        exit 1
    }
}