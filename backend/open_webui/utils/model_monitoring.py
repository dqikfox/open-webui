"""
Model Monitoring Middleware
Automatically tracks model performance metrics for all requests
"""
import time
import logging
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

from open_webui.models.model_capabilities import get_metrics

log = logging.getLogger(__name__)


class ModelMetricsMiddleware(BaseHTTPMiddleware):
    """Track model performance for all API calls"""
    
    async def dispatch(self, request: Request, call_next):
        # Only track model-related endpoints
        if not (
            "/api/chat" in request.url.path or 
            "/api/generate" in request.url.path or
            "/ollama/api/chat" in request.url.path or
            "/ollama/api/generate" in request.url.path or
            "/openai/v1/chat/completions" in request.url.path
        ):
            return await call_next(request)
        
        start_time = time.time()
        model_name = None
        tokens = 0
        success = True
        error_msg = None
        
        try:
            # Try to get model from request body
            if request.method == "POST":
                body = await request.body()
                try:
                    import json
                    data = json.loads(body)
                    model_name = data.get("model")
                except:
                    pass
                
                # Recreate request with body
                from starlette.datastructures import Headers
                scope = request.scope
                scope["body"] = body
                request = Request(scope)
            
            response = await call_next(request)
            
            # Extract metrics from response if possible
            if isinstance(response, StreamingResponse):
                # For streaming responses, we'll track without detailed token counts
                pass
            
            time_taken = time.time() - start_time
            
            # Record metric
            if model_name:
                metrics = get_metrics()
                # Estimate tokens if not available (rough estimate: 4 chars per token)
                if tokens == 0:
                    tokens = max(100, int(time_taken * 20))  # Rough estimate
                
                metrics.record_request(
                    model=model_name,
                    tokens=tokens,
                    time_taken=time_taken,
                    success=success,
                    error=error_msg
                )
                
                log.debug(f"📊 Tracked: {model_name} - {tokens} tokens in {time_taken:.2f}s")
            
            return response
            
        except Exception as e:
            success = False
            error_msg = str(e)
            time_taken = time.time() - start_time
            
            # Record error
            if model_name:
                metrics = get_metrics()
                metrics.record_request(
                    model=model_name,
                    tokens=0,
                    time_taken=time_taken,
                    success=False,
                    error=error_msg
                )
            
            raise


async def sync_available_models(app):
    """Sync available models with model router"""
    try:
        from open_webui.models.model_capabilities import get_router
        import requests
        
        log.info("Starting model sync...")
        
        # Get models directly from Ollama
        if not hasattr(app.state, 'config'):
            log.warning("App state not configured, skipping model sync")
            return
            
        if not hasattr(app.state.config, 'OLLAMA_BASE_URLS'):
            log.warning("Ollama not configured, skipping model sync")
            return
        
        model_names = []
        for url in app.state.config.OLLAMA_BASE_URLS:
            log.debug(f"Fetching models from {url}")
            try:
                response = requests.get(f"{url}/api/tags", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    for model in data.get("models", []):
                        model_names.append(model.get("model"))
                    log.debug(f"Found {len(data.get('models', []))} models from {url}")
            except Exception as e:
                log.warning(f"Failed to get models from {url}: {e}")
        
        # Update router
        if model_names:
            router = get_router()
            router.set_available_models(model_names)
            log.info(f"✅ Synced {len(model_names)} models with intelligence router")
        else:
            log.warning("No models found to sync")
        
    except Exception as e:
        log.error(f"Failed to sync models: {e}", exc_info=True)


async def periodic_model_sync(app, interval_seconds: int = 300):
    """Periodically sync available models (every 5 minutes)"""
    import asyncio
    
    while True:
        await asyncio.sleep(interval_seconds)
        await sync_available_models(app)
