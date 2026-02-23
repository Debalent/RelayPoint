"""
Enterprise Performance Monitoring & Analytics System
Real-time metrics, APM, and business intelligence for RelayPoint
"""

from prometheus_client import Counter, Histogram, Gauge, Info, Summary
from typing import Dict, Any, Optional, List
import time
import structlog
from datetime import datetime, timedelta
from functools import wraps
import asyncio
from contextlib import asynccontextmanager

logger = structlog.get_logger()

# ====================
# INFRASTRUCTURE METRICS
# ====================

# API Performance
api_requests_total = Counter(
    'relaypoint_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status_code', 'tenant_id']
)

api_request_duration = Histogram(
    'relaypoint_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint', 'tenant_id'],
    buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
)

api_errors_total = Counter(
    'relaypoint_api_errors_total',
    'Total API errors',
    ['method', 'endpoint', 'error_type', 'tenant_id']
)

# Database Performance
db_query_duration = Histogram(
    'relaypoint_db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type', 'table', 'tenant_id'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

db_connection_pool = Gauge(
    'relaypoint_db_connection_pool',
    'Database connection pool status',
    ['pool_name', 'state']
)

db_transactions_total = Counter(
    'relaypoint_db_transactions_total',
    'Total database transactions',
    ['operation', 'table', 'status', 'tenant_id']
)

# Cache Performance
cache_hits_total = Counter(
    'relaypoint_cache_hits_total',
    'Total cache hits',
    ['cache_type', 'tenant_id']
)

cache_misses_total = Counter(
    'relaypoint_cache_misses_total',
    'Total cache misses',
    ['cache_type', 'tenant_id']
)

cache_latency = Histogram(
    'relaypoint_cache_latency_seconds',
    'Cache operation latency',
    ['operation', 'cache_type'],
    buckets=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
)

# ====================
# BUSINESS METRICS
# ====================

# User Activity
active_users = Gauge(
    'relaypoint_active_users_total',
    'Number of active users',
    ['tenant_id', 'time_window']
)

user_sessions_total = Counter(
    'relaypoint_user_sessions_total',
    'Total user sessions',
    ['tenant_id', 'session_type']
)

user_actions_total = Counter(
    'relaypoint_user_actions_total',
    'Total user actions',
    ['tenant_id', 'action_type', 'resource_type']
)

# Workflow Metrics
workflows_created_total = Counter(
    'relaypoint_workflows_created_total',
    'Total workflows created',
    ['tenant_id', 'workflow_type']
)

workflows_executed_total = Counter(
    'relaypoint_workflows_executed_total',
    'Total workflow executions',
    ['tenant_id', 'workflow_id', 'status']
)

workflow_execution_duration = Histogram(
    'relaypoint_workflow_execution_duration_seconds',
    'Workflow execution duration',
    ['tenant_id', 'workflow_id'],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600, 1800, 3600]
)

