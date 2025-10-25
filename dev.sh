#!/bin/bash
# RelayPoint Elite - Development Environment Setup Script
# Bash script for Linux/Mac users

# Display banner
echo -e "\033[36m
===============================================
  RelayPoint Elite - Development Environment
===============================================
\033[0m"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "\033[31mError: Docker is not running. Please start Docker and try again.\033[0m"
    exit 1
fi

# Function to display help
show_help() {
    echo -e "\033[33mUsage: ./dev.sh [command]\033[0m"
    echo ""
    echo -e "\033[33mCore Commands:\033[0m"
    echo "  start       Start the development environment"
    echo "  stop        Stop the development environment"
    echo "  restart     Restart the development environment"
    echo "  status      Show status of all services"
    echo "  clean       Remove all development containers and volumes"
    echo ""
    
    echo -e "\033[33mService Commands:\033[0m"
    echo "  logs        Show logs from all services"
    echo "  logs:backend Show logs from backend service"
    echo "  logs:frontend Show logs from frontend service"
    echo "  logs:worker  Show logs from Celery worker"
    echo ""
    
    echo -e "\033[33mDatabase Commands:\033[0m"
    echo "  db          Open PostgreSQL CLI"
    echo "  db:migrate  Run database migrations"
    echo "  db:seed     Seed the database with sample data"
    echo "  redis       Open Redis CLI"
    echo ""
    
    echo -e "\033[33mTesting Commands:\033[0m"
    echo "  test        Run all tests"
    echo "  test:backend Run backend tests"
    echo "  test:frontend Run frontend tests"
    echo "  lint        Run linters"
    echo "  format      Run code formatters"
    echo ""
    
    echo -e "\033[33mMonitoring Commands:\033[0m"
    echo "  monitor     Start monitoring stack (Prometheus, Grafana)"
    echo "  monitor:stop Stop monitoring stack"
    echo ""
    
    echo -e "\033[33mUtility Commands:\033[0m"
    echo "  shell:backend Open shell in backend container"
    echo "  shell:frontend Open shell in frontend container"
    echo "  help        Show this help message"
    echo "  urls        Show all service URLs"
    echo ""
}

# Function to display service URLs
show_service_urls() {
    echo -e "\033[36mService URLs:\033[0m"
    echo -e "\033[32m  Frontend:           http://localhost:3000\033[0m"
    echo -e "\033[32m  Backend API:        http://localhost:8000\033[0m"
    echo -e "\033[32m  API Documentation:  http://localhost:8000/docs\033[0m"
    echo -e "\033[32m  Flower (Celery):    http://localhost:5555\033[0m"
    echo -e "\033[32m  PgAdmin:            http://localhost:5050\033[0m"
    echo -e "\033[32m  Redis Commander:    http://localhost:8081\033[0m"
    echo -e "\033[32m  MailHog:            http://localhost:8025\033[0m"
    
    if docker ps --filter "name=relaypoint_prometheus_dev" --format "{{.Names}}" | grep -q "relaypoint_prometheus_dev"; then
        echo -e "\033[32m  Prometheus:         http://localhost:9090\033[0m"
        echo -e "\033[32m  Grafana:            http://localhost:3001\033[0m"
    fi
}

# Process command line arguments
command=$1
shift

if [ -z "$command" ]; then
    show_help
    exit 0
fi

case $command in
    "start")
        echo -e "\033[32mStarting development environment...\033[0m"
        docker-compose -f docker-compose.dev.yml up -d
        echo -e "\033[32mDevelopment environment started!\033[0m"
        show_service_urls
        ;;
    "stop")
        echo -e "\033[33mStopping development environment...\033[0m"
        docker-compose -f docker-compose.dev.yml down
        echo -e "\033[32mDevelopment environment stopped!\033[0m"
        ;;
    "restart")
        echo -e "\033[33mRestarting development environment...\033[0m"
        docker-compose -f docker-compose.dev.yml down
        docker-compose -f docker-compose.dev.yml up -d
        echo -e "\033[32mDevelopment environment restarted!\033[0m"
        show_service_urls
        ;;
    "status")
        echo -e "\033[36mDevelopment environment status:\033[0m"
        docker-compose -f docker-compose.dev.yml ps
        ;;
    "logs")
        docker-compose -f docker-compose.dev.yml logs -f
        ;;
    "logs:backend")
        docker-compose -f docker-compose.dev.yml logs -f backend
        ;;
    "logs:frontend")
        docker-compose -f docker-compose.dev.yml logs -f frontend
        ;;
    "logs:worker")
        docker-compose -f docker-compose.dev.yml logs -f celery_worker
        ;;
    "db")
        echo -e "\033[36mConnecting to PostgreSQL CLI...\033[0m"
        docker-compose -f docker-compose.dev.yml exec postgres psql -U relaypoint -d relaypoint_elite
        ;;
    "db:migrate")
        echo -e "\033[36mRunning database migrations...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head
        echo -e "\033[32mMigrations completed!\033[0m"
        ;;
    "db:seed")
        echo -e "\033[36mSeeding database with sample data...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend python -m app.scripts.seed_db
        echo -e "\033[32mDatabase seeded!\033[0m"
        ;;
    "redis")
        echo -e "\033[36mConnecting to Redis CLI...\033[0m"
        docker-compose -f docker-compose.dev.yml exec redis redis-cli -a devpassword
        ;;
    "test")
        echo -e "\033[36mRunning all tests...\033[0m"
        
        echo -e "\033[36mRunning backend tests...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend pytest
        
        echo -e "\033[36mRunning frontend tests...\033[0m"
        docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false
        ;;
    "test:backend")
        echo -e "\033[36mRunning backend tests...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend pytest "$@"
        ;;
    "test:frontend")
        echo -e "\033[36mRunning frontend tests...\033[0m"
        docker-compose -f docker-compose.dev.yml exec frontend npm test -- --watchAll=false "$@"
        ;;
    "lint")
        echo -e "\033[36mRunning linters...\033[0m"
        
        echo -e "\033[36mLinting backend code...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend ruff check app tests
        
        echo -e "\033[36mLinting frontend code...\033[0m"
        docker-compose -f docker-compose.dev.yml exec frontend npm run lint
        ;;
    "format")
        echo -e "\033[36mFormatting code...\033[0m"
        
        echo -e "\033[36mFormatting backend code...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend black app tests
        docker-compose -f docker-compose.dev.yml exec backend isort app tests
        
        echo -e "\033[36mFormatting frontend code...\033[0m"
        docker-compose -f docker-compose.dev.yml exec frontend npm run format
        ;;
    "monitor")
        echo -e "\033[32mStarting monitoring stack...\033[0m"
        docker-compose -f docker-compose.dev.yml --profile monitoring up -d
        echo -e "\033[32mMonitoring stack started!\033[0m"
        echo -e "\033[36mPrometheus: http://localhost:9090\033[0m"
        echo -e "\033[36mGrafana: http://localhost:3001\033[0m"
        echo -e "\033[33mDefault Grafana credentials: admin / devpassword\033[0m"
        ;;
    "monitor:stop")
        echo -e "\033[33mStopping monitoring stack...\033[0m"
        docker-compose -f docker-compose.dev.yml --profile monitoring stop prometheus grafana
        echo -e "\033[32mMonitoring stack stopped!\033[0m"
        ;;
    "shell:backend")
        echo -e "\033[36mOpening shell in backend container...\033[0m"
        docker-compose -f docker-compose.dev.yml exec backend /bin/bash
        ;;
    "shell:frontend")
        echo -e "\033[36mOpening shell in frontend container...\033[0m"
        docker-compose -f docker-compose.dev.yml exec frontend /bin/sh
        ;;
    "clean")
        echo -e "\033[33mRemoving all development containers and volumes...\033[0m"
        docker-compose -f docker-compose.dev.yml down -v --remove-orphans
        echo -e "\033[32mDevelopment environment cleaned!\033[0m"
        ;;
    "urls")
        show_service_urls
        ;;
    "help")
        show_help
        ;;
    "backend") # Legacy command for backward compatibility
        docker-compose -f docker-compose.dev.yml logs -f backend
        ;;
    "frontend") # Legacy command for backward compatibility
        docker-compose -f docker-compose.dev.yml logs -f frontend
        ;;
    *)
        echo -e "\033[31mUnknown command: $command\033[0m"
        show_help
        exit 1
        ;;
esac