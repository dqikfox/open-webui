from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging

from open_webui.oasis import OasisAgent, OasisToolLoader, OasisMemory
from open_webui.oasis.nemo_agent import nemo_toolkit
from open_webui.oasis.nvidia_3d_gen import nvidia_3d_gen
from open_webui.oasis.autogpt_integration import autogpt_code
from open_webui.oasis.llm_connector import llm_connector
from open_webui.oasis.function_registry import function_registry, register_qasy_functions
from open_webui.oasis.ollama_integration import init_ollama_integration
from open_webui.oasis.autogen_studio import AutoGenStudio
from open_webui.oasis.autogen_scheduler import AutoGenScheduler
from open_webui.oasis.agent_orchestrator import AgentOrchestrator
from open_webui.oasis.nemotron_loader import nemotron_loader
from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)
router = APIRouter()

# Initialize OASIS components
oasis_agent = OasisAgent()
oasis_agent.llm = llm_connector
oasis_tool_loader = OasisToolLoader(llm_connector=llm_connector)
oasis_memory = OasisMemory()

oasis_tool_loader.load_tools()
for tool_name, tool in oasis_tool_loader.tools.items():
    oasis_agent.register_tool(tool_name, tool)

register_qasy_functions(oasis_agent, oasis_tool_loader, oasis_memory)
ollama_integration = init_ollama_integration(function_registry)

autogen_studio = AutoGenStudio()
autogen_scheduler = AutoGenScheduler(autogen_studio, interval_minutes=60)
agent_orchestrator = AgentOrchestrator(autogen_studio, oasis_agent, oasis_tool_loader)

log.info(f"✅ OASIS initialized: {len(function_registry.functions)} functions")