workflow_step_duration = Histogram(
    'relaypoint_workflow_step_duration_seconds',
    'Individual step execution duration',
    ['tenant_id', 'workflow_id', 'step_type'],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

# System Health
system_health_status = Gauge(
    'relaypoint_system_health_status',
    'System health status (1=healthy, 0=unhealthy)',
    ['component', 'tenant_id']
)

background_jobs_total = Counter(
    'relaypoint_background_jobs_total',
    'Total background jobs',
    ['job_type', 'status', 'tenant_id']
)

background_job_duration = Histogram(
    'relaypoint_background_job_duration_seconds',
    'Background job duration',
    ['job_type', 'tenant_id'],
    buckets=[1, 5, 10, 30, 60, 300, 600, 1800, 3600]
)

# Revenue & Business Intelligence
revenue_events = Counter(
    'relaypoint_revenue_events_total',
    'Revenue tracking events',
    ['tenant_id', 'event_type', 'plan_tier']
)

subscription_changes = Counter(
    'relaypoint_subscription_changes_total',
    'Subscription tier changes',
    ['tenant_id', 'from_tier', 'to_tier', 'change_type']
)

mrr_gauge = Gauge(
    'relaypoint_monthly_recurring_revenue',
    'Monthly Recurring Revenue',
    ['tenant_id', 'plan_tier']
)

# ====================
# DECORATORS & UTILITIES
# ====================

def track_api_metrics(endpoint: str):
    """Decorator to automatically track API endpoint metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            method = kwargs.get('request', args[0] if args else None)
            method_name = getattr(method, 'method', 'UNKNOWN') if method else 'UNKNOWN'
            tenant_id = kwargs.get('tenant_id', 'unknown')
            
            start_time = time.time()
            status_code = 200
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = getattr(e, 'status_code', 500)
                error_type = type(e).__name__
                api_errors_total.labels(
                    method=method_name,
                    endpoint=endpoint,
                    error_type=error_type,
                    tenant_id=tenant_id
                ).inc()
                raise
            finally:
                duration = time.time() - start_time
                api_requests_total.labels(
                    method=method_name,
                    endpoint=endpoint,
                    status_code=status_code,
                    tenant_id=tenant_id
                ).inc()
                api_request_duration.labels(
                    method=method_name,
                    endpoint=endpoint,
                    tenant_id=tenant_id
                ).observe(duration)
        
        return wrapper
    return decorator


def track_db_query(query_type: str, table: str):
    """Decorator to track database query performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tenant_id = kwargs.get('tenant_id', 'unknown')
            start_time = time.time()
            status = 'success'
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'error'
                raise
            finally:
                duration = time.time() - start_time
                db_query_duration.labels(
                    query_type=query_type,
                    table=table,
                    tenant_id=tenant_id
                ).observe(duration)
                db_transactions_total.labels(
                    operation=query_type,
                    table=table,
                    status=status,
                    tenant_id=tenant_id
                ).inc()
        
        return wrapper
    return decorator


@asynccontextmanager
async def track_workflow_execution(tenant_id: str, workflow_id: str):
    """Context manager to track workflow execution"""
    start_time = time.time()
    status = 'success'
    
    try:
        yield
    except Exception as e:
        status = 'error'
        raise
    finally:
        duration = time.time() - start_time
        workflows_executed_total.labels(
            tenant_id=tenant_id,
            workflow_id=workflow_id,
            status=status
        ).inc()
        workflow_execution_duration.labels(
            tenant_id=tenant_id,
            workflow_id=workflow_id
        ).observe(duration)


class PerformanceMonitor:
    """Enterprise performance monitoring and analytics"""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self._health_checks: Dict[str, callable] = {}
    
    def register_health_check(self, component: str, check_func: callable):
        """Register a health check function for a component"""
        self._health_checks[component] = check_func
        logger.info("Health check registered", component=component)
    
    async def check_system_health(self, tenant_id: str = "system") -> Dict[str, Any]:
        """Run all health checks and return system status"""
        health_status = {}
        overall_healthy = True
        
        for component, check_func in self._health_checks.items():
            try:
                is_healthy = await check_func() if asyncio.iscoroutinefunction(check_func) else check_func()
                health_status[component] = {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "checked_at": datetime.utcnow().isoformat()
                }
                system_health_status.labels(component=component, tenant_id=tenant_id).set(1 if is_healthy else 0)
                
                if not is_healthy:
                    overall_healthy = False
            except Exception as e:
                logger.error("Health check failed", component=component, error=str(e))
                health_status[component] = {
                    "status": "error",
                    "error": str(e),
                    "checked_at": datetime.utcnow().isoformat()
                }
                system_health_status.labels(component=component, tenant_id=tenant_id).set(0)
                overall_healthy = False
        
        return {
            "overall_status": "healthy" if overall_healthy else "unhealthy",
            "components": health_status,
            "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_performance_report(self, tenant_id: str, time_window: str = "1h") -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        # This would query Prometheus or time-series database
        # For now, return a template structure
        return {
            "tenant_id": tenant_id,
            "time_window": time_window,
            "api_performance": {
                "total_requests": "Query from api_requests_total",
                "avg_response_time": "Query from api_request_duration",
                "error_rate": "Calculate from api_errors_total",
                "p95_latency": "Query p95 from api_request_duration",
                "p99_latency": "Query p99 from api_request_duration",
            },
            "workflow_performance": {
                "total_executions": "Query from workflows_executed_total",
                "success_rate": "Calculate success/total ratio",
                "avg_duration": "Query from workflow_execution_duration",
                "most_used_workflows": "Query top workflows by execution count",
            },
            "user_activity": {
                "active_users": "Query from active_users",
                "total_sessions": "Query from user_sessions_total",
                "top_actions": "Query from user_actions_total",
            },
            "system_health": await self.check_system_health(tenant_id),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def track_user_action(self, tenant_id: str, action_type: str, resource_type: str):
        """Track user action for analytics"""
        user_actions_total.labels(
            tenant_id=tenant_id,
            action_type=action_type,
            resource_type=resource_type
        ).inc()
        
        logger.info(
            "User action tracked",
            tenant_id=tenant_id,
            action_type=action_type,
            resource_type=resource_type
        )
    
    def track_revenue_event(
        self,
        tenant_id: str,
        event_type: str,
        plan_tier: str,
        amount: Optional[float] = None
    ):
        """Track revenue-related events"""
        revenue_events.labels(
            tenant_id=tenant_id,
            event_type=event_type,
            plan_tier=plan_tier
        ).inc()
        
        if amount and event_type == "subscription_payment":
            # Update MRR if it's a subscription payment
            mrr_gauge.labels(tenant_id=tenant_id, plan_tier=plan_tier).set(amount)
        
        logger.info(
            "Revenue event tracked",
            tenant_id=tenant_id,
            event_type=event_type,
            plan_tier=plan_tier,
            amount=amount
        )
    
    def track_subscription_change(
        self,
        tenant_id: str,
        from_tier: str,
        to_tier: str,
        change_type: str
    ):
        """Track subscription tier changes"""
        subscription_changes.labels(
            tenant_id=tenant_id,
            from_tier=from_tier,
            to_tier=to_tier,
            change_type=change_type
        ).inc()
        
        logger.info(
            "Subscription change tracked",
            tenant_id=tenant_id,
            from_tier=from_tier,
            to_tier=to_tier,
            change_type=change_type
        )


# Global performance monitor instance
performance_monitor = PerformanceMonitor()
