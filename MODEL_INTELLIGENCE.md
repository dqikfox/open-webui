# OASIS Enhanced Model Capabilities

## Overview

The Enhanced Model Capabilities system provides intelligent model selection, performance monitoring, and optimization for your 51+ Ollama models and Nemotron integration.

## Features

### 1. **Intelligent Model Selection**
Automatically selects the best model for your task based on:
- Task type (code, chat, reasoning, vision, math, creative)
- Historical performance metrics
- Speed vs accuracy trade-offs
- Success rates

### 2. **Performance Monitoring**
Real-time tracking of:
- Response times
- Token generation speed (tokens/second)
- Success rates
- Error tracking
- Usage statistics

### 3. **Model Capabilities Mapping**
Pre-configured capability profiles for popular models:
- **Code**: qwen2.5-coder, deepseek-coder, codellama
- **Reasoning**: deepseek-r1, qwen2.5, llama3.x
- **Vision**: llava, bakllava
- **Embedding**: nomic-embed, mxbai-embed
- **Creative**: nous-hermes, neural-chat

### 4. **Smart Recommendations**
Query analysis to recommend optimal models:
```
Query: "Write a Python function to sort a list"
→ Recommends: qwen2.5-coder, deepseek-coder
```

## API Endpoints

All endpoints are available at `/api/v1/model-intelligence/`

### Get Model Recommendations
```bash
POST /api/v1/model-intelligence/recommend
{
  "query": "Help me debug this Python code",
  "top_n": 3
}

Response:
{
  "recommended_models": ["qwen2.5-coder:32b", "deepseek-coder:33b", "codellama:13b"],
  "detected_task": "code",
  "confidence": 0.8
}
```

### Select Best Model for Task
```bash
POST /api/v1/model-intelligence/select-best
{
  "task_type": "code",
  "prefer_fast": true,
  "min_success_rate": 0.7
}

Response:
{
  "model": "qwen2.5-coder:7b",
  "task_type": "code",
  "criteria": {
    "prefer_fast": true,
    "min_success_rate": 0.7
  }
}
```

### Get Model Performance Metrics
```bash
GET /api/v1/model-intelligence/metrics/qwen2.5-coder:32b

Response:
{
  "model": "qwen2.5-coder:32b",
  "requests": 145,
  "errors": 2,
  "success_rate": 0.986,
  "avg_response_time": 2.3,
  "tokens_per_second": 42.5,
  "last_used": "2025-12-13T10:30:00"
}
```

### Get All Model Metrics
```bash
GET /api/v1/model-intelligence/metrics

Response:
{
  "models": [
    {
      "model": "deepseek-r1:14b",
      "requests": 89,
      "success_rate": 0.98,
      "tokens_per_second": 38.2,
      ...
    },
    ...
  ],
  "total_models": 51
}
```

### Get Top Performing Models
```bash
GET /api/v1/model-intelligence/top-models?limit=10&metric=success_rate

Response:
{
  "top_models": [
    {
      "model": "qwen2.5-coder:32b",
      "rank": 1,
      "success_rate": 0.99,
      "requests": 234
    },
    ...
  ],
  "metric": "success_rate",
  "limit": 10
}
```

### Get Model Capabilities
```bash
GET /api/v1/model-intelligence/capabilities

Response:
{
  "capabilities": {
    "code": "Code generation and debugging",
    "chat": "General conversation",
    "reasoning": "Logical reasoning and problem solving",
    ...
  },
  "model_capabilities": {
    "qwen2.5-coder": ["code", "reasoning"],
    "deepseek-r1": ["reasoning", "math", "code"],
    "llava": ["vision", "chat"],
    ...
  },
  "available_models": ["qwen2.5-coder:32b", "llama3.2:3b", ...]
}
```

### Get Recent Errors (Admin)
```bash
GET /api/v1/model-intelligence/errors/recent?hours=24&limit=50

Response:
{
  "errors": [
    {
      "model": "llama3.2:1b",
      "timestamp": "2025-12-13T09:15:00",
      "error": "Context length exceeded"
    },
    ...
  ],
  "total": 3,
  "time_window_hours": 24
}
```

### Get Model Load Status (Admin)
```bash
GET /api/v1/model-intelligence/load-status

Response:
{
  "loaded_models": 5,
  "max_loaded_models": 5,
  "total_memory_mb": 12800,
  "models": [
    {
      "name": "qwen2.5-coder:32b",
      "last_used": "2025-12-13T10:30:00",
      "size_mb": 4500
    },
    ...
  ],
  "models_to_unload": []
}
```

## Usage Examples

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:3000"
TOKEN = "your_auth_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Get recommendations for a query
response = requests.post(
    f"{BASE_URL}/api/v1/model-intelligence/recommend",
    json={
        "query": "Explain how neural networks work",
        "top_n": 3
    },
    headers=headers
)
recommendations = response.json()
print(f"Best models: {recommendations['recommended_models']}")

# Select best model for coding
response = requests.post(
    f"{BASE_URL}/api/v1/model-intelligence/select-best",
    json={
        "task_type": "code",
        "prefer_fast": False,
        "min_success_rate": 0.9
    },
    headers=headers
)
best_model = response.json()["model"]
print(f"Best coding model: {best_model}")

