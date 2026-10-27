"""Function Registry - Expose all OASIS functions to Ollama models"""
import logging
from typing import Dict, Any, List, Callable
import inspect

log = logging.getLogger(__name__)


class FunctionRegistry:
    """Registry of all functions available to Ollama models"""
    
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.schemas: Dict[str, Dict] = {}
    
    def register(self, name: str, func: Callable, schema: Dict = None):
        """Register a function"""
        self.functions[name] = func
        
        # Auto-generate schema if not provided
        if not schema:
            schema = self._generate_schema(name, func)
        
        self.schemas[name] = schema
        log.info(f"Registered function: {name}")
    
    def _generate_schema(self, name: str, func: Callable) -> Dict:
        """Auto-generate OpenAI function schema"""
        sig = inspect.signature(func)
        params = {}
        
        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue
            
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
            
            params[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }
        
        return {
            "name": name,
            "description": func.__doc__ or f"Execute {name}",
            "parameters": {
                "type": "object",
                "properties": params,
                "required": list(params.keys())
            }
        }
    
    def get_all_schemas(self) -> List[Dict]:
        """Get all function schemas for Ollama"""
        return list(self.schemas.values())
    
    async def execute(self, name: str, **kwargs) -> Any:
        """Execute a registered function"""
        if name not in self.functions:
            raise ValueError(f"Function not found: {name}")
        
        func = self.functions[name]
        
        # Handle async functions
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        else:
            return func(**kwargs)
    
    def list_functions(self) -> List[str]:
        """List all registered functions"""
        return list(self.functions.keys())


# Global registry
function_registry = FunctionRegistry()


# Auto-register OASIS core functions
def register_qasy_functions(agent, tool_loader, memory):
    """Register all OASIS functions"""
    
    # Agent functions
    async def execute_command(command: str) -> str:
        """Execute a OASIS command"""
        result = await agent.execute_command(command)
        return str(result)
    
    function_registry.register("execute_command", execute_command)
    
    # Tool functions
    def list_tools() -> List[str]:
        """List all available tools"""
        return [tool.name for tool in tool_loader.tools.values()]
    
    function_registry.register("list_tools", list_tools)
    
    async def execute_tool(tool_name: str, params: str = "") -> str:
        """Execute a specific tool"""
        tool = tool_loader.get_tool(tool_name)
        if not tool:
            return f"Tool not found: {tool_name}"
        result = await tool.execute(command=params)
        return str(result)
    
    function_registry.register("execute_tool", execute_tool)
    
    # Memory functions
    def get_memory(count: int = 10) -> List[Dict]:
        """Get recent memory"""
        return memory.get_recent(count)
    
    function_registry.register("get_memory", get_memory)
    
    def store_fact(key: str, value: str) -> str:
        """Store a fact in memory"""
        memory.store_fact(key, value)
        return f"Stored: {key}"
    
    function_registry.register("store_fact", store_fact)
    
    def recall_fact(key: str) -> Any:
        """Recall a fact from memory"""
        return memory.recall_fact(key)
    
    function_registry.register("recall_fact", recall_fact)
    
    # Screenshot function
    async def take_screenshot() -> str:
        """Take a screenshot and analyze it"""
        tool = tool_loader.get_tool("screenshot_analyzer")
        if tool:
            result = await tool.execute(command="screenshot analyze")
            return str(result)
        return "Screenshot tool not available"
    
    function_registry.register("take_screenshot", take_screenshot)
    
    # Web search function
    async def search_web(query: str) -> str:
        """Search the web"""
        tool = tool_loader.get_tool("web_search")
        if tool:
            result = await tool.execute(query=query)
            return str(result)
        return "Web search tool not available"
    
    function_registry.register("search_web", search_web)
    
    # Image generation function
    async def generate_image(prompt: str) -> str:
        """Generate an image"""
        tool = tool_loader.get_tool("image_generation")
        if tool:
            result = await tool.execute(command=f"generate image {prompt}")
            return str(result)
        return "Image generation tool not available"
    
    function_registry.register("generate_image", generate_image)
    
    log.info(f"Registered {len(function_registry.functions)} functions")
