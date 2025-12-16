import logging
import os
import importlib.util
from typing import Dict, Any, List

log = logging.getLogger(__name__)


class QasyTool:
    """Base class for OASIS tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the tool"""
        raise NotImplementedError


class OasisToolLoader:
    """Dynamic tool loader for OASIS"""
    
    def __init__(self, tools_dir: str = None, llm_connector=None):
        self.tools_dir = tools_dir or os.path.join(os.path.dirname(__file__), "tools")
        self.tools: Dict[str, QasyTool] = {}
        self.llm_connector = llm_connector
    
    def load_tools(self) -> Dict[str, QasyTool]:
        """Load all tools from tools directory"""
        if not os.path.exists(self.tools_dir):
            log.warning(f"Tools directory not found: {self.tools_dir}")
            return {}
        
        for filename in os.listdir(self.tools_dir):
            if filename.endswith("_tool.py") and not filename.startswith("__"):
                self._load_tool_file(filename)
        
        log.info(f"Loaded {len(self.tools)} OASIS tools")
        return self.tools
    
    def _load_tool_file(self, filename: str):
        """Load a single tool file"""
        try:
            filepath = os.path.join(self.tools_dir, filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find tool classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, QasyTool) and attr != QasyTool:
                        tool_instance = attr()
                        self.tools[tool_instance.name] = tool_instance
                        log.info(f"Loaded tool: {tool_instance.name}")
        except Exception as e:
            log.error(f"Failed to load tool {filename}: {e}")
    
    def get_tool(self, name: str) -> QasyTool:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]
