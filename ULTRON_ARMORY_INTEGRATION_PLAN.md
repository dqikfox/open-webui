# ULTRON Agent → ARMORY Integration & Linux Migration Plan

**Date**: 2025-01-27  
**Source**: ultron_agent (Windows) - https://github.com/dqikfox/ultron_agent  
**Target**: ARMORY (Linux) - /home/ultro/projects/openui/oasis  
**Objective**: Merge projects, migrate Windows→Linux, combine GUI functionality, enable all features

---

## 🎯 PROJECT OVERVIEW

### ULTRON Agent (Source)
**Architecture**: Modular AI agent with extensive Windows automation capabilities
- **Backend**: Flask/FastAPI hybrid with async support, Socket.IO for real-time
- **GUI Options**:
  1. **Web Interface (Primary)**: HTML/CSS/JS Pokedex-style GUI (`gui/ultron_enhanced/web/`)
  2. **Desktop GUI**: Tkinter-based interface with cyberpunk theme
  3. **PySide6 Wrapper**: Native Windows desktop wrapper for web UI
- **Core Features**:
  - Multi-AI routing (OpenAI, Ollama, Together.xyz, NVIDIA NIM)
  - Voice: pyttsx3, SpeechRecognition, ElevenLabs
  - Vision: OpenCV, pytesseract, PIL
  - System automation: PyAutoGUI, win32api, ctypes
  - Tool framework: Dynamic tool loading from `tools/` package
  - Pokedex GUI integration for game automation
  - Real-time system monitoring (CPU, memory, disk, GPU)
  - Plugin/pipeline framework for extending LLM capabilities
- **Main Entry Points**:
  - `main.py` - Core agent initialization
  - `agent_core.py` - Brain/core logic
  - `brain.py` - LLM routing and reasoning
  - `gui/ultron_enhanced/launch_ultron.py` - GUI launcher
  - `web_gui_server.py` - Web interface server

### ARMORY (Target)
**Architecture**: FastAPI backend + SvelteKit frontend with LLM/RAG capabilities
- **Backend**: FastAPI + SQLAlchemy, Ollama integration, pipelines framework
- **Frontend**: SvelteKit + Svelte 4 + Tailwind CSS 4, tactical red/black/gold theme
- **Current Features**:
  - Ollama model access (50+ models from `/media/ultro/CK1/models/`)
  - RAG with vector databases (ChromaDB, Milvus, Qdrant)
  - Socket.IO real-time communication
  - Docker containerization
  - MiniMax AI integration for visual generation
  - Tactical ARMORY theme with particle effects, scanlines, SVG backgrounds

---

## 📦 DEPENDENCY ANALYSIS

### Core Dependencies (Common)
```python
# Already in ARMORY or Linux-compatible
fastapi>=0.104.1         ✅ (ARMORY uses 0.104+)
uvicorn[standard]>=0.24.0 ✅
requests>=2.31.0         ✅
psutil>=5.9.0            ✅
pillow>=10.0.0           ✅
numpy>=1.24.0            ✅
opencv-python>=4.8.0     ✅ (ARMORY has opencv-python-headless)
websockets>=12.0         ✅
aiohttp>=3.9.0           ✅
```

### Ultron-Specific (Need Linux Migration)
```python
# Voice/Audio
pyttsx3>=2.90              ✅ Linux compatible (uses espeak)
SpeechRecognition>=3.10.0  ✅ Linux compatible
pyaudio>=0.2.14            ⚠️ Needs portaudio-dev: apt install portaudio19-dev
pygame>=2.5.0              ✅ Linux compatible
elevenlabs>=0.2.0          ✅ API-based (platform independent)

# Vision/OCR
pytesseract>=0.3.10        ⚠️ Needs tesseract: apt install tesseract-ocr
```

### Windows-Only Dependencies (Must Remove/Replace)
```python
pywin32>=306               ❌ Windows-only (win32api, win32con, win32gui)
pyautogui>=0.9.54          ⚠️ Partially compatible (some features Windows-specific)
pynput>=1.7.6              ✅ Linux compatible (X11/Wayland support)
```

