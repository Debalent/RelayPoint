# RelayPoint Elite Enhanced Development Guide

This guide provides comprehensive instructions for setting up and working with the RelayPoint Elite development environment.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) (latest version)
- [Git](https://git-scm.com/downloads) (latest version)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended)
- [Node.js](https://nodejs.org/) v18+ (for local development outside Docker)
- [Python](https://www.python.org/downloads/) 3.11+ (for local development outside Docker)

## Quick Start

We provide convenient scripts to manage the development environment:

### Windows

```powershell
# Start the development environment
.\dev.ps1 start

# View logs
.\dev.ps1 logs

# Run tests
.\dev.ps1 test

# Stop the environment
.\dev.ps1 stop

# For more commands
.\dev.ps1 help
```

### Linux/Mac

```bash
# Make the script executable
chmod +x ./dev.sh

# Start the development environment
./dev.sh start

# View logs
./dev.sh logs

# Run tests
./dev.sh test

# Stop the environment
./dev.sh stop

# For more commands
./dev.sh help
```

## Enhanced Development Environment

The development environment uses Docker Compose to run all necessary services with hot reloading, debugging support, and developer tools:

### Core Services

- **Frontend**: React application running on http://localhost:3000
- **Backend**: FastAPI service running on http://localhost:8000
- **API Documentation**: Available at http://localhost:8000/docs
- **PostgreSQL**: Database running on localhost:5432
- **Redis**: Cache running on localhost:6379
- **Celery**: Background task processing
- **Flower**: Celery monitoring dashboard on http://localhost:5555

### Developer Tools

- **PgAdmin**: PostgreSQL management interface on http://localhost:5050
- **Redis Commander**: Redis management interface on http://localhost:8081
- **MailHog**: Email testing service on http://localhost:8025

### Monitoring Stack (Optional)

Start the monitoring stack with:

```bash
# Windows
.\dev.ps1 monitor

# Linux/Mac
./dev.sh monitor
```

- **Prometheus**: Metrics collection on http://localhost:9090
- **Grafana**: Metrics visualization on http://localhost:3001 (admin/devpassword)

## Development Workflow

### Common Tasks

```bash
# View all available services
./dev.sh urls

# Check service status
./dev.sh status

# Run database migrations
./dev.sh db:migrate

# Seed the database with sample data
./dev.sh db:seed

# Run linters
./dev.sh lint

# Format code
./dev.sh format

# Open a shell in the backend container
./dev.sh shell:backend

# Open a shell in the frontend container
./dev.sh shell:frontend
```

### Testing

```bash
# Run all tests
./dev.sh test

# Run only backend tests
./dev.sh test:backend

# Run only frontend tests
./dev.sh test:frontend

# Run specific backend tests
./dev.sh test:backend app/tests/test_workflows.py
```

## Code Quality Tools

We use several tools to maintain code quality:

### Pre-commit Hooks

Install pre-commit hooks to automatically format and lint code before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install
```

### Backend (Python)

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **pytest**: Testing framework
- **ruff**: Fast linter
- **bandit**: Security scanning

### Frontend (TypeScript/JavaScript)

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Static type checking
- **Jest**: Testing framework

## Debugging

### Backend Debugging

The development environment includes Python's debugpy, which allows you to attach a debugger:

1. In VS Code, create a launch configuration in `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/backend",
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
```

2. Start the debugger in the container:

```bash
# In the backend container
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. Attach the VS Code debugger (F5)

### Frontend Debugging

For the frontend, you can use Chrome DevTools or the VS Code debugger:

1. In VS Code, add to your `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome against localhost",
            "url": "http://localhost:3000",
            "webRoot": "${workspaceFolder}/frontend"
        }
    ]
}
```

2. Start debugging in VS Code (F5)

## Working with the Database

### Accessing PostgreSQL

```bash
# Using the dev script
./dev.sh db

# Or use PgAdmin at http://localhost:5050
# Login with: admin@relaypoint.ai / devpassword
```

### Running Migrations

```bash
# Generate a new migration
./dev.sh shell:backend
alembic revision --autogenerate -m "description"

# Apply migrations
./dev.sh db:migrate
```

## Email Testing

The development environment includes MailHog for testing emails:

1. Send emails from your application to `smtp://mailhog:1025`
2. View sent emails in the MailHog web interface at http://localhost:8025

## Monitoring

The optional monitoring stack provides:

1. **Prometheus** for metrics collection
2. **Grafana** for visualization

Access Grafana at http://localhost:3001 (admin/devpassword)

## Troubleshooting

### Common Issues

1. **Port conflicts**: If you have services already using ports 3000, 8000, 5432, or 6379, you'll need to modify the `docker-compose.dev.yml` file to use different ports.

2. **Docker memory issues**: Ensure Docker has enough memory allocated (at least 4GB recommended).

3. **Hot reload not working**: Make sure the volume mounts in `docker-compose.dev.yml` are correct for your operating system.

### Resetting the Environment

If you encounter persistent issues, you can reset the development environment:

```bash
# Remove all containers and volumes
./dev.sh clean

# Start fresh
./dev.sh start
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for our contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.