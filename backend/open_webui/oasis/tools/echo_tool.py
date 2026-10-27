"""Sample OASIS Tool - Echo"""
from typing import Dict, Any
from ..tool_loader import QasyTool


class EchoTool(QasyTool):
    """Simple echo tool for testing"""
    
    def __init__(self):
        super().__init__(
            name="echo",
            description="Echoes back the input message"
        )
    
    async def execute(self, message: str = "", **kwargs) -> Dict[str, Any]:
        """Echo the message"""
        return {
            "status": "success",
            "tool": self.name,
            "message": message,
            "echo": f"OASIS says: {message}"
        }
