"""
OASIS - Quality Assurance System
Advanced AI agent integrated into OASIS
Rebadged from Ultron Agent
"""

__version__ = "1.0.0"
__author__ = "dqikfox"

from .agent_core import OasisAgent
from .tool_loader import OasisToolLoader
from .memory_system import OasisMemory

__all__ = ["OasisAgent", "OasisToolLoader", "OasisMemory"]