### Windows-Specific Code Patterns to Migrate
1. **win32api usage** → Replace with subprocess/os/pathlib
2. **Windows paths (C:\\ style)** → Use pathlib.Path for cross-platform
3. **Registry access (winreg)** → Remove or use config files
4. **Windows services (win32service)** → Use systemd on Linux
5. **Admin privilege checks (ctypes.windll.shell32)** → Replace with `os.geteuid() == 0`
6. **Windows-specific automation**:
   - `pyautogui` hotkeys (Alt+F4, Win key) → Linux equivalents (Alt+F4, Super key)
   - Office app paths (`C:\Program Files\Microsoft Office\...`) → LibreOffice paths
   - Windows Explorer → Nautilus/Thunar/Dolphin

---

## 🏗️ INTEGRATION ARCHITECTURE

### Merged Backend Structure
```
backend/oasis/
├── main.py                      # Keep ARMORY FastAPI app
├── routers/
│   ├── chats.py                 # ✅ Keep ARMORY
│   ├── users.py                 # ✅ Keep ARMORY
│   ├── models.py                # ✅ Keep ARMORY
│   ├── retrieval.py             # ✅ Keep ARMORY
│   ├── pipelines.py             # ✅ Keep ARMORY
│   ├── ultron_ai.py             # 🆕 ADD: Ultron AI routing (brain.py logic)
│   ├── ultron_voice.py          # 🆕 ADD: Voice synthesis/recognition
│   ├── ultron_vision.py         # 🆕 ADD: Vision/OCR capabilities
│   ├── ultron_tools.py          # 🆕 ADD: Tool execution framework
│   └── ultron_automation.py     # 🆕 ADD: System automation (Linux-adapted)
├── models/
│   ├── ultron_agents.py         # 🆕 ADD: Agent core models
│   └── ultron_tools.py          # 🆕 ADD: Tool metadata models
├── utils/
│   ├── ultron_brain.py          # 🆕 ADD: Multi-AI routing logic
│   ├── ultron_memory.py         # 🆕 ADD: Agent memory/context
│   └── linux_automation.py      # 🆕 ADD: Linux system automation wrapper
├── tools/                       # 🆕 ADD: Dynamic tool loading
│   ├── __init__.py
│   ├── tool_interface.py        # Base class for tools
│   ├── file_tool.py             # File operations
│   ├── web_tool.py              # Web scraping/automation
│   ├── linux_system_tool.py     # Linux system control (migrated from windows_system_tool.py)
│   └── code_executor_tool.py    # Dynamic code execution
```

### Merged Frontend Structure
```
src/
├── routes/
│   ├── (app)/
│   │   ├── +layout.svelte       # ✅ Keep ARMORY tactical theme
│   │   ├── ultron-agent/        # 🆕 ADD: Ultron agent dashboard
│   │   │   ├── +page.svelte     # Agent control panel
│   │   │   ├── voice.svelte     # Voice controls
│   │   │   ├── vision.svelte    # Vision/camera interface
│   │   │   └── tools.svelte     # Tool management
│   │   └── pokedex/             # 🆕 ADD: Pokedex integration (optional)
│   │       └── +page.svelte     # Pokedex-style interface
├── lib/
│   ├── components/
│   │   ├── chat/                # ✅ Keep ARMORY
│   │   ├── ultron/              # 🆕 ADD: Ultron components
│   │   │   ├── AgentStatus.svelte
│   │   │   ├── VoiceControls.svelte
│   │   │   ├── ToolPanel.svelte
│   │   │   └── SystemMonitor.svelte
│   │   └── pokedex/             # 🆕 ADD: Pokedex components
│   │       ├── PokedexFrame.svelte
│   │       ├── PokedexScreen.svelte
│   │       └── PokedexButtons.svelte
│   ├── apis/
│   │   ├── ultron/              # 🆕 ADD: Ultron API clients
│   │   │   ├── ai.ts
│   │   │   ├── voice.ts
│   │   │   ├── vision.ts
│   │   │   └── tools.ts
│   ├── stores/
│   │   └── ultron.ts            # 🆕 ADD: Ultron state management
static/
├── assets/
│   ├── armory/                  # ✅ Keep tactical backgrounds
│   ├── ultron/                  # 🆕 ADD: Ultron assets
│   │   ├── pokedex-frame.svg
│   │   ├── ultron-logo.svg
│   │   └── sound-effects/
│   └── fonts/
```

---

## 🚀 MIGRATION STEPS

### Phase 1: Repository Setup & Analysis ✅ (Current)
- [x] Clone ultron_agent repository analysis via GitHub API
- [x] Document architecture and dependencies
- [x] Identify Windows-specific code
- [x] Create migration plan

