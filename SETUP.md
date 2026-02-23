# Enterprise Setup & Installation Guide

## Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

### 3. Start Redis (Required for Enterprise Features)

**Using Docker:**
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

**Using Windows:**
- Download Redis from https://github.com/microsoftarchive/redis/releases
- Or use WSL: `sudo apt install redis-server && redis-server`

### 4. Configure Environment

Backend `.env` file is already configured. Update these values:

```env
# Change in production!
JWT_SECRET=your-super-secret-key-change-in-production
SECRET_KEY=your-256-bit-secret-key-change-in-production

# Update database credentials
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/relaypoint_db
```

### 5. Start Development Environment

```bash
# From root directory
.\dev.ps1
```

Or manually:

```bash
# Start backend
cd backend
uvicorn app.main:app --reload --port 8000

# Start frontend (separate terminal)
cd frontend
npm start
```

### 6. Access the Platform

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Metrics:** http://localhost:8000/metrics
- **Health:** http://localhost:8000/health

## Enterprise Features Testing

### Test Rate Limiting

```bash
# Make rapid requests to see rate limiting in action
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/workflows

# Check rate limit headers
HTTP/1.1 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 45
X-RateLimit-Tier: FREE
```

### Test Caching

```python
from app.core.cache import enterprise_cache

# Set cache
await enterprise_cache.set("test_key", {"data": "value"}, ttl=300)

# Get cache
value = await enterprise_cache.get("test_key")

# Get stats
stats = enterprise_cache.get_stats()
print(f"Cache hit rate: {stats['hit_rate_percent']}%")
```

### Test Authentication

```bash
# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Use token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/workflows
```

### Test Multi-Tenancy

```python
from app.models.tenant import TenantManager, PlanTier

# Create tenant
tenant = await tenant_manager.create_tenant(
    name="Acme Corp",
    slug="acme",
    plan_tier=PlanTier.PROFESSIONAL
)

# Update branding
await tenant_manager.update_branding(
    tenant_id=tenant.id,
    branding_config={
        "primary_color": "#FF5722",
        "logo_url": "https://example.com/logo.png"
    }
)
```

## Troubleshooting

### Redis Connection Issues

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Check connection from Python
python -c "import redis; r=redis.Redis(host='localhost', port=6379); print(r.ping())"
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U username -d relaypoint_db -c "SELECT 1"
```

### Frontend Build Issues

```bash
cd frontend
# Clear cache
rm -rf node_modules
npm cache clean --force
npm install

# Clear Metro bundler cache
npx expo start --clear
```

## Production Deployment

See [ENTERPRISE_DOCUMENTATION.md](../ENTERPRISE_DOCUMENTATION.md) for:
- Kubernetes deployment
- Scaling strategies
- Security best practices
- Monitoring setup

## Support

- Documentation: [ENTERPRISE_DOCUMENTATION.md](../ENTERPRISE_DOCUMENTATION.md)
- Revenue Strategy: [REVENUE_STRATEGY.md](../REVENUE_STRATEGY.md)
- Issues: Create GitHub issue
- Enterprise Support: enterprise@balentinetech.com
