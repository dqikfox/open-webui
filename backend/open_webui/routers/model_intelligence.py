"""
Model Intelligence API Router
Provides intelligent model selection, performance monitoring, and optimization
"""
import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from open_webui.models.model_capabilities import (
    get_metrics,
    get_router,
    get_load_manager,
    ModelCapability
)
from open_webui.utils.auth import get_verified_user, get_admin_user

log = logging.getLogger(__name__)
router = APIRouter()


# Request/Response Models
class ModelRecommendationRequest(BaseModel):
    """Request for model recommendations"""
    query: str = Field(..., description="User query to analyze")
    top_n: int = Field(3, ge=1, le=10, description="Number of recommendations")
    task_type: Optional[str] = Field(None, description="Specific task type (code, chat, reasoning, etc.)")


class ModelRecommendationResponse(BaseModel):
    """Model recommendation response"""
    recommended_models: List[str]
    detected_task: str
    confidence: float


class ModelSelectionRequest(BaseModel):
    """Request for best model selection"""
    task_type: str = Field(..., description="Task type: code, chat, reasoning, vision, embedding, math, creative")
    prefer_fast: bool = Field(False, description="Prefer faster models")
    min_success_rate: float = Field(0.7, ge=0.0, le=1.0)


class ModelPerformanceResponse(BaseModel):
    """Model performance statistics"""
    model: str
    requests: int
    errors: int
    success_rate: float
    avg_response_time: float
    tokens_per_second: float
    last_used: Optional[str]


class RecordMetricRequest(BaseModel):
    """Record a model metric"""
    model: str
    tokens: int
    time_taken: float
    success: bool = True
    error: Optional[str] = None


@router.post("/recommend", response_model=ModelRecommendationResponse)
async def recommend_models(
    request: ModelRecommendationRequest,
    user=Depends(get_verified_user)
):
    """
    Get intelligent model recommendations based on query
    
    Analyzes query content to detect task type and recommends best models
    """
    try:
        router_instance = get_router()
        
        # Get recommendations
        recommendations = router_instance.recommend_models_for_query(
            request.query,
            top_n=request.top_n
        )
        
        # Detect task type
        query_lower = request.query.lower()
        detected_task = "chat"
        
        if any(kw in query_lower for kw in ["code", "function", "program"]):
            detected_task = "code"
        elif any(kw in query_lower for kw in ["solve", "calculate", "math"]):
            detected_task = "math"
        elif any(kw in query_lower for kw in ["think", "reason", "analyze"]):
            detected_task = "reasoning"
        elif any(kw in query_lower for kw in ["image", "picture", "vision"]):
            detected_task = "vision"
        
        return ModelRecommendationResponse(
            recommended_models=recommendations,
            detected_task=detected_task,
            confidence=0.8  # Could be enhanced with ML model
        )
    except Exception as e:
        log.error(f"Error recommending models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/select-best")
