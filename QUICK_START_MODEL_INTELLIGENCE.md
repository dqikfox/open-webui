# 🚀 Quick Start: Enhanced Model Intelligence

## Your 51 Models Just Got Smarter!

### What's New?
✨ Automatic model recommendations based on your query  
📊 Real-time performance tracking for all models  
🎯 Intelligent selection of best model for each task  
⚡ Memory optimization with auto-unload  

---

## 🔥 5-Minute Quick Start

### 1. Get Model Recommendations
```bash
# Login to get token (replace credentials)
TOKEN=$(curl -X POST http://localhost:3000/api/v1/auths/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}' \
  | jq -r .token)

# Get recommendations for a coding task
curl -X POST http://localhost:3000/api/v1/model-intelligence/recommend \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Write a Python sorting algorithm","top_n":3}' | jq
```

### 2. Select Best Model
```bash
# Get best model for coding
curl -X POST http://localhost:3000/api/v1/model-intelligence/select-best \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"task_type":"code","prefer_fast":false}' | jq
```

### 3. View Performance Metrics
```bash
# See all model statistics
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/v1/model-intelligence/metrics | jq

# Get top 5 performing models
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:3000/api/v1/model-intelligence/top-models?limit=5" | jq
```

### 4. Check Model Capabilities
```bash
# See what each model is good at
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/v1/model-intelligence/capabilities | jq
```

---

## 📚 Task Types

| Type | When to Use | Best Models |
|------|-------------|-------------|
| `code` | Programming, debugging | qwen2.5-coder, deepseek-coder |
| `reasoning` | Logic, analysis | deepseek-r1, qwen2.5 |
| `chat` | Conversation, Q&A | llama3.2, mistral |
| `math` | Calculations, equations | deepseek-r1 |
| `vision` | Image understanding | llava, bakllava |
| `creative` | Writing, stories | nous-hermes, neural-chat |
| `embedding` | Text embeddings | nomic-embed, mxbai-embed |

---

## 💻 Python Integration

```python
import requests

BASE_URL = "http://localhost:3000"
TOKEN = "your_token_here"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Get recommendations
def get_best_model(query):
    response = requests.post(
        f"{BASE_URL}/api/v1/model-intelligence/recommend",
        json={"query": query, "top_n": 1},
        headers=headers
    )
    return response.json()["recommended_models"][0]

# Use it
best_model = get_best_model("Explain quantum computing")
print(f"Use model: {best_model}")

# Get performance stats
def get_stats(model):
    response = requests.get(
        f"{BASE_URL}/api/v1/model-intelligence/metrics/{model}",
        headers=headers
    )
    return response.json()

stats = get_stats(best_model)
print(f"Success rate: {stats['success_rate']:.1%}")
print(f"Speed: {stats['tokens_per_second']:.1f} tok/s")
```

---

## 🎯 Common Use Cases

### Use Case 1: Auto-Select in Chat
```python
# Before making chat request
query = user_input
recommended = get_best_model(query)

# Use recommended model
response = ollama.chat(model=recommended, messages=[...])
```

### Use Case 2: Performance Dashboard
```python
# Get all metrics
metrics = requests.get(
    f"{BASE_URL}/api/v1/model-intelligence/metrics",
    headers=headers
).json()

# Display top performers
for m in sorted(metrics['models'], 
                key=lambda x: x['success_rate'], 
                reverse=True)[:10]:
    print(f"{m['model']}: {m['success_rate']:.1%} success")
```

### Use Case 3: Error Monitoring
```python
# Check for recent errors (admin only)
errors = requests.get(
    f"{BASE_URL}/api/v1/model-intelligence/errors/recent?hours=24",
    headers=headers
).json()

for error in errors['errors']:
    print(f"{error['model']}: {error['error']}")
```

---

## 🔍 Key Endpoints

| Endpoint | What It Does |
|----------|-------------|
| `POST /recommend` | Get model recommendations from query |
| `POST /select-best` | Choose best model for task type |
| `GET /metrics` | View all model performance stats |
| `GET /top-models` | See top performing models |
| `GET /capabilities` | List model capabilities |
| `GET /errors/recent` | Monitor recent failures (admin) |

Full docs: **http://localhost:3000/docs#/model-intelligence**

---

## 🎓 Learn More

- **Full Guide**: `MODEL_INTELLIGENCE.md` (comprehensive documentation)
- **Implementation**: `MODEL_CAPABILITIES_SUMMARY.md` (technical details)
- **API Docs**: http://localhost:3000/docs (interactive)

---

## ⚡ Pro Tips

1. **Prefer Fast**: Add `"prefer_fast": true` when speed matters more than accuracy
2. **Set Min Success**: Use `"min_success_rate": 0.9` to avoid unreliable models
3. **Monitor Trends**: Check metrics daily to spot performance changes
4. **Custom Mapping**: Add your own models to `MODEL_CAPABILITIES` in code
5. **Track Everything**: Metrics are auto-collected, no manual work needed

---

## 🐛 Troubleshooting

**Q: No recommendations returned?**  
A: Models need usage history. Use any model a few times first.

**Q: "Not authenticated" error?**  
A: Get token: `POST /api/v1/auths/signin` with credentials.

**Q: Model not in capability map?**  
A: Add to `MODEL_CAPABILITIES` in `model_capabilities.py` or defaults to "chat".

**Q: Metrics not showing?**  
A: Metrics accumulate over time. Check again after using models.

---

## 🎉 You're Ready!

Your OASIS installation now has:
- ✅ Smart model recommendations
- ✅ Performance tracking
- ✅ Automatic optimization
- ✅ Error monitoring

**Start by visiting**: http://localhost:3000/docs#/model-intelligence

Enjoy your enhanced model capabilities! 🚀
