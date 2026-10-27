"""
ULTRON MiniMax Router - Enhanced AI Features
Integrates MiniMax AI for visual generation, creative content, and advanced reasoning
"""

import logging
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import base64

from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.config import WEBUI_NAME

log = logging.getLogger(__name__)
router = APIRouter()


class MinimaxConfig(BaseModel):
    """MiniMax API configuration"""
    api_key: str
    group_id: str
    model: str = "abab6.5s-chat"
    api_base: str = "https://api.minimax.chat/v1"


class CreativeRequest(BaseModel):
    """Creative content generation request"""
    prompt: str
    task: str = "describe"  # describe, enhance, generate
    style: Optional[str] = "tactical"
    temperature: float = 0.9
    top_p: float = 0.95


class ImageGenerationRequest(BaseModel):
    """Image generation request"""
    prompt: str
    style: str = "tactical"
    width: int = 1024
    height: int = 1024
    num_images: int = 1


class MinimaxResponse(BaseModel):
    """MiniMax AI response"""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None


class UltronMinimaxManager:
    """Manages MiniMax AI integration"""
    
    def __init__(self):
        self.config = MinimaxConfig(
            api_key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJBbHBoYSBPbWVnYSIsIlVzZXJOYW1lIjoiQWxwaGEgT21lZ2EiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTkzOTI2NTM5MDI2NTc2Njg0NiIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5MzkyNjUzOTAyNTczNzgyMzgiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJkcWlrc3RAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTUgMTE6MTE6MzMiLCJUb2tlblR5cGUiOjQsImlzcyI6Im1pbmltYXgifQ.JhachFbS3l9nvn7xVJ0LL1y3FEfv5cuoiUF2HDSByNT3gBEHT02ZPqGjNRBzXhHtcKyAHYDpUWDcuadDFsJXcNyHwzOaKuvGJB6v49xHcWBrul_bDFeGHPo607MAsxzXig64j-gLXeWjHt-vEA7GCliGYbjhdGAZWmeLm_psbxV7L53rLCEXhOXrnf8RLaIGOvmB2pryaRlSGnbrNX-wrSBjQFkhoyJTFJCyBQ6z6t4g-_a2k03ADWWwu-UPjjTqT08TEZT35BlhIo5vCphB4GQTH2GH-vPIINe2ZP9D-SByerBwFi3AiTFXt-_iZgNTZ2-H3aXgGUHcOszQSQWJug",
            group_id="1939265390257378238"
        )
        self.tactical_system_prompt = """You are ULTRON, an advanced tactical AI assistant integrated into the ARMORY system.
Your responses should be:
- Precise and actionable
- Military/tactical themed
- Focused on efficiency and results
- Professional with technical depth
Style: Red (#ff0000), Black (#0a0a0a), Gold (#cc9900) - tactical, powerful, elite"""
    
    async def generate_creative_content(self, request: CreativeRequest) -> MinimaxResponse:
        """Generate creative content using MiniMax"""
        import httpx
        
        url = f"{self.config.api_base}/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        # Build system prompt based on task
        if request.style == "tactical":
            system_prompt = self.tactical_system_prompt
        else:
            system_prompt = "You are a creative AI assistant that generates engaging, detailed content."
        
        # Enhance prompt based on task
        if request.task == "enhance":
            enhanced_prompt = f"Enhance and expand this concept with creative details:\n{request.prompt}"
        elif request.task == "generate":
            enhanced_prompt = f"Generate creative content for:\n{request.prompt}"
        else:  # describe
            enhanced_prompt = request.prompt
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": enhanced_prompt}
            ],
            "temperature": request.temperature,
            "top_p": request.top_p
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return MinimaxResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", self.config.model),
                usage=data.get("usage")
            )
    
    async def enhance_chat_response(self, user_message: str, ai_response: str) -> str:
        """Enhance AI responses with tactical styling"""
        request = CreativeRequest(
            prompt=f"Rewrite this AI response in ULTRON's tactical style:\n\nUser: {user_message}\nResponse: {ai_response}",
            task="enhance",
            style="tactical"
        )
        
        result = await self.generate_creative_content(request)
        return result.content
    
    async def generate_visual_description(self, concept: str) -> str:
        """Generate detailed visual descriptions for UI elements"""
        request = CreativeRequest(
            prompt=f"Create a detailed visual description for this ARMORY UI element:\n{concept}\n\nInclude: colors (red/black/gold), shapes, animations, tactical effects",
            task="generate",
            style="tactical",
            temperature=0.95
        )
        
        result = await self.generate_creative_content(request)
        return result.content
    
    async def analyze_and_suggest(self, context: str) -> Dict[str, Any]:
        """Analyze context and provide tactical suggestions"""
        request = CreativeRequest(
            prompt=f"Analyze this situation and provide tactical recommendations:\n{context}\n\nFormat: Brief analysis, 3-5 actionable steps, risk assessment",
            task="generate",
            style="tactical"
        )
        
        result = await self.generate_creative_content(request)
        
        # Parse response into structured format
        content = result.content
        return {
            "analysis": content,
            "model": result.model,
            "style": "tactical",
            "recommendations": self._extract_recommendations(content)
        }
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract actionable recommendations from text"""
        # Simple extraction - look for numbered lists or bullet points
        recommendations = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                recommendations.append(line.lstrip('0123456789.-•').strip())
        return recommendations[:5]  # Top 5
    
    async def generate_code_explanation(self, code: str, language: str = "python") -> str:
        """Generate detailed code explanations"""
        request = CreativeRequest(
            prompt=f"Explain this {language} code in tactical terms (mission objectives, execution flow, potential issues):\n\n```{language}\n{code}\n```",
            task="describe",
            style="tactical"
        )
        
        result = await self.generate_creative_content(request)
        return result.content
    
    async def create_mission_brief(self, task_description: str) -> Dict[str, str]:
        """Convert task into tactical mission brief"""
        request = CreativeRequest(
            prompt=f"Convert this task into a military-style mission brief:\n{task_description}\n\nInclude: Objective, Assets, Timeline, Success Criteria, Risk Level",
            task="generate",
            style="tactical"
        )
        
        result = await self.generate_creative_content(request)
        
        return {
            "mission_brief": result.content,
            "status": "AWAITING DEPLOYMENT",
            "classification": "TACTICAL"
        }


# Initialize manager
minimax_manager = UltronMinimaxManager()


@router.get("/config", response_model=MinimaxConfig)
async def get_config(user=Depends(get_admin_user)):
    """Get MiniMax configuration (admin only)"""
    # Return config without sensitive data
    return MinimaxConfig(
        api_key="***REDACTED***",
        group_id=minimax_manager.config.group_id,
        model=minimax_manager.config.model,
        api_base=minimax_manager.config.api_base
    )


@router.post("/config", response_model=MinimaxConfig)
async def update_config(config: MinimaxConfig, user=Depends(get_admin_user)):
    """Update MiniMax configuration (admin only)"""
    minimax_manager.config = config
    return config


@router.post("/creative", response_model=MinimaxResponse)
async def generate_creative(request: CreativeRequest, user=Depends(get_verified_user)):
    """Generate creative content"""
    try:
        result = await minimax_manager.generate_creative_content(request)
        return result
    except Exception as e:
        log.error(f"Creative generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/enhance-response")
async def enhance_response(
    user_message: str,
    ai_response: str,
    user=Depends(get_verified_user)
):
    """Enhance AI response with tactical styling"""
    try:
        enhanced = await minimax_manager.enhance_chat_response(user_message, ai_response)
        return {"enhanced_response": enhanced}
    except Exception as e:
        log.error(f"Response enhancement failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/visual-description")
async def generate_visual(concept: str, user=Depends(get_verified_user)):
    """Generate visual description for UI elements"""
    try:
        description = await minimax_manager.generate_visual_description(concept)
        return {"description": description, "style": "tactical"}
    except Exception as e:
        log.error(f"Visual description failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/analyze")
async def analyze_context(context: str, user=Depends(get_verified_user)):
    """Analyze context and provide tactical suggestions"""
    try:
        analysis = await minimax_manager.analyze_and_suggest(context)
        return analysis
    except Exception as e:
        log.error(f"Context analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/explain-code")
async def explain_code(
    code: str,
    language: str = "python",
    user=Depends(get_verified_user)
):
    """Generate tactical code explanation"""
    try:
        explanation = await minimax_manager.generate_code_explanation(code, language)
        return {"explanation": explanation, "language": language}
    except Exception as e:
        log.error(f"Code explanation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/mission-brief")
async def create_mission(task: str, user=Depends(get_verified_user)):
    """Convert task into tactical mission brief"""
    try:
        brief = await minimax_manager.create_mission_brief(task)
        return brief
    except Exception as e:
        log.error(f"Mission brief creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/status")
async def get_status(user=Depends(get_verified_user)):
    """Get MiniMax integration status"""
    return {
        "status": "operational",
        "model": minimax_manager.config.model,
        "features": [
            "creative_content",
            "response_enhancement",
            "visual_descriptions",
            "tactical_analysis",
            "code_explanations",
            "mission_briefs"
        ],
        "style": "tactical"
    }
