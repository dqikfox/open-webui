# QA$Y$ - Quality Assurance System
## Integrated AI Agent for OASIS

### Overview
QA$Y$ (Quality Assurance System) is an advanced AI agent system integrated into OASIS, rebadged from the Ultron Agent project. It provides autonomous workflow execution, comprehensive tool ecosystem, and multi-modal interaction capabilities.

### Features
- ✅ **Agent-Based Execution**: Autonomous command processing
- ✅ **Tool Ecosystem**: Extensible tool system with dynamic loading
- ✅ **Memory System**: Short-term and long-term memory management
- ✅ **API Integration**: RESTful endpoints for all operations
- ✅ **MiniMax AI**: Image generation and visual analysis
- ✅ **Ultron Theme**: Dark futuristic UI with red glowing circuits

### Architecture

```
backend/oasis/qasy/
├── __init__.py              # Module initialization
├── agent_core.py            # Core agent logic
├── tool_loader.py           # Dynamic tool loading
├── memory_system.py         # Memory management
├── config.py                # Configuration
└── tools/                   # Tool implementations
    └── echo_tool.py         # Sample tool

backend/oasis/routers/
└── qasy.py                  # API endpoints

backend/oasis/utils/
└── minimax_image_gen.py     # MiniMax integration
```

### API Endpoints

#### Execute Command
```http
POST /api/oasis/execute
Content-Type: application/json

{
  "command": "test hello world",
  "context": {}
}
```

#### List Tools
```http
GET /api/oasis/tools
```

#### Execute Tool
```http
POST /api/oasis/tool/echo
Content-Type: application/json

{
  "params": {
    "message": "Hello QA$Y$"
  }
}
```

#### Get Status
```http
GET /api/oasis/status
```

#### Get Memory
```http
GET /api/oasis/memory
```

#### Clear Memory
```http
DELETE /api/oasis/memory
```

### Configuration

Environment variables:
```bash
QASY_ENABLED=True
QASY_TOOLS_DIR=./backend/oasis/qasy/tools
QASY_MEMORY_SIZE=100
QASY_MINIMAX_ENABLED=True
```

### Creating Custom Tools

```python
# backend/oasis/qasy/tools/my_tool.py
from ..tool_loader import QasyTool
from typing import Dict, Any

class MyTool(QasyTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Description of my tool"
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        # Tool logic here
        return {
            "status": "success",
            "result": "Tool executed"
        }
```

### MiniMax Integration

Generate QA$Y$ branded assets:
```python
from backend.oasis.utils.minimax_image_gen import generate_ultron_image

# Generate logo
logo_path = generate_ultron_image(
    prompt="QA$Y$ quality assurance system logo, modern tech style",
    width=512,
    height=512,
    output_path="static/assets/qasy/logo.png"
)
```

### Commands

QA$Y$ supports the following command patterns:

- `test [args]` - Run tests
- `analyze [args]` - Analyze data
- `tool [tool_name] [args]` - Execute specific tool

### Memory System

QA$Y$ maintains two types of memory:

1. **Short-term Memory**: Recent conversation history (last 100 messages)
2. **Long-term Memory**: Persistent facts and knowledge

### Integration with OASIS

QA$Y$ integrates seamlessly with OASIS:

- Uses OASIS authentication
- Follows OASIS coding patterns
- Styled with Ultron theme
- Accessible via API and UI

### Development

#### Adding New Features
1. Create tool in `backend/oasis/qasy/tools/`
2. Tool will be auto-loaded on startup
3. Access via API or UI

#### Testing
```bash
# Test QA$Y$ status
curl http://localhost:8080/api/oasis/status

# Test tool execution
curl -X POST http://localhost:8080/api/oasis/tool/echo \
  -H "Content-Type: application/json" \
  -d '{"params": {"message": "test"}}'
```

### Roadmap

- [ ] Frontend UI components
- [ ] Voice integration
- [ ] Advanced tool migration from Ultron Agent
- [ ] Autonomous workflow system
- [ ] Visual analysis tools
- [ ] Web automation tools

### Credits

- **Original Project**: Ultron Agent by dqikfox
- **Integration**: QA$Y$ for OASIS
- **Theme**: Ultron dark theme with red circuits
- **AI**: MiniMax for image generation

### License

Follows OASIS license (revised BSD-3-Clause)
