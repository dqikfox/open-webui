"""LLM Connector - Connect all OASIS tools to Ollama/LLM"""
import logging
import requests
from typing import Dict, Any, Optional, List

log = logging.getLogger(__name__)


class LLMConnector:
    """Connect OASIS tools to local Ollama or any LLM"""
    
    def __init__(self, ollama_url: str = "http://ollama:11434"):
        self.ollama_url = ollama_url
        self.default_model = "llama3.1"
        self.available_models = []
        self._check_connection()
    
    def _check_connection(self):
        """Check Ollama connection and get available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [m['name'] for m in data.get('models', [])]
                log.info(f"✅ Connected to Ollama: {len(self.available_models)} models available")
            else:
                log.warning("⚠️ Ollama not responding")
        except Exception as e:
            log.error(f"❌ Ollama connection failed: {e}")
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        context: Optional[List] = None
    ) -> str:
        """Generate response from LLM"""
        model = model or self.default_model
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            if system:
                payload["system"] = system
            
            if context:
                payload["context"] = context
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            log.error(f"LLM generation failed: {e}")
            return f"Error: {str(e)}"
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None
    ) -> str:
        """Chat with LLM"""
        model = model or self.default_model
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            log.error(f"LLM chat failed: {e}")
            return f"Error: {str(e)}"
    
    def get_models(self) -> List[str]:
        """Get available models"""
        return self.available_models
    
    def set_default_model(self, model: str):
        """Set default model"""
        if model in self.available_models:
            self.default_model = model
            log.info(f"Default model set to: {model}")
        else:
            log.warning(f"Model {model} not available")


# Global instance
llm_connector = LLMConnector()
