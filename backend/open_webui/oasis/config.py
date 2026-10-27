import os
from open_webui.config import PersistentConfig

# OASIS Configuration
QASY_ENABLED = PersistentConfig(
    "QASY_ENABLED",
    "qasy.enabled",
    os.getenv("QASY_ENABLED", "True").lower() == "true",
)

QASY_TOOLS_DIR = PersistentConfig(
    "QASY_TOOLS_DIR",
    "qasy.tools_dir",
    os.getenv("QASY_TOOLS_DIR", "./backend/oasis/qasy/tools"),
)

QASY_MEMORY_SIZE = PersistentConfig(
    "QASY_MEMORY_SIZE",
    "qasy.memory_size",
    int(os.getenv("QASY_MEMORY_SIZE", "100")),
)

QASY_MINIMAX_ENABLED = PersistentConfig(
    "QASY_MINIMAX_ENABLED",
    "qasy.minimax.enabled",
    os.getenv("QASY_MINIMAX_ENABLED", "True").lower() == "true",
)
