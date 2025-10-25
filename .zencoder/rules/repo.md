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
- **k8s/**: Kubernetes deployment configurations
- **.github/**: CI/CD workflows for automated testing and deployment
- **src/**: Legacy or shared components

### Main Repository Components
- **Frontend**: React 19 application with TypeScript, Material UI, and advanced visualization components
- **Backend**: FastAPI service with PostgreSQL and Redis integration, AI capabilities, and real-time features
- **Infrastructure**: Docker containerization with Kubernetes orchestration
- **CI/CD**: GitHub Actions workflows for testing, building, and deployment

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

### Backend
**Configuration File**: backend/requirements.txt

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
- Celery 5.3.4 for background task processing
- Redis 5.0.1 for caching and session management

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
**Run Command**:
```bash
pytest
```

## Infrastructure

### Docker Compose
**File**: docker-compose.prod.yml
**Services**:
- PostgreSQL 15 database
- Redis 7 cache
- Backend API service
- Celery worker and beat scheduler
- Frontend application
- Nginx load balancer
- Prometheus monitoring
- Grafana dashboards

### Kubernetes
**Directory**: k8s/
**Environments**: Production and Staging
**Deployment**: AWS EKS with automated CI/CD pipeline

### CI/CD
**Workflow**: .github/workflows/production.yml
**Stages**:
- Backend and frontend testing
- Security scanning
- Docker image building and pushing
- Staging deployment and integration tests
- Production deployment with rollback capability