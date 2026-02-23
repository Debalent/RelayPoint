"""
Enterprise Caching Layer with Redis
Multi-level caching strategy for optimal performance
"""

import redis.asyncio as redis
from typing import Any, Optional, Union, List, Dict, Callable
import json
import pickle
import hashlib
from datetime import timedelta
from functools import wraps
import structlog
import asyncio
from contextlib import asynccontextmanager

logger = structlog.get_logger()


class CacheStrategy:
    """Cache invalidation strategies"""
    TTL = "ttl"  # Time-to-live
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    WRITE_THROUGH = "write_through"  # Write to cache and DB simultaneously
    WRITE_BACK = "write_back"  # Write to cache first, DB later


class CacheTier:
    """Cache tier definitions"""
    L1_MEMORY = "l1_memory"  # In-process memory cache
    L2_REDIS = "l2_redis"  # Redis cache
    L3_CDN = "l3_cdn"  # CDN cache (for static assets)


class EnterpriseCache:
    """
    Enterprise-grade caching system with:
    - Multi-level caching (L1 memory + L2 Redis)
    - Intelligent cache warming
    - Automatic cache invalidation
    - Cache stampede prevention
    - Performance analytics
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        default_ttl: int = 3600,
        enable_l1_cache: bool = True,
        l1_max_size: int = 1000
    ):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.default_ttl = default_ttl
        
        # L1 In-memory cache (simple dict for demo, use LRU cache in production)
        self.enable_l1_cache = enable_l1_cache
        self.l1_cache: Dict[str, Any] = {}
        self.l1_max_size = l1_max_size
        
        # Cache statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }
    
    async def connect(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=False  # Handle binary data
            )
            await self.redis_client.ping()
            logger.info("Cache system initialized", redis_url=self.redis_url)
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Cache system disconnected")
    
    def _generate_key(self, key: str, tenant_id: Optional[str] = None, namespace: Optional[str] = None) -> str:
        """Generate namespaced cache key"""
        parts = []
        if namespace:
            parts.append(namespace)
        if tenant_id:
            parts.append(f"tenant:{tenant_id}")
        parts.append(key)
        return ":".join(parts)
    
    async def get(
        self,
        key: str,
        tenant_id: Optional[str] = None,
        namespace: Optional[str] = None,
        use_l1: bool = True
    ) -> Optional[Any]:
        """
        Get value from cache with multi-level lookup
        1. Check L1 (memory) cache
        2. Check L2 (Redis) cache
        3. Return None if not found
        """
        cache_key = self._generate_key(key, tenant_id, namespace)
        
        # L1 Cache lookup
        if use_l1 and self.enable_l1_cache and cache_key in self.l1_cache:
            self.stats["hits"] += 1
            logger.debug("L1 cache hit", key=cache_key)
            return self.l1_cache[cache_key]
        
        # L2 Redis lookup
        try:
            if not self.redis_client:
                await self.connect()
            
            value = await self.redis_client.get(cache_key)
            
            if value is not None:
                self.stats["hits"] += 1
                logger.debug("L2 cache hit", key=cache_key)
                
                # Deserialize
                deserialized = pickle.loads(value)
                
                # Populate L1 cache
                if use_l1 and self.enable_l1_cache:
                    self._set_l1(cache_key, deserialized)
                
                return deserialized
            else:
                self.stats["misses"] += 1
                logger.debug("Cache miss", key=cache_key)
                return None
                
        except Exception as e:
            self.stats["errors"] += 1
            logger.error("Cache get error", key=cache_key, error=str(e))
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tenant_id: Optional[str] = None,
        namespace: Optional[str] = None,
        use_l1: bool = True
    ) -> bool:
        """
        Set value in cache with multi-level write
        """
        cache_key = self._generate_key(key, tenant_id, namespace)
        ttl = ttl or self.default_ttl
        
        try:
            # Serialize value
            serialized = pickle.dumps(value)
            
            # Write to Redis (L2)
            if not self.redis_client:
                await self.connect()
            
            await self.redis_client.setex(cache_key, ttl, serialized)
            
            # Write to L1 cache
            if use_l1 and self.enable_l1_cache:
                self._set_l1(cache_key, value)
            
            self.stats["sets"] += 1
            logger.debug("Cache set", key=cache_key, ttl=ttl)
            return True
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error("Cache set error", key=cache_key, error=str(e))
            return False
    
    async def delete(
        self,
        key: str,
        tenant_id: Optional[str] = None,
        namespace: Optional[str] = None
    ) -> bool:
        """Delete value from all cache levels"""
        cache_key = self._generate_key(key, tenant_id, namespace)
        
        try:
            # Delete from L1
            if cache_key in self.l1_cache:
                del self.l1_cache[cache_key]
            
            # Delete from Redis
            if not self.redis_client:
                await self.connect()
            
            await self.redis_client.delete(cache_key)
            
            self.stats["deletes"] += 1
            logger.debug("Cache delete", key=cache_key)
            return True
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error("Cache delete error", key=cache_key, error=str(e))
            return False
    
    async def invalidate_pattern(
        self,
        pattern: str,
        tenant_id: Optional[str] = None,
        namespace: Optional[str] = None
    ) -> int:
        """Invalidate all keys matching pattern"""
        cache_pattern = self._generate_key(pattern, tenant_id, namespace)
        
        try:
            if not self.redis_client:
                await self.connect()
            
            # Find matching keys
            keys = []
            async for key in self.redis_client.scan_iter(match=cache_pattern):
                keys.append(key)
            
            # Delete matching keys
            if keys:
                deleted = await self.redis_client.delete(*keys)
                
                # Also clear from L1
                for key in keys:
                    if key in self.l1_cache:
                        del self.l1_cache[key]
                
                logger.info("Pattern invalidation", pattern=cache_pattern, count=deleted)
                return deleted
            return 0
            
        except Exception as e:
            logger.error("Pattern invalidation error", pattern=cache_pattern, error=str(e))
            return 0
    
    def _set_l1(self, key: str, value: Any):
        """Set value in L1 cache with simple LRU eviction"""
        if len(self.l1_cache) >= self.l1_max_size:
            # Simple eviction: remove oldest entry
            oldest_key = next(iter(self.l1_cache))
            del self.l1_cache[oldest_key]
        
        self.l1_cache[key] = value
    
    async def get_or_set(
        self,
        key: str,
        factory_func: Callable,
        ttl: Optional[int] = None,
        tenant_id: Optional[str] = None,
        namespace: Optional[str] = None
    ) -> Any:
        """
        Get value from cache or compute and cache it
        Prevents cache stampede with locking
        """
        # Try to get from cache
        value = await self.get(key, tenant_id, namespace)
        
        if value is not None:
            return value
        
        # Acquire lock to prevent stampede
        lock_key = f"lock:{self._generate_key(key, tenant_id, namespace)}"
        
        try:
            if not self.redis_client:
                await self.connect()
            
            # Try to acquire lock
            lock = await self.redis_client.set(lock_key, "1", ex=10, nx=True)
            
            if lock:
                # We got the lock, compute the value
                try:
                    if asyncio.iscoroutinefunction(factory_func):
                        value = await factory_func()
                    else:
                        value = factory_func()
                    
                    # Cache the computed value
                    await self.set(key, value, ttl, tenant_id, namespace)
                    return value
                finally:
                    # Release lock
                    await self.redis_client.delete(lock_key)
            else:
                # Someone else is computing, wait and retry
                await asyncio.sleep(0.1)
                return await self.get_or_set(key, factory_func, ttl, tenant_id, namespace)
                
        except Exception as e:
            logger.error("Get or set error", key=key, error=str(e))
            # Fall back to computing without cache
            if asyncio.iscoroutinefunction(factory_func):
                return await factory_func()
            else:
                return factory_func()
    
    async def warm_cache(
        self,
        warming_functions: List[tuple[str, Callable]],
        tenant_id: Optional[str] = None
    ):
        """Pre-warm cache with commonly accessed data"""
        logger.info("Starting cache warming", functions=len(warming_functions))
        
        for key, factory_func in warming_functions:
            try:
                if asyncio.iscoroutinefunction(factory_func):
                    value = await factory_func()
                else:
                    value = factory_func()
                
                await self.set(key, value, tenant_id=tenant_id)
                logger.debug("Cache warmed", key=key)
                
            except Exception as e:
                logger.error("Cache warming error", key=key, error=str(e))
        
        logger.info("Cache warming completed")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "deletes": self.stats["deletes"],
            "errors": self.stats["errors"],
            "hit_rate_percent": round(hit_rate, 2),
            "l1_cache_size": len(self.l1_cache),
            "l1_max_size": self.l1_max_size
        }
    
    def reset_stats(self):
        """Reset cache statistics"""
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }


# Decorator for automatic caching
def cached(
    ttl: int = 3600,
    namespace: str = "default",
    key_builder: Optional[Callable] = None
):
    """
    Decorator to automatically cache function results
    
    Usage:
        @cached(ttl=300, namespace="users")
        async def get_user(user_id: str):
            return await db.get_user(user_id)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default: hash function name + args
                key_parts = [func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}={v}" for k, v in kwargs.items())
                key_str = ":".join(key_parts)
                cache_key = hashlib.md5(key_str.encode()).hexdigest()
            
            # Get tenant_id from kwargs if available
            tenant_id = kwargs.get("tenant_id")
            
            # Try to get from cache
            from app.core.cache import enterprise_cache  # Avoid circular import
            
            value = await enterprise_cache.get(cache_key, tenant_id=tenant_id, namespace=namespace)
            
            if value is not None:
                return value
            
            # Cache miss, compute value
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Cache the result
            await enterprise_cache.set(cache_key, result, ttl=ttl, tenant_id=tenant_id, namespace=namespace)
            
            return result
        
        return wrapper
    return decorator


# Global cache instance
enterprise_cache = EnterpriseCache()
