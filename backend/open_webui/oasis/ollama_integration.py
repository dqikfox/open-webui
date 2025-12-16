"""Ollama Integration - Make all functions available to any Ollama model"""
import logging
import requests
from typing import Dict, Any, List, Optional

log = logging.getLogger(__name__)


class OllamaFunctionIntegration:
    """Integrate OASIS functions with Ollama models"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", function_registry=None):
        self.ollama_url = ollama_url
        self.function_registry = function_registry
    
    async def chat_with_functions(
        self,
        model: str,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Chat with Ollama model with function calling support"""
        
        # Get all available functions if not specified
        if functions is None and self.function_registry:
            functions = self.function_registry.get_all_schemas()
        
        # Add functions to system message
        system_message = self._build_system_message(functions)
        
        # Prepend system message
        full_messages = [
            {"role": "system", "content": system_message}
        ] + messages
        
        try:
            # Call Ollama
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": full_messages,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")
                
                # Check if model wants to call a function
                function_call = self._parse_function_call(content)
                
                if function_call and self.function_registry:
                    # Execute function
                    func_result = await self.function_registry.execute(
                        function_call["name"],
                        **function_call["parameters"]
                    )
                    
                    # Add function result to conversation
                    full_messages.append({
                        "role": "assistant",
                        "content": content
                    })
                    full_messages.append({
                        "role": "function",
                        "name": function_call["name"],
                        "content": str(func_result)
                    })
                    
                    # Get final response
                    final_response = requests.post(
                        f"{self.ollama_url}/api/chat",
                        json={
                            "model": model,
                            "messages": full_messages,
                            "stream": False
                        },
                        timeout=60
                    )
                    
                    if final_response.status_code == 200:
                        final_data = final_response.json()
                        return {
                            "response": final_data.get("message", {}).get("content", ""),
                            "function_called": function_call["name"],
                            "function_result": func_result
                        }
                
                return {"response": content}
            
            return {"error": f"Ollama error: {response.status_code}"}
            
        except Exception as e:
            log.exception(e)
            return {"error": str(e)}
    
    def _build_system_message(self, functions: List[Dict]) -> str:
        """Build system message with available functions"""
        if not functions:
            return "You are OASIS, a quality assurance AI assistant."
        
        func_descriptions = []
        for func in functions:
            name = func.get("name", "")
            desc = func.get("description", "")
            params = func.get("parameters", {}).get("properties", {})
            
            param_str = ", ".join([f"{k}: {v.get('type', 'any')}" for k, v in params.items()])
            func_descriptions.append(f"- {name}({param_str}): {desc}")
        
        return f"""You are OASIS, a quality assurance AI assistant with access to the following functions:

{chr(10).join(func_descriptions)}

To call a function, respond with:
FUNCTION_CALL: function_name(param1="value1", param2="value2")

Available functions: {', '.join([f.get('name', '') for f in functions])}"""
    
    def _parse_function_call(self, content: str) -> Optional[Dict]:
        """Parse function call from model response"""
        if "FUNCTION_CALL:" not in content:
            return None
        
        try:
            # Extract function call
            call_str = content.split("FUNCTION_CALL:")[1].strip().split("\n")[0]
            
            # Parse function name and parameters
            func_name = call_str.split("(")[0].strip()
            params_str = call_str.split("(")[1].split(")")[0]
            
            # Parse parameters
            parameters = {}
            if params_str:
                for param in params_str.split(","):
                    key, value = param.split("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    parameters[key] = value
            
            return {
                "name": func_name,
                "parameters": parameters
            }
        except Exception as e:
            log.error(f"Failed to parse function call: {e}")
            return None


# Global instance
ollama_integration = None

def init_ollama_integration(function_registry):
    """Initialize Ollama integration with function registry"""
    global ollama_integration
    ollama_integration = OllamaFunctionIntegration(function_registry=function_registry)
    log.info("Ollama function integration initialized")
    return ollama_integration
