import logging
import os
from typing import Dict, Any, Optional

log = logging.getLogger(__name__)

class CUDAManager:
    """CUDA GPU management and optimization"""
    
    def __init__(self):
        self.cuda_available = False
        self.device_count = 0
        self.devices = []
        self._init_cuda()
    
    def _init_cuda(self):
        """Initialize CUDA"""
        try:
            import torch
            self.cuda_available = torch.cuda.is_available()
            
            if self.cuda_available:
                self.device_count = torch.cuda.device_count()
                self.devices = [
                    {
                        "id": i,
                        "name": torch.cuda.get_device_name(i),
                        "capability": torch.cuda.get_device_capability(i),
                        "memory": torch.cuda.get_device_properties(i).total_memory / 1024**3
                    }
                    for i in range(self.device_count)
                ]
                log.info(f"CUDA initialized: {self.device_count} GPU(s) available")
            else:
                log.warning("CUDA not available")
        except Exception as e:
            log.error(f"CUDA init error: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get CUDA status"""
        if not self.cuda_available:
            return {"available": False}
        
        try:
            import torch
            status = {
                "available": True,
                "device_count": self.device_count,
                "devices": self.devices,
                "current_device": torch.cuda.current_device(),
                "cuda_version": torch.version.cuda,
                "cudnn_version": torch.backends.cudnn.version()
            }
            
            # Memory info for each device
            for i in range(self.device_count):
                mem_allocated = torch.cuda.memory_allocated(i) / 1024**3
                mem_reserved = torch.cuda.memory_reserved(i) / 1024**3
                status["devices"][i]["memory_allocated_gb"] = round(mem_allocated, 2)
                status["devices"][i]["memory_reserved_gb"] = round(mem_reserved, 2)
            
            return status
        except Exception as e:
            log.exception(e)
            return {"available": False, "error": str(e)}
    
    def optimize_model(self, model, device_id: int = 0):
        """Optimize model for CUDA"""
        if not self.cuda_available:
            return model
        
        try:
            import torch
            device = torch.device(f"cuda:{device_id}")
            model = model.to(device)
            
            # Enable optimizations
            if hasattr(torch, "compile"):
                model = torch.compile(model)
            
            torch.backends.cudnn.benchmark = True
            
            log.info(f"Model optimized for CUDA device {device_id}")
            return model
        except Exception as e:
            log.error(f"Model optimization error: {e}")
            return model
    
    def clear_cache(self):
        """Clear CUDA cache"""
        if not self.cuda_available:
            return {"status": "cuda_not_available"}
        
        try:
            import torch
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            return {"status": "success", "message": "CUDA cache cleared"}
        except Exception as e:
            log.exception(e)
            return {"status": "error", "error": str(e)}
    
    def set_device(self, device_id: int):
        """Set active CUDA device"""
        if not self.cuda_available or device_id >= self.device_count:
            return {"status": "error", "error": "Invalid device"}
        
        try:
            import torch
            torch.cuda.set_device(device_id)
            return {"status": "success", "device": device_id}
        except Exception as e:
            log.exception(e)
            return {"status": "error", "error": str(e)}

# Global instance
cuda_manager = CUDAManager()
