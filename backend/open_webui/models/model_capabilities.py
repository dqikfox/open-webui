"""
OASIS Enhanced Model Capabilities System
Improves model performance, routing, monitoring, and intelligent selection
"""
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import asyncio

log = logging.getLogger(__name__)


class ModelCapability(Enum):
    """Model capability categories"""
    CODE = "code"
    CHAT = "chat"
    REASONING = "reasoning"
    VISION = "vision"
    EMBEDDING = "embedding"
    FUNCTION_CALLING = "function_calling"
    MATH = "math"
    CREATIVE = "creative"


class ModelMetrics:
    """Track model performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "requests": 0,
            "errors": 0,
            "total_tokens": 0,
            "total_time": 0.0,
            "last_used": None,
            "avg_response_time": 0.0,
            "success_rate": 1.0,
            "tokens_per_second": 0.0
        })
        self.request_history: List[Dict] = []
        self.max_history = 1000
        
    def record_request(
        self, 
        model: str, 
        tokens: int, 
        time_taken: float, 
        success: bool = True,
        error: Optional[str] = None
    ):
        """Record a model request"""
        m = self.metrics[model]
        m["requests"] += 1
        m["last_used"] = datetime.now()
        
        if success:
            m["total_tokens"] += tokens
            m["total_time"] += time_taken
            m["avg_response_time"] = m["total_time"] / m["requests"]
            if time_taken > 0:
                m["tokens_per_second"] = tokens / time_taken
        else:
            m["errors"] += 1
            
        m["success_rate"] = (m["requests"] - m["errors"]) / m["requests"]
        
        # Store in history
        self.request_history.append({
            "model": model,
            "timestamp": datetime.now(),
            "tokens": tokens,
            "time": time_taken,
            "success": success,
            "error": error
        })
        
        # Trim history
        if len(self.request_history) > self.max_history:
            self.request_history = self.request_history[-self.max_history:]
    
    def get_model_stats(self, model: str) -> Dict[str, Any]:
        """Get statistics for a specific model"""
        return dict(self.metrics.get(model, {}))
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all models"""
        return dict(self.metrics)
    
    def get_top_models(self, limit: int = 10, metric: str = "success_rate") -> List[tuple]:
        """Get top performing models by metric"""
        sorted_models = sorted(
            self.metrics.items(),
            key=lambda x: x[1].get(metric, 0),
            reverse=True
        )
        return sorted_models[:limit]
    
    def get_recent_errors(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """Get recent errors within time window"""
        cutoff = datetime.now() - timedelta(hours=hours)
        errors = [
            h for h in self.request_history 
            if not h["success"] and h["timestamp"] > cutoff
        ]
        return errors[-limit:]


class ModelRouter:
    """Intelligent model routing and selection"""
    
    # Model capability mapping (can be extended)
    MODEL_CAPABILITIES = {
        # Code-focused models
        "qwen2.5-coder": [ModelCapability.CODE, ModelCapability.REASONING],
        "deepseek-coder": [ModelCapability.CODE, ModelCapability.REASONING],
        "codellama": [ModelCapability.CODE],
        "codegemma": [ModelCapability.CODE],
        
        # Reasoning models
        "deepseek-r1": [ModelCapability.REASONING, ModelCapability.MATH, ModelCapability.CODE],
        "qwen2.5": [ModelCapability.REASONING, ModelCapability.CHAT],
        
        # Chat models
        "llama3.2": [ModelCapability.CHAT, ModelCapability.REASONING],
        "llama3.1": [ModelCapability.CHAT, ModelCapability.REASONING],
        "mistral": [ModelCapability.CHAT],
        "gemma2": [ModelCapability.CHAT],
        
        # Vision models
        "llava": [ModelCapability.VISION, ModelCapability.CHAT],
        "bakllava": [ModelCapability.VISION],
        
        # Embedding models
        "nomic-embed": [ModelCapability.EMBEDDING],
        "all-minilm": [ModelCapability.EMBEDDING],
        "mxbai-embed": [ModelCapability.EMBEDDING],
        
        # Creative models
        "nous-hermes": [ModelCapability.CREATIVE, ModelCapability.CHAT],
        "neural-chat": [ModelCapability.CREATIVE, ModelCapability.CHAT],
    }
    
    def __init__(self, metrics: ModelMetrics):
        self.metrics = metrics
        self.available_models: List[str] = []
        
    def set_available_models(self, models: List[str]):
        """Update list of available models"""
        self.available_models = models
        log.info(f"Model router updated with {len(models)} available models")
    
    def get_model_capabilities(self, model: str) -> List[ModelCapability]:
        """Get capabilities for a model"""
        # Check exact match
        if model in self.MODEL_CAPABILITIES:
            return self.MODEL_CAPABILITIES[model]
        
        # Check partial match (e.g., "qwen2.5-coder:7b" matches "qwen2.5-coder")
        for pattern, capabilities in self.MODEL_CAPABILITIES.items():
            if pattern in model.lower():
                return capabilities
        
        # Default to chat
        return [ModelCapability.CHAT]
    
    def select_best_model(
        self, 
        task_type: ModelCapability,
        available_models: Optional[List[str]] = None,
        prefer_fast: bool = False,
        min_success_rate: float = 0.7
    ) -> Optional[str]:
        """
        Intelligently select best model for a task
        
        Args:
            task_type: Type of task (code, chat, reasoning, etc.)
            available_models: List of available models (uses self.available_models if None)
            prefer_fast: Prefer faster models over accuracy
            min_success_rate: Minimum acceptable success rate
            
        Returns:
            Best model name or None
        """
        models = available_models or self.available_models
        
        # Filter models by capability
        capable_models = [
            m for m in models 
            if task_type in self.get_model_capabilities(m)
        ]
        
        if not capable_models:
            log.warning(f"No models found with capability {task_type.value}")
            return None
        
        # Score models
        scores = []
        for model in capable_models:
            stats = self.metrics.get_model_stats(model)
            
            # Skip models with low success rate
            success_rate = stats.get("success_rate", 1.0)
            if success_rate < min_success_rate:
                continue
            
            # Calculate score
            if prefer_fast:
                # Prioritize speed
                score = stats.get("tokens_per_second", 0) * success_rate
            else:
                # Balance speed and reliability
                tps = stats.get("tokens_per_second", 10)
                score = success_rate * (1 + min(tps / 50, 1))
            
            scores.append((model, score, stats))
        
        if not scores:
            # No models with metrics, return first capable model
            return capable_models[0]
        
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        best_model = scores[0][0]
        
        log.info(f"Selected {best_model} for {task_type.value} (score: {scores[0][1]:.2f})")
        return best_model
    
    def recommend_models_for_query(self, query: str, top_n: int = 3) -> List[str]:
        """Recommend models based on query content"""
        query_lower = query.lower()
        
        # Detect task type from query
        task_type = ModelCapability.CHAT  # default
        
        if any(kw in query_lower for kw in ["code", "function", "program", "script", "debug"]):
            task_type = ModelCapability.CODE
        elif any(kw in query_lower for kw in ["solve", "calculate", "math", "equation"]):
            task_type = ModelCapability.MATH
        elif any(kw in query_lower for kw in ["think", "reason", "analyze", "explain"]):
            task_type = ModelCapability.REASONING
        elif any(kw in query_lower for kw in ["image", "picture", "photo", "vision"]):
            task_type = ModelCapability.VISION
        elif any(kw in query_lower for kw in ["story", "poem", "creative", "write"]):
            task_type = ModelCapability.CREATIVE
        
        # Get capable models
        capable_models = [
            m for m in self.available_models
            if task_type in self.get_model_capabilities(m)
        ]
        
        if not capable_models:
            return self.available_models[:top_n]
        
        # Sort by performance
        scored = []
        for model in capable_models:
            stats = self.metrics.get_model_stats(model)
            score = stats.get("success_rate", 1.0)
            scored.append((model, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in scored[:top_n]]


class ModelLoadManager:
    """Manage model loading/unloading for memory optimization"""
    
    def __init__(self, keep_alive_minutes: int = 30):
        self.loaded_models: Dict[str, datetime] = {}
        self.keep_alive_minutes = keep_alive_minutes
        self.model_sizes: Dict[str, int] = {}  # In MB
        self.max_loaded_models = 5
        
    def mark_loaded(self, model: str, size_mb: int = 0):
        """Mark model as loaded"""
        self.loaded_models[model] = datetime.now()
        if size_mb > 0:
            self.model_sizes[model] = size_mb
        log.info(f"✅ Model loaded: {model}")
    
    def mark_used(self, model: str):
        """Update last used time"""
        if model in self.loaded_models:
            self.loaded_models[model] = datetime.now()
    
    def get_models_to_unload(self) -> List[str]:
        """Get list of models that should be unloaded"""
        cutoff = datetime.now() - timedelta(minutes=self.keep_alive_minutes)
        to_unload = [
            model for model, last_used in self.loaded_models.items()
            if last_used < cutoff
        ]
        return to_unload
    
    def should_preload(self, model: str) -> bool:
        """Check if model should be preloaded"""
        if model in self.loaded_models:
            return False
        return len(self.loaded_models) < self.max_loaded_models
    
    def get_loaded_count(self) -> int:
        """Get number of loaded models"""
        return len(self.loaded_models)
    
    def get_total_memory_mb(self) -> int:
        """Get total memory used by loaded models"""
        return sum(self.model_sizes.values())


# Global instances
_metrics = ModelMetrics()
_router = ModelRouter(_metrics)
_load_manager = ModelLoadManager()


def get_metrics() -> ModelMetrics:
    """Get global metrics instance"""
    return _metrics


def get_router() -> ModelRouter:
    """Get global router instance"""
    return _router


def get_load_manager() -> ModelLoadManager:
    """Get global load manager instance"""
    return _load_manager
