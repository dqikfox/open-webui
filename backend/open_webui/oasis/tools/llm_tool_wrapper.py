"""LLM Tool Wrapper - Wraps migrated tools with LLM access"""
from typing import Dict, Any
from ..tool_loader import QasyTool


class LLMToolWrapper(QasyTool):
    """Base wrapper for tools that need LLM access"""
    
    def __init__(self, name: str, description: str, original_tool=None, llm=None):
        super().__init__(name, description)
        self.original_tool = original_tool
        self.llm = llm
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute with LLM access"""
        # Inject LLM into original tool if it has config
        if self.original_tool and hasattr(self.original_tool, 'config'):
            if self.original_tool.config is None:
                self.original_tool.config = {}
            self.original_tool.config['llm'] = self.llm
        
        # Execute original tool
        if self.original_tool and hasattr(self.original_tool, 'execute'):
            result = self.original_tool.execute(kwargs.get('command', ''))
            return {"status": "success", "result": result}
        
        return {"status": "error", "message": "Tool not configured"}


def wrap_tool_with_llm(tool_class, llm):
    """Wrap a tool class with LLM access"""
    try:
        # Instantiate original tool
        original = tool_class()
        
        # Get tool metadata
        name = getattr(tool_class, 'name', tool_class.__name__)
        description = getattr(tool_class, 'description', 'No description')
        
        # Create wrapper
        wrapper = LLMToolWrapper(name, description, original, llm)
        return wrapper
    except Exception as e:
        print(f"Failed to wrap tool {tool_class}: {e}")
        return None
