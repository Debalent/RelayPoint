"""
Elite AI Service Manager for RelayPoint

This module provides enterprise-grade AI service management with support for
multiple AI providers, intelligent routing, fallback handling, cost optimization,
and advanced workflow automation capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import hashlib
import time

import openai
import anthropic
from google.generativeai import GenerativeModel
import tiktoken

logger = logging.getLogger(__name__)


class AIProvider(str, Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"


class ModelType(str, Enum):
    """AI model types for different use cases."""
    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    IMAGE = "image"
    CODE = "code"
    ANALYSIS = "analysis"


@dataclass
class AIModel:
    """AI model configuration."""
    name: str
    provider: AIProvider
    model_type: ModelType
    max_tokens: int
    cost_per_1k_tokens: float
    rate_limit_rpm: int
    capabilities: List[str]
    context_window: int


@dataclass
class AIRequest:
    """Structured AI request."""
    prompt: str
    model_type: ModelType
    user_id: str
    workflow_id: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    system_prompt: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    priority: int = 5  # 1-10, 10 being highest
    timeout: int = 60


@dataclass
class AIResponse:
    """Structured AI response."""
    content: str
    model_used: str
    provider: AIProvider
    tokens_used: int
    cost: float
    processing_time: float
    timestamp: datetime
    request_id: str
    metadata: Dict[str, Any]


class EliteAIManager:
    """
    Enterprise-grade AI service manager with advanced features.
    
    Features:
    - Multi-provider support with intelligent routing
    - Cost optimization and budget management
    - Rate limiting and queue management
    - Caching for improved performance
    - Fallback handling and error recovery
    - Usage analytics and monitoring
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models: Dict[str, AIModel] = {}
        self.providers: Dict[AIProvider, Any] = {}
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.response_cache: Dict[str, AIResponse] = {}
        self.usage_stats: Dict[str, Any] = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "requests_by_provider": {},
            "requests_by_model": {},
            "average_response_time": 0.0
        }
        self.rate_limiters: Dict[str, List[float]] = {}
        
        self._initialize_providers()
        self._initialize_models()
        
        # Start background workers
        asyncio.create_task(self._request_processor())
        asyncio.create_task(self._cache_cleanup())
    
    def _initialize_providers(self):
        """Initialize AI provider clients."""
        if self.config.get("OPENAI_API_KEY"):
            self.providers[AIProvider.OPENAI] = openai.AsyncOpenAI(
                api_key=self.config["OPENAI_API_KEY"]
            )
        
        if self.config.get("ANTHROPIC_API_KEY"):
            self.providers[AIProvider.ANTHROPIC] = anthropic.AsyncAnthropic(
                api_key=self.config["ANTHROPIC_API_KEY"]
            )
        
        if self.config.get("GOOGLE_AI_API_KEY"):
            import google.generativeai as genai
            genai.configure(api_key=self.config["GOOGLE_AI_API_KEY"])
            self.providers[AIProvider.GOOGLE] = genai
    
    def _initialize_models(self):
        """Initialize available AI models with their configurations."""
        self.models = {
            # OpenAI Models
            "gpt-4-turbo": AIModel(
                name="gpt-4-turbo-preview",
                provider=AIProvider.OPENAI,
                model_type=ModelType.CHAT,
                max_tokens=4096,
                cost_per_1k_tokens=0.03,
                rate_limit_rpm=500,
                capabilities=["chat", "reasoning", "code", "analysis"],
                context_window=128000
            ),
            "gpt-4": AIModel(
                name="gpt-4",
                provider=AIProvider.OPENAI,
                model_type=ModelType.CHAT,
                max_tokens=4096,
                cost_per_1k_tokens=0.06,
                rate_limit_rpm=200,
                capabilities=["chat", "reasoning", "analysis"],
                context_window=8192
            ),
            "gpt-3.5-turbo": AIModel(
                name="gpt-3.5-turbo",
                provider=AIProvider.OPENAI,
                model_type=ModelType.CHAT,
                max_tokens=4096,
                cost_per_1k_tokens=0.002,
                rate_limit_rpm=3500,
                capabilities=["chat", "basic_reasoning"],
                context_window=16385
            ),
            
            # Anthropic Models
            "claude-3-opus": AIModel(
                name="claude-3-opus-20240229",
                provider=AIProvider.ANTHROPIC,
                model_type=ModelType.CHAT,
                max_tokens=4096,
                cost_per_1k_tokens=0.075,
                rate_limit_rpm=50,
                capabilities=["chat", "reasoning", "analysis", "creative"],
                context_window=200000
            ),
            "claude-3-sonnet": AIModel(
                name="claude-3-sonnet-20240229",
                provider=AIProvider.ANTHROPIC,
                model_type=ModelType.CHAT,
                max_tokens=4096,
                cost_per_1k_tokens=0.015,
                rate_limit_rpm=100,
                capabilities=["chat", "reasoning", "analysis"],
                context_window=200000
            ),
            
            # Google Models
            "gemini-pro": AIModel(
                name="gemini-pro",
                provider=AIProvider.GOOGLE,
                model_type=ModelType.CHAT,
                max_tokens=2048,
                cost_per_1k_tokens=0.001,
                rate_limit_rpm=60,
                capabilities=["chat", "reasoning", "multimodal"],
                context_window=32768
            )
        }
    
    async def process_request(self, request: AIRequest) -> AIResponse:
        """
        Process an AI request with intelligent routing and optimization.
        
        Args:
            request: AI request to process
            
        Returns:
            AI response with metadata
        """
        start_time = time.time()
        request_id = self._generate_request_id(request)
        
        # Check cache first
        if cached_response := self._get_cached_response(request):
            logger.info(f"Returning cached response for request {request_id}")
            return cached_response
        
        # Select optimal model
        model = self._select_optimal_model(request)
        if not model:
            raise ValueError("No suitable model available for this request")
        
        # Check rate limits
        if not self._check_rate_limit(model.name):
            # Queue request for later processing
            await self.request_queue.put((request, model))
            return await self._wait_for_queued_response(request_id)
        
        # Process request
        try:
            response = await self._execute_request(request, model)
            response.request_id = request_id
            response.processing_time = time.time() - start_time
            
            # Cache response
            self._cache_response(request, response)
            
            # Update statistics
            self._update_stats(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing AI request {request_id}: {e}")
            
            # Try fallback model
            fallback_model = self._get_fallback_model(model)
            if fallback_model:
                try:
                    response = await self._execute_request(request, fallback_model)
                    response.request_id = request_id
                    response.processing_time = time.time() - start_time
                    
                    self._cache_response(request, response)
                    self._update_stats(response)
                    
                    return response
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
            
            raise e
    
    def _select_optimal_model(self, request: AIRequest) -> Optional[AIModel]:
        """
        Select the optimal model based on request requirements.
        
        Args:
            request: AI request to analyze
            
        Returns:
            Best model for the request or None if no suitable model
        """
        suitable_models = []
        
        for model in self.models.values():
            if model.model_type != request.model_type:
                continue
            
            if model.provider not in self.providers:
                continue
            
            # Check if model can handle the request
            max_tokens = request.max_tokens or model.max_tokens
            if max_tokens > model.max_tokens:
                continue
            
            suitable_models.append(model)
        
        if not suitable_models:
            return None
        
        # Rank models by cost-effectiveness and availability
        def model_score(model: AIModel) -> float:
            cost_factor = 1.0 / (model.cost_per_1k_tokens + 0.001)
            speed_factor = model.rate_limit_rpm / 100.0
            capability_factor = len(model.capabilities) / 10.0
            
            return cost_factor * 0.4 + speed_factor * 0.3 + capability_factor * 0.3
        
        return max(suitable_models, key=model_score)
    
    def _get_fallback_model(self, failed_model: AIModel) -> Optional[AIModel]:
        """Get a fallback model when the primary model fails."""
        fallback_models = [
            model for model in self.models.values()
            if (model.model_type == failed_model.model_type and 
                model.provider != failed_model.provider and
                model.provider in self.providers)
        ]
        
        if not fallback_models:
            return None
        
        # Return the cheapest available fallback
        return min(fallback_models, key=lambda m: m.cost_per_1k_tokens)
    
    async def _execute_request(self, request: AIRequest, model: AIModel) -> AIResponse:
        """Execute the actual AI request with the specified model."""
        start_time = time.time()
        
        if model.provider == AIProvider.OPENAI:
            return await self._execute_openai_request(request, model)
        elif model.provider == AIProvider.ANTHROPIC:
            return await self._execute_anthropic_request(request, model)
        elif model.provider == AIProvider.GOOGLE:
            return await self._execute_google_request(request, model)
        else:
            raise ValueError(f"Unsupported provider: {model.provider}")
    
    async def _execute_openai_request(self, request: AIRequest, model: AIModel) -> AIResponse:
        """Execute OpenAI request."""
        client = self.providers[AIProvider.OPENAI]
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        response = await client.chat.completions.create(
            model=model.name,
            messages=messages,
            max_tokens=request.max_tokens or model.max_tokens,
            temperature=request.temperature or 0.7,
            timeout=request.timeout
        )
        
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        cost = (tokens_used / 1000) * model.cost_per_1k_tokens
        
        return AIResponse(
            content=content,
            model_used=model.name,
            provider=model.provider,
            tokens_used=tokens_used,
            cost=cost,
            processing_time=0.0,  # Will be set by caller
            timestamp=datetime.utcnow(),
            request_id="",  # Will be set by caller
            metadata={"finish_reason": response.choices[0].finish_reason}
        )
    
    async def _execute_anthropic_request(self, request: AIRequest, model: AIModel) -> AIResponse:
        """Execute Anthropic request."""
        client = self.providers[AIProvider.ANTHROPIC]
        
        prompt = request.prompt
        if request.system_prompt:
            prompt = f"System: {request.system_prompt}\n\nUser: {prompt}"
        
        response = await client.messages.create(
            model=model.name,
            max_tokens=request.max_tokens or model.max_tokens,
            temperature=request.temperature or 0.7,
            messages=[{"role": "user", "content": prompt}],
            timeout=request.timeout
        )
        
        content = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        cost = (tokens_used / 1000) * model.cost_per_1k_tokens
        
        return AIResponse(
            content=content,
            model_used=model.name,
            provider=model.provider,
            tokens_used=tokens_used,
            cost=cost,
            processing_time=0.0,
            timestamp=datetime.utcnow(),
            request_id="",
            metadata={"stop_reason": response.stop_reason}
        )
    
    async def _execute_google_request(self, request: AIRequest, model: AIModel) -> AIResponse:
        """Execute Google AI request."""
        genai = self.providers[AIProvider.GOOGLE]
        model_instance = GenerativeModel(model.name)
        
        prompt = request.prompt
        if request.system_prompt:
            prompt = f"{request.system_prompt}\n\n{prompt}"
        
        response = await model_instance.generate_content_async(
            prompt,
            generation_config={
                "max_output_tokens": request.max_tokens or model.max_tokens,
                "temperature": request.temperature or 0.7,
            }
        )
        
        content = response.text
        # Google doesn't provide token usage, so we estimate
        tokens_used = len(content.split()) * 1.3  # Rough estimation
        cost = (tokens_used / 1000) * model.cost_per_1k_tokens
        
        return AIResponse(
            content=content,
            model_used=model.name,
            provider=model.provider,
            tokens_used=int(tokens_used),
            cost=cost,
            processing_time=0.0,
            timestamp=datetime.utcnow(),
            request_id="",
            metadata={"finish_reason": "stop"}
        )
    
    def _generate_request_id(self, request: AIRequest) -> str:
        """Generate a unique request ID based on request content."""
        content = f"{request.prompt}{request.system_prompt or ''}{request.user_id}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _get_cached_response(self, request: AIRequest) -> Optional[AIResponse]:
        """Get cached response if available and valid."""
        cache_key = self._generate_cache_key(request)
        
        if cache_key in self.response_cache:
            cached_response = self.response_cache[cache_key]
            # Check if cache is still valid (1 hour TTL)
            if (datetime.utcnow() - cached_response.timestamp).total_seconds() < 3600:
                return cached_response
            else:
                del self.response_cache[cache_key]
        
        return None
    
    def _cache_response(self, request: AIRequest, response: AIResponse):
        """Cache response for future use."""
        cache_key = self._generate_cache_key(request)
        self.response_cache[cache_key] = response
    
    def _generate_cache_key(self, request: AIRequest) -> str:
        """Generate cache key for request."""
        key_content = f"{request.prompt}{request.system_prompt or ''}{request.model_type.value}"
        return hashlib.sha256(key_content.encode()).hexdigest()
    
    def _check_rate_limit(self, model_name: str) -> bool:
        """Check if request is within rate limits for the model."""
        model = self.models.get(model_name)
        if not model:
            return False
        
        now = time.time()
        window = 60  # 1 minute window
        
        if model_name not in self.rate_limiters:
            self.rate_limiters[model_name] = []
        
        # Clean old entries
        cutoff = now - window
        self.rate_limiters[model_name] = [
            timestamp for timestamp in self.rate_limiters[model_name]
            if timestamp > cutoff
        ]
        
        # Check limit
        if len(self.rate_limiters[model_name]) >= model.rate_limit_rpm:
            return False
        
        # Add current request
        self.rate_limiters[model_name].append(now)
        return True
    
    def _update_stats(self, response: AIResponse):
        """Update usage statistics."""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["total_tokens"] += response.tokens_used
        self.usage_stats["total_cost"] += response.cost
        
        # Update provider stats
        provider = response.provider.value
        if provider not in self.usage_stats["requests_by_provider"]:
            self.usage_stats["requests_by_provider"][provider] = 0
        self.usage_stats["requests_by_provider"][provider] += 1
        
        # Update model stats
        model = response.model_used
        if model not in self.usage_stats["requests_by_model"]:
            self.usage_stats["requests_by_model"][model] = 0
        self.usage_stats["requests_by_model"][model] += 1
        
        # Update average response time
        total_requests = self.usage_stats["total_requests"]
        current_avg = self.usage_stats["average_response_time"]
        self.usage_stats["average_response_time"] = (
            (current_avg * (total_requests - 1) + response.processing_time) / total_requests
        )
    
    async def _request_processor(self):
        """Background task to process queued requests."""
        while True:
            try:
                request, model = await self.request_queue.get()
                
                # Wait for rate limit to reset if needed
                while not self._check_rate_limit(model.name):
                    await asyncio.sleep(1)
                
                # Process the queued request
                response = await self._execute_request(request, model)
                # Store response somewhere accessible by request ID
                
            except Exception as e:
                logger.error(f"Error in request processor: {e}")
    
    async def _cache_cleanup(self):
        """Background task to clean up expired cache entries."""
        while True:
            try:
                await asyncio.sleep(300)  # Clean up every 5 minutes
                
                now = datetime.utcnow()
                expired_keys = []
                
                for cache_key, response in self.response_cache.items():
                    if (now - response.timestamp).total_seconds() > 3600:  # 1 hour TTL
                        expired_keys.append(cache_key)
                
                for key in expired_keys:
                    del self.response_cache[key]
                
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
                
            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")
    
    async def _wait_for_queued_response(self, request_id: str) -> AIResponse:
        """Wait for a queued request to be processed."""
        # This would typically involve checking a response store
        # For now, we'll raise an exception
        raise Exception("Request queued due to rate limits - please retry later")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return self.usage_stats.copy()
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available models."""
        return {
            name: {
                "provider": model.provider.value,
                "type": model.model_type.value,
                "max_tokens": model.max_tokens,
                "cost_per_1k_tokens": model.cost_per_1k_tokens,
                "capabilities": model.capabilities,
                "context_window": model.context_window
            }
            for name, model in self.models.items()
            if model.provider in self.providers
        }


# Global AI manager instance (will be initialized with config)
ai_manager: Optional[EliteAIManager] = None


def initialize_ai_manager(config: Dict[str, Any]) -> EliteAIManager:
    """Initialize the global AI manager with configuration."""
    global ai_manager
    ai_manager = EliteAIManager(config)
    return ai_manager


def get_ai_manager() -> EliteAIManager:
    """Get the global AI manager instance."""
    if ai_manager is None:
        raise RuntimeError("AI manager not initialized. Call initialize_ai_manager first.")
    return ai_manager