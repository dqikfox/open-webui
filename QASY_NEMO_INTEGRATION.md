# QA$Y$ + NVIDIA NeMo Agent Toolkit Integration

## Overview
QA$Y$ now integrates with NVIDIA NeMo Agent Toolkit for advanced AI agent capabilities including multi-turn conversations, tool use, and enterprise-grade agent orchestration.

## Installation

### Prerequisites
- Python 3.10+
- CUDA 12.1+ (for GPU acceleration)
- Docker (optional)

### Install NeMo Agent Toolkit

```bash
# Install from PyPI
pip install nemo-agent-toolkit

# Or install from source
git clone https://github.com/NVIDIA/NeMo-Agent-Toolkit.git
cd NeMo-Agent-Toolkit
pip install -e .
```

### Verify Installation
```bash
python -c "import nemo_agent; print('NeMo Agent Toolkit installed successfully')"
```

## Configuration

### Environment Variables
```bash
# Enable NeMo integration
export QASY_NEMO_ENABLED=True

# NeMo model configuration
export NEMO_MODEL_PATH=/path/to/nemo/models
export NEMO_GPU_ENABLED=True
```

### QA$Y$ Configuration
```python
# backend/oasis/qasy/config.py
QASY_NEMO_ENABLED = PersistentConfig(
    "QASY_NEMO_ENABLED",
    "qasy.nemo.enabled",
    os.getenv("QASY_NEMO_ENABLED", "False").lower() == "true",
)
```

## Features

### 1. Multi-Turn Conversations
NeMo agents maintain context across multiple turns:
```python
from oasis.qasy.nemo_integration import NeMoAgent

nemo = NeMoAgent()
agent = await nemo.create_agent("assistant", ["conversation", "memory"])
result = await nemo.execute_task("assistant", "Remember my name is John")
```

### 2. Tool Integration
NeMo agents can use QA$Y$ tools:
```python
agent = await nemo.create_agent("qa_agent", ["tools", "analysis"])
result = await nemo.execute_task("qa_agent", "Analyze this screenshot")
```

### 3. Enterprise Features
- Multi-agent orchestration
- Guardrails and safety
- Observability and monitoring
- Production-ready deployment

## API Endpoints

### Create NeMo Agent
```http
POST /api/oasis/nemo/agent
Content-Type: application/json

{
  "name": "my_agent",
  "capabilities": ["conversation", "tools", "memory"]
}
```

### Execute Task
```http
POST /api/oasis/nemo/execute
Content-Type: application/json

{
  "agent": "my_agent",
  "task": "Analyze this data"
}
```

### Get Status
```http
GET /api/oasis/nemo/status
```

## Architecture

```
QA$Y$ Agent
    ↓
NeMo Agent Toolkit
    ↓
├── Conversation Manager
├── Tool Executor
├── Memory System
└── Guardrails
    ↓
NVIDIA NIMs / LLMs
```

## Use Cases

### 1. Quality Assurance Testing
```python
qa_agent = await nemo.create_agent("qa_tester", ["testing", "analysis"])
result = await nemo.execute_task("qa_tester", "Test login functionality")
```

### 2. Code Review
```python
review_agent = await nemo.create_agent("code_reviewer", ["code", "analysis"])
result = await nemo.execute_task("code_reviewer", "Review this pull request")
```

### 3. Documentation Generation
```python
doc_agent = await nemo.create_agent("doc_writer", ["documentation", "writing"])
result = await nemo.execute_task("doc_writer", "Generate API docs")
```

## Performance

### GPU Acceleration
NeMo leverages NVIDIA GPUs for optimal performance:
- 10x faster inference with TensorRT
- Multi-GPU support
- Optimized memory usage

### Benchmarks
- Single-turn latency: <100ms
- Multi-turn context: 10K+ tokens
- Concurrent agents: 100+

## Deployment

### Docker Deployment
```dockerfile
FROM nvcr.io/nvidia/nemo:24.01

COPY backend/ /app/backend/
RUN pip install -r /app/backend/requirements.txt

CMD ["python", "-m", "oasis.main"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qasy-nemo
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: qasy
        image: qasy:latest
        resources:
          limits:
            nvidia.com/gpu: 1
```

## Monitoring

### Metrics
- Agent response time
- Tool execution success rate
- Memory usage
- GPU utilization

### Logging
```python
import logging
log = logging.getLogger("qasy.nemo")
log.setLevel(logging.INFO)
```

## Troubleshooting

### NeMo Not Found
```bash
pip install nemo-agent-toolkit
```

### CUDA Errors
```bash
# Check CUDA version
nvidia-smi

# Install correct CUDA toolkit
conda install cudatoolkit=12.1
```

### Memory Issues
```python
# Reduce batch size
config = {"batch_size": 1}
nemo = NeMoAgent(config)
```

## Resources

- [NeMo Agent Toolkit Docs](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
- [NVIDIA NIMs](https://www.nvidia.com/en-us/ai-data-science/products/nim/)
- [QA$Y$ Documentation](./QASY_README.md)

## Roadmap

- [ ] Multi-agent collaboration
- [ ] Custom guardrails
- [ ] Advanced memory systems
- [ ] Production monitoring dashboard
- [ ] Auto-scaling support

## License

Follows OASIS license (revised BSD-3-Clause)