# Get performance metrics
response = requests.get(
    f"{BASE_URL}/api/v1/model-intelligence/metrics/{best_model}",
    headers=headers
)
metrics = response.json()
print(f"Success rate: {metrics['success_rate']:.1%}")
print(f"Speed: {metrics['tokens_per_second']:.1f} tokens/sec")
```

### JavaScript/TypeScript Example

```typescript
const BASE_URL = 'http://localhost:3000';
const token = localStorage.getItem('token');

async function getModelRecommendations(query: string) {
  const response = await fetch(
    `${BASE_URL}/api/v1/model-intelligence/recommend`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query, top_n: 3 })
    }
  );
  return await response.json();
}

async function getBestModelForTask(taskType: string) {
  const response = await fetch(
    `${BASE_URL}/api/v1/model-intelligence/select-best`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        task_type: taskType,
        prefer_fast: true,
        min_success_rate: 0.8
      })
    }
  );
  return await response.json();
}

// Usage
const recommendations = await getModelRecommendations("Write a sorting algorithm");
console.log('Recommended:', recommendations.recommended_models);

const bestModel = await getBestModelForTask('code');
console.log('Best model:', bestModel.model);
```

## Task Types

| Task Type | Description | Example Models |
|-----------|-------------|----------------|
| `code` | Code generation, debugging, refactoring | qwen2.5-coder, deepseek-coder, codellama |
| `chat` | General conversation and Q&A | llama3.2, mistral, gemma2 |
| `reasoning` | Logic, analysis, problem-solving | deepseek-r1, qwen2.5, llama3.1 |
| `vision` | Image understanding and analysis | llava, bakllava |
| `embedding` | Text embedding generation | nomic-embed, mxbai-embed |
| `math` | Mathematical problem-solving | deepseek-r1, qwen2.5 |
| `creative` | Creative writing, storytelling | nous-hermes, neural-chat |
| `function_calling` | Tool/function calling | (any compatible model) |

## Automatic Features

### 1. **Auto-Metrics Collection**
All model requests are automatically tracked:
- No manual instrumentation needed
- Metrics collected for all `/api/chat` and `/api/generate` endpoints
- Real-time performance monitoring

### 2. **Model Sync**
Available models are automatically synced:
- Updates every 5 minutes
- Adds new models to capability mapping
- Removes unavailable models

### 3. **Performance-Based Routing**
When multiple models have the same capability:
- Automatically selects best performer
- Considers success rate and speed
- Adapts to changing performance

## Configuration

### Add Custom Model Capabilities

Edit `/backend/open_webui/models/model_capabilities.py`:

```python
MODEL_CAPABILITIES = {
    # Add your custom model
    "my-custom-model": [
        ModelCapability.CODE,
        ModelCapability.REASONING
    ],
    
    # Existing models...
}
```

### Adjust Load Management

Edit `/backend/open_webui/utils/model_monitoring.py`:

```python
# Change keep-alive time (default: 30 minutes)
_load_manager = ModelLoadManager(keep_alive_minutes=60)

# Change max loaded models (default: 5)
_load_manager.max_loaded_models = 10
```

## Integration with Existing Code

### Using in Chat Endpoints

```python
from open_webui.models.model_capabilities import get_router

# Get best model for user query
router = get_router()
recommended_models = router.recommend_models_for_query(user_query, top_n=1)
best_model = recommended_models[0] if recommended_models else default_model

# Use the recommended model
response = await generate_chat_completion(
    model=best_model,
    messages=messages,
    ...
)
```

### Recording Custom Metrics

```python
from open_webui.models.model_capabilities import get_metrics
import time

start = time.time()
try:
    result = await model_inference(...)
    tokens = len(result.split())
    
    # Record success
    get_metrics().record_request(
        model="my-model",
        tokens=tokens,
        time_taken=time.time() - start,
        success=True
    )
except Exception as e:
    # Record failure
    get_metrics().record_request(
        model="my-model",
        tokens=0,
        time_taken=time.time() - start,
        success=False,
        error=str(e)
    )
```

## Benefits

### For Users
- ✅ **Better Results**: Automatically uses best model for each task
- ✅ **Faster Responses**: Optimizes for speed when appropriate
- ✅ **Reliability**: Avoids models with high error rates
- ✅ **Transparency**: See which models perform best

### For Admins
- 📊 **Performance Insights**: Track all model usage and performance
- 🔍 **Error Monitoring**: Identify problematic models quickly
- ⚡ **Resource Optimization**: Auto-unload unused models
- 📈 **Usage Analytics**: Understand which models are most used

## Troubleshooting

### No Recommendations Returned
```bash
# Check available models
curl http://localhost:3000/api/v1/model-intelligence/capabilities
```

### Metrics Not Recording
```bash
# Verify metrics collection
curl http://localhost:3000/api/v1/model-intelligence/metrics
```

### Model Not in Capability Map
Add it manually in `model_capabilities.py` or it will default to `chat` capability.

## Future Enhancements

- [ ] ML-based task detection (replace keyword matching)
- [ ] Cost optimization (prefer smaller models when possible)
- [ ] A/B testing between models
- [ ] User preference learning
- [ ] Automatic capability detection
- [ ] Multi-model ensemble responses
- [ ] Predictive model loading

## API Reference

Full OpenAPI documentation available at:
```
http://localhost:3000/docs#/model-intelligence
```

After starting OASIS, visit `/docs` to see interactive API documentation.
