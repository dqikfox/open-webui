#!/usr/bin/env python3
"""Migrate Ultron Agent tools to QA$Y$"""
import os
import shutil
from pathlib import Path

# Source and destination
ULTRON_TOOLS = Path("/home/ultro/projects/openui/ultron_agent/tools")
QASY_TOOLS = Path("/home/ultro/projects/openui/oasis/backend/oasis/qasy/tools")

# Priority tools to migrate
PRIORITY_TOOLS = [
    "screenshot_analyzer_tool.py",
    "web_search_tool.py",
    "image_generation_tool.py",
    "enhanced_memory_tool.py",
    "pyautogui_tool.py",
    "aws_integration_tool.py",
    "docker_integration_tool.py",
    "database_tool.py",
    "file_monitor_tool.py",
    "performance_monitor.py"
]

def migrate_tool(tool_name):
    """Migrate a single tool"""
    src = ULTRON_TOOLS / tool_name
    dst = QASY_TOOLS / tool_name
    
    if not src.exists():
        print(f"⚠️  {tool_name} not found")
        return False
    
    try:
        shutil.copy2(src, dst)
        print(f"✅ Migrated {tool_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to migrate {tool_name}: {e}")
        return False

def main():
    print("🔄 Migrating Ultron Agent tools to QA$Y$...")
    print(f"Source: {ULTRON_TOOLS}")
    print(f"Destination: {QASY_TOOLS}")
    print()
    
    # Ensure destination exists
    QASY_TOOLS.mkdir(parents=True, exist_ok=True)
    
    # Migrate priority tools
    migrated = 0
    for tool in PRIORITY_TOOLS:
        if migrate_tool(tool):
            migrated += 1
    
    print()
    print(f"✅ Migration complete: {migrated}/{len(PRIORITY_TOOLS)} tools migrated")
    print()
    print("Available tools in QA$Y$:")
    for tool_file in sorted(QASY_TOOLS.glob("*_tool.py")):
        print(f"  - {tool_file.name}")

if __name__ == "__main__":
    main()