### Phase 2: Linux Environment Preparation
```bash
# Install Linux-specific dependencies
sudo apt update
sudo apt install -y \
  portaudio19-dev \
  tesseract-ocr \
  tesseract-ocr-eng \
  espeak \
  libxcb-cursor0 \
  libx11-dev \
  libxext-dev \
  python3-tk

# Install Python packages (add to backend/requirements.txt)
pip install \
  pyttsx3==2.90 \
  SpeechRecognition==3.10.4 \
  pyaudio==0.2.14 \
  pytesseract==0.3.10 \
  pygame==2.5.2 \
  elevenlabs==1.2.0 \
  pynput==1.7.6
```

### Phase 3: Core Backend Integration
**Priority**: Migrate agent brain, tool framework, AI routing

#### 3.1: Create Ultron Router Suite
```bash
# New files to create
touch backend/oasis/routers/ultron_ai.py
touch backend/oasis/routers/ultron_voice.py
touch backend/oasis/routers/ultron_vision.py
touch backend/oasis/routers/ultron_tools.py
touch backend/oasis/routers/ultron_automation.py
```

**Example `ultron_ai.py`**:
```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter()

class AIRequest(BaseModel):
    prompt: str
    model: Optional[str] = "qwen2.5-coder"
    context: Optional[List[Dict]] = []

class AIResponse(BaseModel):
    response: str
    model: str
    tokens: Optional[int]

@router.post("/ai/generate", response_model=AIResponse)
async def generate_ai_response(request: AIRequest, user=Depends(get_verified_user)):
    """Route request to appropriate AI model (Ollama, OpenAI, etc.)"""
    # Implement multi-AI routing logic from brain.py
    pass

@router.post("/ai/function-call")
async def execute_function_call(tool_name: str, args: Dict, user=Depends(get_verified_user)):
    """Execute tool/function calls from LLM"""
    # Implement tool execution framework
    pass
```

#### 3.2: Create Tool Framework
```python
# backend/oasis/tools/__init__.py
from pathlib import Path
import importlib
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def load_tools(self):
        """Dynamically load all tools from tools/ directory"""
        tool_dir = Path(__file__).parent
        for file in tool_dir.glob("*_tool.py"):
            try:
                module = importlib.import_module(f".{file.stem}", package="oasis.tools")
                if hasattr(module, "register"):
                    tool = module.register()
                    self.tools[tool.name] = tool
                    logger.info(f"Loaded tool: {tool.name}")
            except Exception as e:
                logger.error(f"Failed to load tool {file.stem}: {e}")
    
    def execute(self, tool_name: str, **kwargs):
        """Execute a tool by name"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")
        return self.tools[tool_name].execute(**kwargs)

# Global tool registry
tool_registry = ToolRegistry()
tool_registry.load_tools()
```

#### 3.3: Migrate Windows Automation → Linux Automation
```python
# backend/oasis/utils/linux_automation.py
import subprocess
import psutil
from pathlib import Path
from typing import Optional

class LinuxSystemAutomation:
    """Linux-compatible system automation (replaces win32api)"""
    
    @staticmethod
    def open_application(app_name: str) -> bool:
        """Open application (Linux version)"""
        app_map = {
            "browser": "firefox",
            "files": "nautilus",  # Or thunar, dolphin
            "terminal": "gnome-terminal",  # Or konsole, xterm
            "editor": "gedit",  # Or kate, mousepad
            "calc": "gnome-calculator"
        }
        
        app = app_map.get(app_name.lower(), app_name)
        try:
            subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False
    
    @staticmethod
    def is_admin() -> bool:
        """Check if running as root/sudo (replaces ctypes.windll.shell32.IsUserAnAdmin())"""
        import os
        return os.geteuid() == 0
    
    @staticmethod
    def get_system_info() -> dict:
        """Get system information"""
        return {
            "os": "Linux",
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "distro": subprocess.check_output(["lsb_release", "-d"], text=True).split(":")[-1].strip()
        }
```

### Phase 4: GUI Integration

#### 4.1: Merge Pokedex GUI Elements
**Source**: `gui/ultron_enhanced/web/index.html`, `styles.css`, `app.js`

