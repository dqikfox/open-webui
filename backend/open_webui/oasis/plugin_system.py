import logging
import importlib.util
from typing import Dict, Any, List, Callable
from pathlib import Path

log = logging.getLogger(__name__)

class PluginSystem:
    """Plugin system for extensibility"""
    
    def __init__(self, plugin_dir: str = "/tmp/oasis_plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(exist_ok=True)
        self.plugins = {}
        self.hooks = {}
        
    def register_plugin(self, name: str, plugin_path: str) -> Dict[str, Any]:
        """Register a plugin"""
        try:
            spec = importlib.util.spec_from_file_location(name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.plugins[name] = {
                "module": module,
                "path": plugin_path,
                "enabled": True,
                "hooks": getattr(module, "HOOKS", [])
            }
            
            # Register hooks
            for hook in self.plugins[name]["hooks"]:
                if hook not in self.hooks:
                    self.hooks[hook] = []
                self.hooks[hook].append(name)
            
            log.info(f"Plugin registered: {name}")
            return {"status": "success", "plugin": name}
        except Exception as e:
            log.exception(e)
            return {"status": "error", "error": str(e)}
    
    def execute_hook(self, hook_name: str, data: Any) -> Any:
        """Execute all plugins registered for a hook"""
        if hook_name not in self.hooks:
            return data
        
        result = data
        for plugin_name in self.hooks[hook_name]:
            plugin = self.plugins[plugin_name]
            if not plugin["enabled"]:
                continue
            
            try:
                hook_func = getattr(plugin["module"], hook_name, None)
                if hook_func:
                    result = hook_func(result)
            except Exception as e:
                log.error(f"Plugin {plugin_name} hook {hook_name} failed: {e}")
        
        return result
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all plugins"""
        return [
            {
                "name": name,
                "enabled": plugin["enabled"],
                "hooks": plugin["hooks"]
            }
            for name, plugin in self.plugins.items()
        ]
    
    def enable_plugin(self, name: str):
        """Enable plugin"""
        if name in self.plugins:
            self.plugins[name]["enabled"] = True
            return {"status": "success"}
        return {"status": "error", "error": "Plugin not found"}
    
    def disable_plugin(self, name: str):
        """Disable plugin"""
        if name in self.plugins:
            self.plugins[name]["enabled"] = False
            return {"status": "success"}
        return {"status": "error", "error": "Plugin not found"}

plugin_system = PluginSystem()
