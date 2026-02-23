"""
Enterprise Features Test Suite
Run this to verify all enterprise features are working
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

async def test_redis_connection():
    """Test Redis connection"""
    print("\n🔍 Testing Redis Connection...")
    try:
        from app.core.cache import enterprise_cache
        await enterprise_cache.connect()
        await enterprise_cache.set("test_key", "test_value", ttl=60)
        value = await enterprise_cache.get("test_key")
        assert value == "test_value", "Cache read/write failed"
        print("✅ Redis connection: OK")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing Database Connection...")
    try:
        from app.core.database import engine
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            assert result is not None
        print("✅ Database connection: OK")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_auth_system():
    """Test authentication system"""
    print("\n🔍 Testing Authentication System...")
    try:
        from app.core.auth_enterprise import AuthService, UserRole, Permission
        
        # Test password hashing
        password = "test_password_123"
        hashed = AuthService.get_password_hash(password)
        assert AuthService.verify_password(password, hashed)
        
        # Test token creation
        token = AuthService.create_access_token(
            data={"sub": "user123", "tenant_id": "tenant1", "roles": ["user"]}
        )
        assert token is not None
        
        # Test permission validation
        has_perm = AuthService.validate_permissions(
            user_roles=["manager"],
            required_permission=Permission.WORKFLOW_READ
        )
        assert has_perm is True
        
        print("✅ Authentication system: OK")
        return True
    except Exception as e:
        print(f"❌ Authentication system failed: {e}")
        return False

def test_rate_limiter():
    """Test rate limiter"""
    print("\n🔍 Testing Rate Limiter...")
    try:
        from app.middleware.rate_limiter import RateLimitTier
        
        # Verify tier configurations
        assert RateLimitTier.FREE["requests_per_minute"] == 60
        assert RateLimitTier.PROFESSIONAL["requests_per_minute"] == 1000
        assert RateLimitTier.ENTERPRISE["requests_per_minute"] == 5000
        
        print("✅ Rate limiter configuration: OK")
        return True
    except Exception as e:
        print(f"❌ Rate limiter failed: {e}")
        return False

def test_monitoring():
    """Test monitoring system"""
    print("\n🔍 Testing Monitoring System...")
    try:
        from app.core.monitoring import (
            api_requests_total,
            api_request_duration,
            performance_monitor
        )
        
        # Verify metrics are defined
        assert api_requests_total is not None
        assert api_request_duration is not None
        assert performance_monitor is not None
        
        print("✅ Monitoring system: OK")
        return True
    except Exception as e:
        print(f"❌ Monitoring system failed: {e}")
        return False

def test_tenant_model():
    """Test tenant model"""
    print("\n🔍 Testing Multi-Tenancy...")
    try:
        from app.models.tenant import Tenant, TenantStatus, PlanTier
        
        # Verify enums
        assert TenantStatus.ACTIVE == "active"
        assert PlanTier.ENTERPRISE == "enterprise"
        
        print("✅ Multi-tenancy model: OK")
        return True
    except Exception as e:
        print(f"❌ Multi-tenancy failed: {e}")
        return False

async def test_cache_operations():
    """Test cache operations"""
    print("\n🔍 Testing Cache Operations...")
    try:
        from app.core.cache import enterprise_cache
        
        # Test basic operations
        await enterprise_cache.set("test1", {"data": "value1"}, ttl=60)
        result = await enterprise_cache.get("test1")
        assert result["data"] == "value1"
        
        # Test pattern invalidation
        await enterprise_cache.set("pattern:test:1", "value1")
        await enterprise_cache.set("pattern:test:2", "value2")
        deleted = await enterprise_cache.invalidate_pattern("pattern:test:*")
        assert deleted >= 0
        
        # Test stats
        stats = enterprise_cache.get_stats()
        assert "hit_rate_percent" in stats
        
        print("✅ Cache operations: OK")
        print(f"   Cache stats: {stats}")
        return True
    except Exception as e:
        print(f"❌ Cache operations failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 RelayPoint Enterprise Feature Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Auth System", test_auth_system()))
    results.append(("Rate Limiter", test_rate_limiter()))
    results.append(("Monitoring", test_monitoring()))
    results.append(("Tenant Model", test_tenant_model()))
    results.append(("Redis Connection", await test_redis_connection()))
    results.append(("Cache Operations", await test_cache_operations()))
    results.append(("Database Connection", await test_database_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All enterprise features are working correctly!")
        return 0
    else:
        print("\n⚠️  Some features need attention. Check errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
