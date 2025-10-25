---
description: Repository Information Overview
alwaysApply: true
---

# Repository Information Overview

## Repository Summary
RelayPoint Elite is an enterprise-grade workflow automation platform that enables intelligent automation, real-time collaboration, and advanced analytics. The platform features a visual workflow builder with 50+ components, AI-powered optimization, and enterprise security compliance.

## Repository Structure
- **frontend/**: React-based web application with TypeScript
- **backend/**: FastAPI Python backend service
- **docker/**: Docker configurations for services (PostgreSQL, Redis, Grafana, Prometheus)
- **k8s/**: Kubernetes deployment configurations
- **helm/**: Helm charts for Kubernetes deployment
- **.github/**: CI/CD workflows for automated testing and deployment
- **src/**: Legacy or shared components
- **.zencoder/**: Zencoder configuration and rules
- **dev.ps1/dev.sh**: Development environment setup scripts

### Main Repository Components
- **Frontend**: React 19 application with TypeScript, Material UI, and advanced visualization components
- **Backend**: FastAPI service with PostgreSQL and Redis integration, AI capabilities, and real-time features
- **Infrastructure**: Docker containerization with Kubernetes orchestration
- **CI/CD**: GitHub Actions workflows for testing, building, and deployment
- **Code Quality**: Pre-commit hooks, linting configurations, and automated fixing scripts

## Projects

### Frontend
**Configuration File**: frontend/package.json

#### Language & Runtime
**Language**: JavaScript/TypeScript
**Version**: React 19.1.0
**Build System**: react-scripts (Create React App)
**Package Manager**: npm

#### Dependencies
**Main Dependencies**:
- React 19.1.0 with TypeScript 5.3.3
- Material UI 5.15.0 for UI components
- React Router 6.20.0 for routing
- React Query 3.39.3 for data fetching
- Reactflow 11.10.1 for workflow visualization
- Zustand 4.4.7 for state management
- Socket.io-client 4.7.4 for real-time features
- Framer Motion 10.16.16 for animations
- Monaco Editor 0.45.0 for code editing

**Development Dependencies**:
- ESLint 8.54.0 with TypeScript and React plugins
- Prettier 3.1.0 for code formatting
- Storybook 7.6.3 for component development
- Husky 8.0.3 and lint-staged 15.2.0 for git hooks
- Tailwind CSS 4.1.11 for utility-first styling

#### Build & Installation
```bash
cd frontend
npm install
npm start
```

#### Docker
**Dockerfile**: frontend/Dockerfile
**Image**: Node 18 Alpine (build) + Nginx Alpine (production)
**Configuration**: Multi-stage build with optimized production deployment

#### Testing
**Framework**: Jest with React Testing Library
**Test Location**: frontend/src/**/*.test.js
**Run Command**:
```bash
npm test
```

#### Code Quality
**Linting**: ESLint with TypeScript and React plugins
**Formatting**: Prettier
**Type Checking**: TypeScript with strict mode enabled
**Commands**:
```bash
npm run lint       # Check for linting issues
npm run lint:fix   # Fix linting issues
npm run format     # Format code with Prettier
npm run typecheck  # Run TypeScript type checking
```

### Backend
**Configuration File**: backend/requirements.txt, pyproject.toml

#### Language & Runtime
**Language**: Python
**Version**: 3.11
**Framework**: FastAPI 0.104.1
**Package Manager**: pip

#### Dependencies
**Main Dependencies**:
- FastAPI 0.104.1 for API framework
- SQLAlchemy 2.0.23 for ORM
- Alembic 1.12.1 for database migrations
- OpenAI 1.3.8 and Anthropic 0.7.8 for AI capabilities
- LangChain 0.0.335 for AI orchestration
- Celery 5.3.4 for background task processing
- Redis 5.0.1 for caching and session management
- Prometheus client 0.19.0 for metrics
- Sentry SDK 1.38.0 for error tracking
- Structlog 23.2.0 for structured logging

**Development Dependencies**:
- Pytest 7.4.3 with pytest-asyncio for testing
- Black, isort, ruff for code formatting and linting
- Mypy for static type checking
- Bandit for security scanning

#### Build & Installation
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Docker
**Dockerfile**: backend/Dockerfile
**Image**: Python 3.11 slim
**Configuration**: Multi-stage build with optimized production deployment

#### Testing
**Framework**: pytest with pytest-asyncio
**Test Location**: backend/tests/
**Configuration**: pyproject.toml [tool.pytest.ini_options]
**Run Command**:
```bash
pytest
```

#### Code Quality
**Linting**: Ruff with comprehensive rule sets
**Formatting**: Black with isort
**Type Checking**: Mypy with strict settings
**Security**: Bandit for security scanning
**Configuration**: pyproject.toml

## Infrastructure

### Docker Compose
**Development File**: docker-compose.dev.yml
**Production File**: docker-compose.prod.yml
**Services**:
- PostgreSQL 15 database
- Redis 7 cache
- Backend API service
- Celery worker and beat scheduler
- Frontend application
- Nginx load balancer
- Prometheus monitoring
- Grafana dashboards
- PgAdmin for database management
- Redis Commander for cache inspection
- Mailhog for email testing
- Flower for Celery monitoring

### Kubernetes
**Directory**: k8s/
**Environments**: Production and Staging
**Deployment**: AWS EKS with automated CI/CD pipeline
**Helm Charts**: helm/relaypoint/ for templated deployments

### CI/CD
**Workflow**: .github/workflows/production.yml
**Stages**:
- Backend and frontend testing
- Security scanning
- Docker image building and pushing
- Staging deployment and integration tests
- Production deployment with rollback capability

### Code Quality Tools
**Pre-commit Hooks**: .pre-commit-config.yaml
**Automated Fixing**: fix_code_issues.ps1 (Windows), fix_code_issues.sh (Linux/Mac)
**Linting Configuration**:
- Frontend: .eslintrc.js, .prettierrc
- Backend: pyproject.toml
**Documentation**:
- CODE_QUALITY.md: Code quality standards and tools
- DEVELOPMENT.md: Development workflow and setup