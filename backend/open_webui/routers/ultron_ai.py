"""
ULTRON AI Router - Multi-AI Provider Integration
Handles routing to OpenAI, Ollama, Together.xyz, and NVIDIA NIM
Integrated into ARMORY backend
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.config import WEBUI_NAME

log = logging.getLogger(__name__)
router = APIRouter()


class AIProvider(BaseModel):
    """AI Provider configuration"""
    name: str
    type: str  # openai, ollama, together, nvidia_nim
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    models: List[str] = Field(default_factory=list)
    enabled: bool = True


class AIRequest(BaseModel):
    """AI request model"""
    provider: Optional[str] = None  # Auto-select if not specified
    model: str
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False


class AIResponse(BaseModel):
    """AI response model"""
    provider: str
    model: str
    content: str
    usage: Optional[Dict[str, int]] = None


class UltronAIRouter:
    """Routes requests to different AI providers"""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self._initialize_default_providers()
    
    def _initialize_default_providers(self):
        """Initialize default AI providers"""
        # Ollama (local)
        self.providers["ollama"] = AIProvider(
            name="Ollama",
            type="ollama",
            base_url="http://ollama:11434",
            models=[],
            enabled=True
        )
        
        # OpenAI
        self.providers["openai"] = AIProvider(
            name="OpenAI",
            type="openai",
            base_url="https://api.openai.com/v1",
            models=["gpt-4", "gpt-3.5-turbo"],
            enabled=False  # Requires API key
        )
        
        # Together.xyz
        self.providers["together"] = AIProvider(
            name="Together",
            type="together",
            base_url="https://api.together.xyz",
            models=[],
            enabled=False
        )
        
        # NVIDIA NIM
        self.providers["nvidia_nim"] = AIProvider(
            name="NVIDIA NIM",
            type="nvidia_nim",
            base_url="https://integrate.api.nvidia.com/v1",
            models=[],
            enabled=False
        )
    
    def select_provider(self, model: str) -> str:
        """Auto-select provider based on model name"""
        # Check if model explicitly specifies provider
        for provider_name, provider in self.providers.items():
            if provider.enabled and model in provider.models:
                return provider_name
        
        # Default to Ollama for local models
        return "ollama"
    
    async def route_request(self, request: AIRequest) -> AIResponse:
        """Route AI request to appropriate provider"""
        provider_name = request.provider or self.select_provider(request.model)
        
        if provider_name not in self.providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provider '{provider_name}' not found"
            )
        
        provider = self.providers[provider_name]
        
        if not provider.enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provider '{provider_name}' is not enabled"
            )
        
        # Route to specific provider implementation
        if provider.type == "ollama":
            return await self._route_ollama(provider, request)
        elif provider.type == "openai":
            return await self._route_openai(provider, request)
        elif provider.type == "together":
            return await self._route_together(provider, request)
        elif provider.type == "nvidia_nim":
            return await self._route_nvidia(provider, request)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unsupported provider type: {provider.type}"
            )
    
    async def _route_ollama(self, provider: AIProvider, request: AIRequest) -> AIResponse:
        """Route to Ollama"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{provider.base_url}/api/chat",
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "stream": request.stream,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return AIResponse(
                provider="ollama",
                model=request.model,
                content=data.get("message", {}).get("content", ""),
                usage=None  # Ollama doesn't provide usage stats
            )
    
    async def _route_openai(self, provider: AIProvider, request: AIRequest) -> AIResponse:
        """Route to OpenAI"""
        import httpx
        
        if not provider.api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OpenAI API key not configured"
            )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{provider.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {provider.api_key}"},
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                    "stream": request.stream
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return AIResponse(
                provider="openai",
                model=request.model,
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage")
            )
    
    async def _route_together(self, provider: AIProvider, request: AIRequest) -> AIResponse:
        """Route to Together.xyz"""
        import httpx
        
        if not provider.api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Together API key not configured"
            )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{provider.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {provider.api_key}"},
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return AIResponse(
                provider="together",
                model=request.model,
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage")
            )
    
    async def _route_nvidia(self, provider: AIProvider, request: AIRequest) -> AIResponse:
        """Route to NVIDIA NIM"""
        import httpx
        
        if not provider.api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NVIDIA API key not configured"
            )
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{provider.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {provider.api_key}"},
                json={
                    "model": request.model,
                    "messages": request.messages,
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return AIResponse(
                provider="nvidia_nim",
                model=request.model,
                content=data["choices"][0]["message"]["content"],
                usage=data.get("usage")
            )


# Initialize router
ai_router = UltronAIRouter()


@router.get("/providers", response_model=Dict[str, AIProvider])
async def get_providers(user=Depends(get_verified_user)):
    """Get all configured AI providers"""
    return ai_router.providers


@router.post("/providers/{provider_name}", response_model=AIProvider)
async def update_provider(
    provider_name: str,
    provider: AIProvider,
    user=Depends(get_admin_user)
):
    """Update AI provider configuration (admin only)"""
    ai_router.providers[provider_name] = provider
    return provider


@router.post("/chat", response_model=AIResponse)
async def chat(request: AIRequest, user=Depends(get_verified_user)):
    """Send chat request to AI provider"""
    try:
        return await ai_router.route_request(request)
    except httpx.HTTPError as e:
        log.error(f"AI request failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI provider error: {str(e)}"
        )
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models")
async def get_models(provider: Optional[str] = None, user=Depends(get_verified_user)):
    """Get available models from providers"""
    if provider:
        if provider not in ai_router.providers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Provider '{provider}' not found"
            )
        return {provider: ai_router.providers[provider].models}
    
    # Return all models from all enabled providers
    models = {}
    for name, prov in ai_router.providers.items():
        if prov.enabled:
            models[name] = prov.models
    return models