class OasisCommandRequest(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = None


@router.post("/execute")
async def execute_command(request: Request, cmd: OasisCommandRequest, user=Depends(get_verified_user)):
    result = await oasis_agent.execute_command(cmd.command, cmd.context)
    oasis_memory.add_message("user", cmd.command)
    oasis_memory.add_message("oasis", str(result))
    return result


@router.get("/tools")
async def list_tools(request: Request, user=Depends(get_verified_user)):
    return {"tools": oasis_tool_loader.list_tools()}


@router.get("/status")
async def get_status(request: Request, user=Depends(get_verified_user)):
    return {"agent": oasis_agent.get_status(), "memory": oasis_memory.get_stats()}


# Analytics
@router.get("/analytics/dashboard")
async def analytics_dashboard(request: Request, user=Depends(get_verified_user)):
    from open_webui.oasis.analytics_engine import analytics_engine
    return analytics_engine.get_dashboard_stats()


@router.get("/analytics/export")
async def export_analytics(request: Request, format: str = "json", user=Depends(get_verified_user)):
    from open_webui.oasis.analytics_engine import analytics_engine
    return {"report": analytics_engine.export_report(format)}


# Plugins
@router.post("/plugins/register")
async def register_plugin(request: Request, data: dict, user=Depends(get_verified_user)):
    from open_webui.oasis.plugin_system import plugin_system
    return plugin_system.register_plugin(data["name"], data["path"])


@router.get("/plugins/list")
async def list_plugins(request: Request, user=Depends(get_verified_user)):
    from open_webui.oasis.plugin_system import plugin_system
    return {"plugins": plugin_system.list_plugins()}


# Context
@router.post("/context/add")
async def add_context(request: Request, data: dict, user=Depends(get_verified_user)):
    from open_webui.oasis.context_manager import context_manager
    context_manager.add_context(data["session_id"], data["message"])
    return {"status": "success"}


@router.get("/context/{session_id}")
async def get_context(request: Request, session_id: str, user=Depends(get_verified_user)):
    from open_webui.oasis.context_manager import context_manager
    return {"context": context_manager.get_context(session_id)}


# Workflows
@router.post("/workflow/execute")
async def execute_workflow(request: Request, data: dict, user=Depends(get_verified_user)):
    return await agent_orchestrator.execute_workflow(data["workflow_type"], data["params"])


@router.get("/workflow/list")
async def list_workflows(request: Request, user=Depends(get_verified_user)):
    return {"workflows": agent_orchestrator.list_workflows()}


# AutoGen
@router.post("/autogen/suggest")
async def autogen_suggest(request: Request, data: dict, user=Depends(get_verified_user)):
    suggestions = await autogen_studio.suggest_enhancements(data.get("context", "OASIS"))
    return {"status": "success", "suggestions": suggestions}


# CUDA
@router.get("/cuda/status")
async def cuda_status(request: Request, user=Depends(get_verified_user)):
    from open_webui.utils.cuda_utils import cuda_manager
    return cuda_manager.get_status()


# Nemotron Model
class NemotronLoadRequest(BaseModel):
    model_name: Optional[str] = None
    dtype: str = "auto"
    device_map: str = "auto"


class NemotronGenerateRequest(BaseModel):
    prompt: str
    max_length: int = 512
    temperature: float = 0.7
    top_p: float = 0.9


class NemotronEmbeddingRequest(BaseModel):
    text: str


@router.post("/nemotron/load")
async def load_nemotron_model(request: Request, data: NemotronLoadRequest, user=Depends(get_verified_user)):
    """Load NVIDIA Nemotron-Nano-9B-v2 model"""
    result = nemotron_loader.load_model(
        model_name=data.model_name,
        dtype=data.dtype,
        device_map=data.device_map
    )
    return result


@router.get("/nemotron/status")
async def nemotron_status(request: Request, user=Depends(get_verified_user)):
    """Get Nemotron model status"""
    return nemotron_loader.get_status()


@router.post("/nemotron/generate")
async def generate_with_nemotron(request: Request, data: NemotronGenerateRequest, user=Depends(get_verified_user)):
    """Generate text using Nemotron model"""
    result = nemotron_loader.generate(
        prompt=data.prompt,
        max_length=data.max_length,
        temperature=data.temperature,
        top_p=data.top_p
    )
    return result


@router.post("/nemotron/embeddings")
async def get_nemotron_embeddings(request: Request, data: NemotronEmbeddingRequest, user=Depends(get_verified_user)):
    """Get embeddings from Nemotron model"""
    result = nemotron_loader.get_embeddings(data.text)
    return result


@router.post("/nemotron/unload")
async def unload_nemotron_model(request: Request, user=Depends(get_verified_user)):
    """Unload Nemotron model from memory"""
    result = nemotron_loader.unload_model()
    return result


# System Monitoring
@router.get("/system/stats")
async def get_system_stats(request: Request, user=Depends(get_verified_user)):
    """Get system statistics"""
    from open_webui.utils.performance import cached
    
    @cached(ttl=10)  # Cache for 10 seconds
    async def _get_stats():
        try:
            import psutil
        except ImportError:
            return {"error": "psutil not installed. Run: pip install psutil"}
        
        return await _fetch_system_stats(psutil)
    
    return await _get_stats()

async def _fetch_system_stats(psutil):
    try:
        import GPUtil
    except ImportError:
        GPUtil = None
    
    try:
        # CPU stats
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_temp = 0
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                cpu_temp = temps['coretemp'][0].current
        except:
            pass
        
        # Memory stats
        memory = psutil.virtual_memory()
        
        # Disk stats
        disk = psutil.disk_usage('/')
        
        # GPU stats
        gpu_usage = 0
        gpu_memory = 0
        gpu_temp = 0
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_usage = gpu.load * 100
                    gpu_memory = gpu.memoryUsed * 1024 * 1024
                    gpu_temp = gpu.temperature
            except:
                pass
        
        return {
            "cpu": {
                "usage": cpu_percent,
                "cores": cpu_count,
                "temperature": cpu_temp
            },
            "memory": {
                "used": memory.used,
                "total": memory.total,
                "available": memory.available
            },
            "disk": {
                "used": disk.used,
                "total": disk.total,
                "free": disk.free
            },
            "gpu": {
                "usage": gpu_usage,
                "memory": gpu_memory,
                "temperature": gpu_temp
            },
            "network": {
                "sent": 0,
                "received": 0
            }
        }
    except Exception as e:
        log.exception(f"System stats error: {e}")
        return {
            "cpu": {"usage": 0, "cores": 0, "temperature": 0},
            "memory": {"used": 0, "total": 0, "available": 0},
            "disk": {"used": 0, "total": 0, "free": 0},
            "gpu": {"usage": 0, "memory": 0, "temperature": 0},
            "network": {"sent": 0, "received": 0}
        }


@router.get("/system/processes")
async def get_system_processes(request: Request, user=Depends(get_verified_user)):
    """Get top system processes"""
    try:
        import psutil
    except ImportError:
        return {"error": "psutil not installed"}
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pinfo = proc.info
                processes.append({
                    "pid": pinfo['pid'],
                    "name": pinfo['name'],
                    "cpu": pinfo['cpu_percent'] or 0,
                    "memory": pinfo['memory_info'].rss if pinfo['memory_info'] else 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:20]  # Top 20 processes
        
    except Exception as e:
        log.exception(f"Process list error: {e}")
        return []
