# Ollama Function Access Configuration
## All Ollama Models Can Now Use All QA$Y$ Functions

---

## ✅ CONFIGURED

All Ollama models running on your local instance now have access to all QA$Y$ functions and tools.

---

## 🎯 Available Functions

### Core Functions (8)
1. **execute_command** - Execute QA$Y$ commands
2. **list_tools** - List all available tools
3. **execute_tool** - Execute specific tool
4. **get_memory** - Get recent memory
5. **store_fact** - Store fact in memory
6. **recall_fact** - Recall fact from memory
7. **take_screenshot** - Screenshot & analyze
8. **search_web** - Web search
9. **generate_image** - Generate images

### Tool Functions (11)
- screenshot_analyzer
- web_search
- image_generation
- enhanced_memory
- pyautogui
- aws_integration
- docker_integration
- database
- file_monitor
- performance_monitor
- echo

---

## 🚀 How It Works

### 1. Function Registry
All functions are registered in a central registry that Ollama models can access:

```python
# Functions are auto-registered on startup
function_registry.register("execute_command", execute_command)
function_registry.register("search_web", search_web)
# ... all other functions
```

### 2. Ollama Integration
When you chat with any Ollama model, functions are automatically available:

```python
# System message includes all available functions
system_message = """
You are QA$Y$ with access to:
- execute_command(command: string)
- search_web(query: string)
- take_screenshot()
- generate_image(prompt: string)
...
"""
```

### 3. Function Calling
Models can call functions by responding with:
```
FUNCTION_CALL: search_web(query="AI news")
```

---

## 🧪 Testing

### Test 1: List Available Functions
```bash
curl http://localhost:8080/api/oasis/functions
```

**Expected Output:**
```json
{
  "functions": [
    "execute_command",
    "list_tools",
    "execute_tool",
    "get_memory",
    "store_fact",
    "recall_fact",
    "take_screenshot",
    "search_web",
    "generate_image"
  ],
  "count": 9
}
```

### Test 2: Execute Function Directly
```bash
curl -X POST http://localhost:8080/api/oasis/functions/execute \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "list_tools",
    "parameters": {}
  }'
```

### Test 3: Chat with Ollama + Functions
```bash
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      {"role": "user", "content": "Search the web for AI news"}
    ],
    "use_functions": true
  }'
```

### Test 4: Use Any Ollama Model
```bash
# With llama3.1
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{"model": "llama3.1", "messages": [{"role": "user", "content": "Take a screenshot"}]}'

# With qwen
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{"model": "qwen2.5", "messages": [{"role": "user", "content": "Generate an image of a cat"}]}'

# With mistral
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{"model": "mistral", "messages": [{"role": "user", "content": "Search for Python tutorials"}]}'
```

---

## 📋 Function Schemas

All functions have OpenAI-compatible schemas:

```json
{
  "name": "search_web",
  "description": "Search the web",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query"
      }
    },
    "required": ["query"]
  }
}
```

---

## 🔧 Configuration

### Ollama URL
Default: `http://localhost:11434`

Change in `llm_connector.py`:
```python
llm_connector = LLMConnector(ollama_url="http://your-ollama:11434")
```

### Default Model
Default: `llama3.1`

Change via API:
```bash
curl -X POST http://localhost:8080/api/oasis/config \
  -d '{"default_model": "qwen2.5"}'
```

### Enable/Disable Functions
```bash
# Disable function calling
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{"model": "llama3.1", "messages": [...], "use_functions": false}'
```

---

## 🎯 Usage Examples

### Example 1: Web Search
```bash
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1",
    "messages": [
      {"role": "user", "content": "Search for the latest AI developments"}
    ]
  }'
```

**Model Response:**
```
FUNCTION_CALL: search_web(query="latest AI developments")
```

**Function Result:**
```
Found 10 results:
1. OpenAI releases GPT-5...
2. Google announces Gemini 2.0...
```

**Final Response:**
```
Based on the search results, here are the latest AI developments:
- OpenAI has released GPT-5 with improved reasoning
- Google announced Gemini 2.0 with multimodal capabilities
...
```

### Example 2: Screenshot Analysis
```bash
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{
    "model": "qwen2.5",
    "messages": [
      {"role": "user", "content": "Take a screenshot and tell me what you see"}
    ]
  }'
```

### Example 3: Image Generation
```bash
curl -X POST http://localhost:8080/api/oasis/ollama/chat \
  -d '{
    "model": "mistral",
    "messages": [
      {"role": "user", "content": "Generate an image of a futuristic city"}
    ]
  }'
```

---

## 🔍 Debugging

### Check Ollama Connection
```bash
curl http://localhost:11434/api/tags
```

### Check Available Models
```bash
curl http://localhost:11434/api/tags | jq '.models[].name'
```

### Check Function Registry
```bash
curl http://localhost:8080/api/oasis/functions | jq '.count'
```

### View Function Schemas
```bash
curl http://localhost:8080/api/oasis/functions | jq '.schemas'
```

---

## 📊 Architecture

```
Ollama Model (any model)
    ↓
System Message (includes all functions)
    ↓
Model Response (may include FUNCTION_CALL)
    ↓
Function Registry
    ↓
Execute Function
    ↓
Return Result to Model
    ↓
Final Response to User
```

---

## ✅ Verification Checklist

- [x] Function registry initialized
- [x] All QA$Y$ functions registered
- [x] Ollama integration configured
- [x] LLM connector active
- [x] All tools loaded
- [x] Function schemas generated
- [x] API endpoints active
- [x] System message includes functions
- [x] Function calling parser working
- [x] All Ollama models have access

---

## 🎉 Summary

**Every Ollama model on your system now has access to:**
- 9 core functions
- 11 tools
- Screenshot analysis
- Web search
- Image generation
- Memory management
- AWS integration
- Docker control
- Database operations
- File monitoring
- Performance tracking

**No additional configuration needed!**

Just chat with any Ollama model and it can use all functions automatically.

---

**Status**: ✅ FULLY CONFIGURED  
**Models**: ALL Ollama models  
**Functions**: 9 core + 11 tools  
**Access**: Automatic
