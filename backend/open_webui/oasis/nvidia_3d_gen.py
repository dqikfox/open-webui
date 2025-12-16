"""NVIDIA 3D Object Generation Integration"""
import logging
import os
import subprocess
from typing import Dict, Any, Optional

log = logging.getLogger(__name__)


class Nvidia3DGenerator:
    """NVIDIA 3D Object Generation Blueprint Integration"""
    
    def __init__(self):
        self.enabled = False
        self.docker_available = False
        self._check_availability()
    
    def _check_availability(self):
        """Check if Docker and NVIDIA runtime available"""
        try:
            # Check Docker
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.docker_available = True
                log.info("✅ Docker available")
            
            # Check NVIDIA Docker runtime
            result = subprocess.run(['docker', 'run', '--rm', '--gpus', 'all', 
                                   'nvidia/cuda:12.1.0-base-ubuntu22.04', 
                                   'nvidia-smi'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.enabled = True
                log.info("✅ NVIDIA Docker runtime available")
            else:
                log.warning("⚠️ NVIDIA Docker runtime not available")
        except Exception as e:
            log.warning(f"Docker/NVIDIA check failed: {e}")
    
    async def generate_3d_object(
        self,
        prompt: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate 3D object from text prompt"""
        if not self.enabled:
            return {
                "error": "NVIDIA 3D generation not available",
                "docker": self.docker_available,
                "nvidia_runtime": self.enabled,
                "install": "https://github.com/NVIDIA-AI-Blueprints/3d-object-generation"
            }
        
        try:
            # Run NVIDIA 3D generation container
            output_path = output_path or f"/tmp/3d_object_{hash(prompt)}.obj"
            
            cmd = [
                'docker', 'run', '--rm', '--gpus', 'all',
                '-v', f'{os.path.dirname(output_path)}:/output',
                'nvcr.io/nvidia/3d-object-generation:latest',
                '--prompt', prompt,
                '--output', '/output/' + os.path.basename(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "prompt": prompt,
                    "output_path": output_path,
                    "message": "3D object generated successfully"
                }
            else:
                return {
                    "error": "Generation failed",
                    "stderr": result.stderr
                }
        except subprocess.TimeoutExpired:
            return {"error": "Generation timeout (5 minutes)"}
        except Exception as e:
            log.exception(e)
            return {"error": str(e)}
    
    async def generate_city_building(
        self,
        style: str = "futuristic",
        height: int = 100
    ) -> Dict[str, Any]:
        """Generate a futuristic city building"""
        prompt = f"{style} cyberpunk building, {height} floors, neon lights, red circuits, ultra detailed"
        return await self.generate_3d_object(prompt)
    
    def get_status(self) -> Dict[str, Any]:
        """Get 3D generation status"""
        return {
            "enabled": self.enabled,
            "docker_available": self.docker_available,
            "nvidia_runtime": self.enabled,
            "framework": "NVIDIA 3D Object Generation Blueprint",
            "install_guide": "https://github.com/NVIDIA-AI-Blueprints/3d-object-generation",
            "requirements": [
                "Docker installed",
                "NVIDIA GPU with CUDA support",
                "nvidia-docker2 runtime"
            ]
        }


# Global instance
nvidia_3d_gen = Nvidia3DGenerator()