async def select_best_model(
    request: ModelSelectionRequest,
    user=Depends(get_verified_user)
):
    """
    Select best model for a specific task type
    
    Uses performance metrics and capabilities to choose optimal model
    """
    try:
        # Map string to enum
        task_map = {
            "code": ModelCapability.CODE,
            "chat": ModelCapability.CHAT,
            "reasoning": ModelCapability.REASONING,
            "vision": ModelCapability.VISION,
            "embedding": ModelCapability.EMBEDDING,
            "math": ModelCapability.MATH,
            "creative": ModelCapability.CREATIVE,
            "function_calling": ModelCapability.FUNCTION_CALLING
        }
        
        task_type = task_map.get(request.task_type.lower())
        if not task_type:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid task type. Must be one of: {', '.join(task_map.keys())}"
            )
        
        router_instance = get_router()
        best_model = router_instance.select_best_model(
            task_type=task_type,
            prefer_fast=request.prefer_fast,
            min_success_rate=request.min_success_rate
        )
        
        if not best_model:
            raise HTTPException(
                status_code=404,
                detail=f"No suitable model found for task: {request.task_type}"
            )
        
        return {
            "model": best_model,
            "task_type": request.task_type,
            "criteria": {
                "prefer_fast": request.prefer_fast,
                "min_success_rate": request.min_success_rate
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error selecting best model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{model}", response_model=ModelPerformanceResponse)
async def get_model_metrics(
    model: str,
    user=Depends(get_verified_user)
):
    """Get performance metrics for a specific model"""
    try:
        metrics = get_metrics()
        stats = metrics.get_model_stats(model)
        
        if not stats or stats.get("requests", 0) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No metrics found for model: {model}"
            )
        
        return ModelPerformanceResponse(
            model=model,
            requests=stats.get("requests", 0),
            errors=stats.get("errors", 0),
            success_rate=stats.get("success_rate", 1.0),
            avg_response_time=stats.get("avg_response_time", 0.0),
            tokens_per_second=stats.get("tokens_per_second", 0.0),
            last_used=stats.get("last_used").isoformat() if stats.get("last_used") else None
        )
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_all_metrics(user=Depends(get_verified_user)):
    """Get performance metrics for all models"""
    try:
        metrics = get_metrics()
        all_stats = metrics.get_all_stats()
        
        # Convert to list format with model name
        result = []
        for model, stats in all_stats.items():
            result.append({
                "model": model,
                **stats,
                "last_used": stats.get("last_used").isoformat() if stats.get("last_used") else None
            })
        
        return {"models": result, "total_models": len(result)}
    except Exception as e:
        log.error(f"Error getting all metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-models")
async def get_top_models(
    limit: int = 10,
    metric: str = "success_rate",
    user=Depends(get_verified_user)
):
    """
    Get top performing models
    
    Args:
        limit: Number of models to return
        metric: Metric to sort by (success_rate, tokens_per_second, requests)
    """
    try:
        valid_metrics = ["success_rate", "tokens_per_second", "requests", "avg_response_time"]
        if metric not in valid_metrics:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid metric. Must be one of: {', '.join(valid_metrics)}"
            )
        
        metrics = get_metrics()
        top_models = metrics.get_top_models(limit=limit, metric=metric)
        
        result = []
        for model, stats in top_models:
            result.append({
                "model": model,
                "rank": len(result) + 1,
                metric: stats.get(metric, 0),
                "requests": stats.get("requests", 0),
                "success_rate": stats.get("success_rate", 1.0)
            })
        
        return {
            "top_models": result,
            "metric": metric,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting top models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/record-metric")
async def record_metric(
    request: RecordMetricRequest,
    user=Depends(get_admin_user)
):
    """
    Record a model performance metric (admin only)
    
    This endpoint is called automatically by the system to track model performance
    """
    try:
        metrics = get_metrics()
        metrics.record_request(
            model=request.model,
            tokens=request.tokens,
            time_taken=request.time_taken,
            success=request.success,
            error=request.error
        )
        
        return {"status": "recorded", "model": request.model}
    except Exception as e:
        log.error(f"Error recording metric: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/errors/recent")
async def get_recent_errors(
    hours: int = 24,
    limit: int = 50,
    user=Depends(get_admin_user)
):
    """Get recent model errors (admin only)"""
    try:
        metrics = get_metrics()
        errors = metrics.get_recent_errors(hours=hours, limit=limit)
        
        # Format errors
        formatted_errors = []
        for error in errors:
            formatted_errors.append({
                "model": error["model"],
                "timestamp": error["timestamp"].isoformat(),
                "tokens": error.get("tokens", 0),
                "time": error.get("time", 0),
                "error": error.get("error", "Unknown error")
            })
        
        return {
            "errors": formatted_errors,
            "total": len(formatted_errors),
            "time_window_hours": hours
        }
    except Exception as e:
        log.error(f"Error getting recent errors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/load-status")
async def get_load_status(user=Depends(get_admin_user)):
    """Get current model loading status (admin only)"""
    try:
        load_manager = get_load_manager()
        
        return {
            "loaded_models": len(load_manager.loaded_models),
            "max_loaded_models": load_manager.max_loaded_models,
            "total_memory_mb": load_manager.get_total_memory_mb(),
            "models": [
                {
                    "name": model,
                    "last_used": last_used.isoformat(),
                    "size_mb": load_manager.model_sizes.get(model, 0)
                }
                for model, last_used in load_manager.loaded_models.items()
            ],
            "models_to_unload": load_manager.get_models_to_unload()
        }
    except Exception as e:
        log.error(f"Error getting load status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def get_model_capabilities_list(user=Depends(get_verified_user)):
    """Get list of all model capabilities and their mappings"""
    try:
        router_instance = get_router()
        
        # Get all capability types
        capabilities = {
            "code": "Code generation and debugging",
            "chat": "General conversation",
            "reasoning": "Logical reasoning and problem solving",
            "vision": "Image understanding and analysis",
            "embedding": "Text embedding generation",
            "math": "Mathematical problem solving",
            "creative": "Creative writing and content generation",
            "function_calling": "Tool/function calling capabilities"
        }
        
        # Get model mapping
        model_mapping = {}
        for model, caps in router_instance.MODEL_CAPABILITIES.items():
            model_mapping[model] = [cap.value for cap in caps]
        
        return {
            "capabilities": capabilities,
            "model_capabilities": model_mapping,
            "available_models": router_instance.available_models
        }
    except Exception as e:
        log.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-available-models")
async def update_available_models(
    models: List[str],
    user=Depends(get_admin_user)
):
    """Update list of available models (admin only)"""
    try:
        router_instance = get_router()
        router_instance.set_available_models(models)
        
        return {
            "status": "updated",
            "model_count": len(models)
        }
    except Exception as e:
        log.error(f"Error updating available models: {e}")
        raise HTTPException(status_code=500, detail=str(e))