**Strategy**:
1. Extract Pokedex visual components (frame, screen, buttons)
2. Create Svelte components with ARMORY tactical theme overlay
3. Integrate into new `/ultron-agent` route

**Key Components to Port**:
- Pokedex frame SVG (red/blue theme variations)
- LCD screen effect with scanlines
- Circular D-pad button layout
- Sound effects system (wake.wav, button_press.wav, confirm.wav)
- Animated eye/face graphics
- System status panels (CPU, memory, GPU)

#### 4.2: Voice Controls Component
```svelte
<!-- src/lib/components/ultron/VoiceControls.svelte -->
<script lang="ts">
  import { ultronStore } from '$lib/stores/ultron';
  import { onMount } from 'svelte';
  
  let listening = false;
  let voiceEnabled = false;
  
  async function toggleVoice() {
    const response = await fetch('/api/v1/ultron/voice/toggle', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.token}` }
    });
    voiceEnabled = (await response.json()).enabled;
  }
  
  async function startListening() {
    listening = true;
    const response = await fetch('/api/v1/ultron/voice/listen', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.token}` }
    });
    const { transcript } = await response.json();
    ultronStore.update(s => ({ ...s, lastCommand: transcript }));
    listening = false;
  }
</script>

<div class="voice-controls tactical-panel">
  <button 
    class="voice-toggle {voiceEnabled ? 'active' : ''}"
    on:click={toggleVoice}
  >
    🎤 {voiceEnabled ? 'Voice ON' : 'Voice OFF'}
  </button>
  
  <button 
    class="listen-button {listening ? 'listening' : ''}"
    on:click={startListening}
    disabled={!voiceEnabled || listening}
  >
    {#if listening}
      <span class="pulse-ring"></span>
      Listening...
    {:else}
      🎙️ Push to Talk
    {/if}
  </button>
</div>

<style>
  .voice-controls {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: rgba(10, 10, 10, 0.8);
    border: 2px solid var(--armory-red);
    border-radius: 8px;
  }
  
  .voice-toggle.active {
    background: var(--armory-red);
    box-shadow: 0 0 20px var(--armory-red);
  }
  
  .listen-button.listening {
    animation: pulse 1.5s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
</style>
```

### Phase 5: Feature Enablement

#### 5.1: Identify Disabled Features
**Search for**:
- `FULL_FEATURES` flags
- Commented-out code blocks
- `if False:` statements
- `# TODO: Enable when...` comments
- Feature flags in config files

**Common Disabled Features in Ultron**:
1. Pygame audio (often commented out due to initialization issues)
2. Advanced vision features (camera access)
3. Some tool integrations (ADB, Unity, blockchain)
4. Windows-specific automation (will remain disabled or replaced)

#### 5.2: Enable Features Systematically
```python
# Before (ultron_agent)
FULL_FEATURES = False  # Global flag disabling features

if FULL_FEATURES:
    import pygame
    pygame.mixer.init()

# After (ARMORY)
try:
    import pygame
    pygame.mixer.init()
    logger.info("✅ Pygame audio initialized")
except Exception as e:
    logger.warning(f"Pygame audio unavailable: {e}")
    # Gracefully degrade, don't disable entire feature
```

### Phase 6: Testing & Validation

#### 6.1: Unit Tests
```python
# backend/test/ultron_agent/test_linux_automation.py
import pytest
from oasis.utils.linux_automation import LinuxSystemAutomation

def test_is_admin_check():
    # Should return False in normal test environment
    assert LinuxSystemAutomation.is_admin() == False

def test_open_application():
    # Test with safe application (calculator)
    result = LinuxSystemAutomation.open_application("calc")
    assert result == True

def test_get_system_info():
    info = LinuxSystemAutomation.get_system_info()
    assert info["os"] == "Linux"
    assert 0 <= info["cpu_percent"] <= 100
    assert 0 <= info["memory_percent"] <= 100
```

#### 6.2: Integration Tests
```bash
# Test voice system
curl -X POST http://localhost:8080/api/v1/ultron/voice/toggle \
  -H "Authorization: Bearer $TOKEN"

# Test tool execution
curl -X POST http://localhost:8080/api/v1/ultron/tools/execute \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tool": "file_tool", "action": "list", "path": "/tmp"}'

# Test AI routing
curl -X POST http://localhost:8080/api/v1/ultron/ai/generate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"prompt": "Hello, what can you do?", "model": "qwen2.5-coder"}'
```

### Phase 7: Docker Integration

#### 7.1: Update docker-compose.yaml
```yaml
services:
  oasis:
    build: .
    environment:
      - ULTRON_VOICE_ENABLED=true
      - ULTRON_TOOLS_DIR=/app/backend/oasis/tools
    devices:
      - /dev/snd:/dev/snd  # Audio device access
    volumes:
      - ./backend/oasis/tools:/app/backend/oasis/tools
```

#### 7.2: Update Dockerfile
```dockerfile
# Install Linux dependencies for Ultron features
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    espeak \
    libxcb-cursor0 \
    && rm -rf /var/lib/apt/lists/*

# Install Ultron Python dependencies
RUN pip install --no-cache-dir \
    pyttsx3==2.90 \
    SpeechRecognition==3.10.4 \
    pyaudio==0.2.14 \
    pytesseract==0.3.10 \
    pygame==2.5.2 \
    elevenlabs==1.2.0
```

---

## 🎨 GUI STYLE INTEGRATION

### ARMORY Tactical Theme + Ultron Pokedex Elements

**Combined Aesthetic**:
- **Base**: ARMORY red (#ff0000), black (#0a0a0a), gold (#cc9900)
- **Overlay**: Pokedex LCD green (#00ff00), blue (#0099ff) accents
- **Effects**: Tactical scanlines + particle system + circuit patterns + Pokedex screen glow

**Example Merged Component**:
```svelte
<div class="ultron-pokedex-panel armory-tactical">
  <!-- ARMORY tactical header with Ultron branding -->
  <div class="panel-header">
    <img src="/assets/ultron/ultron-logo.svg" alt="ULTRON" class="ultron-logo">
    <span class="armory-callsign">ARMORY-ULTRON</span>
  </div>
  
  <!-- Pokedex-style screen with ARMORY colors -->
  <div class="pokedex-screen armory-screen">
    <div class="scanline-effect"></div>
    <div class="lcd-content">
      <!-- Content here -->
    </div>
  </div>
  
  <!-- Tactical button grid (Pokedex D-pad + ARMORY styling) -->
  <div class="pokedex-controls armory-controls">
    <button class="dpad-up tactical-btn"></button>
    <button class="dpad-down tactical-btn"></button>
    <button class="dpad-left tactical-btn"></button>
    <button class="dpad-right tactical-btn"></button>
    <button class="action-a armory-btn-primary">EXECUTE</button>
    <button class="action-b armory-btn-secondary">CANCEL</button>
  </div>
</div>

<style>
  .ultron-pokedex-panel {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 100%);
    border: 3px solid var(--armory-red);
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(255, 0, 0, 0.3),
                inset 0 0 20px rgba(255, 0, 0, 0.1);
  }
  
  .pokedex-screen.armory-screen {
    background: #0a0a0a;
    border: 2px solid var(--armory-red);
    box-shadow: 
      0 0 20px rgba(255, 0, 0, 0.5),
      inset 0 0 30px rgba(0, 255, 0, 0.1); /* Pokedex LCD glow */
  }
  
  .tactical-btn {
    background: rgba(204, 153, 0, 0.2);
    border: 2px solid var(--armory-gold);
    transition: all 0.2s ease;
  }
  
  .tactical-btn:hover {
    background: var(--armory-gold);
    box-shadow: 0 0 20px var(--armory-gold);
  }
</style>
```

---

## 📋 FEATURE CHECKLIST

### Core Features to Enable
- [ ] Multi-AI routing (Ollama + OpenAI + Together.xyz)
- [ ] Voice synthesis (pyttsx3 with espeak)
- [ ] Voice recognition (SpeechRecognition)
- [ ] Vision/OCR (OpenCV + pytesseract)
- [ ] Tool execution framework
- [ ] Linux system automation
- [ ] Real-time system monitoring
- [ ] File operations (read, write, execute)
- [ ] Web scraping/automation
- [ ] Dynamic code execution
- [ ] Memory/context management
- [ ] Session persistence
- [ ] Logging and analytics

### GUI Features to Integrate
- [ ] Pokedex-style frame component
- [ ] Voice control panel
- [ ] Vision/camera interface
- [ ] Tool management panel
- [ ] System monitor dashboard
- [ ] Agent status indicators
- [ ] Sound effects system
- [ ] Animated visual feedback
- [ ] Command history
- [ ] Quick action buttons
- [ ] Theme switcher (ARMORY + Pokedex variants)

### Advanced Features (Optional)
- [ ] ElevenLabs voice integration
- [ ] Advanced AI model switching
- [ ] Plugin/extension system
- [ ] Blockchain integrations (if needed)
- [ ] Game automation (Pokedex-specific)
- [ ] ADB device control (Android)
- [ ] Unity engine integration

---

## 🚨 WINDOWS-SPECIFIC CODE REMOVAL

### Files to Delete or Replace
```bash
# Windows-only files
rm -rf Oracle_JDK-24/include/win32/
rm gui/ultron_enhanced/setup.py  # References D:/ paths, Windows admin checks

# Windows-specific tools
rm tools/windows_system_tool.py  # Replace with linux_system_tool.py

# Batch files
rm *.bat
rm run.bat
rm start-oasis.bat
rm stop-oasis.bat
```

### Code Patterns to Find & Replace
```bash
# Search for Windows-specific code
grep -r "import win32" .
grep -r "import winreg" .
grep -r "ctypes.windll" .
grep -r "C:\\\\" .
grep -r "D:\\\\" .
grep -r "os.name == 'nt'" .

# Replace patterns
sed -i 's/os.name == "nt"/sys.platform.startswith("linux")/g' **/*.py
sed -i 's/Path("C:\\\\Users")/Path.home()/g' **/*.py
```

### Manual Migration Required
1. **Admin checks**: `ctypes.windll.shell32.IsUserAnAdmin()` → `os.geteuid() == 0`
2. **File paths**: Hardcoded Windows paths → Use `Path.home()`, `Path.cwd()`, env vars
3. **Registry access**: Remove entirely or replace with config files
4. **Windows services**: systemd units on Linux
5. **Office automation**: LibreOffice paths instead of MS Office

---

## 🎯 SUCCESS CRITERIA

✅ **Migration Complete When**:
1. All Windows-specific dependencies removed or replaced
2. ARMORY containers build successfully with ultron_agent features
3. Voice system functional on Linux (pyttsx3 + espeak)
4. Vision system functional (OpenCV + tesseract)
5. Tool framework operational with Linux automation
6. GUI integrates Pokedex elements with ARMORY theme
7. Multi-AI routing functional (Ollama + OpenAI)
8. Real-time system monitoring working
9. No errors referencing Windows paths or APIs
10. All disabled features enabled and tested

✅ **Quality Checkpoints**:
- No `pywin32` or `win32api` imports remain
- No hardcoded `C:\` or `D:\` paths
- All subprocess calls use `pathlib.Path` or relative paths
- Audio works in Docker container (with device access)
- GUI responsive on localhost:3000
- Tool execution passes security validation
- API endpoints return 200 status codes
- Socket.IO real-time communication functional

---

## 📚 REFERENCE FILES

### Key Ultron Files to Review
```
main.py                           - Core entry point
agent_core.py                     - Agent brain logic
brain.py                          - Multi-AI routing
gui/ultron_enhanced/web/          - Web GUI (HTML/CSS/JS)
gui/ultron_enhanced/core/         - Core modules (voice, vision, system)
tools/                            - Tool framework
ultron_config.json                - Configuration schema
requirements_complete.txt         - Full dependency list
```

### Key ARMORY Files to Extend
```
backend/oasis/main.py        - Add ultron routers
backend/oasis/routers/       - Add ultron_*.py routers
src/routes/(app)/                 - Add ultron-agent/ route
src/lib/components/               - Add ultron/ components
static/themes/ultron.css          - Extend with Pokedex styles
docker-compose.yaml               - Add audio device access
```

---

## 🚀 NEXT STEPS

1. **Clone ultron_agent locally** (if approved by user):
   ```bash
   cd /home/ultro/projects/openui
   git clone https://github.com/dqikfox/ultron_agent.git
   ```

2. **Start with Phase 3**: Create backend routers and tool framework

3. **Incremental testing**: Build and test each feature in isolation

4. **Document changes**: Update ARMORY_THEME.md with integrated features

5. **Create migration documentation**: Track what was changed and why

---

**Status**: Ready to proceed with Phase 2 (Linux environment setup)  
**Estimated Time**: 3-5 days for full integration  
**Risk Level**: Medium (Windows→Linux migration always has surprises)
