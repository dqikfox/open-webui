# NVIDIA Nemotron-Nano-9B-v2 Integration

## Overview

OASIS now includes direct support for loading and using NVIDIA's Nemotron-Nano-9B-v2 model via the transformers library.

## Model Details

- **Model**: `nvidia/NVIDIA-Nemotron-Nano-9B-v2`
- **Size**: 9 billion parameters
- **Framework**: HuggingFace Transformers + PyTorch
- **Capabilities**: Text generation, embeddings, inference

## Installation

Install required dependencies:

```bash
pip install transformers torch accelerate
```

For GPU support (recommended):
```bash
pip install transformers torch accelerate bitsandbytes
```

## API Endpoints

### 1. Load Model

```bash
POST /api/oasis/nemotron/load
```

**Request:**
```json
{
  "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
  "dtype": "auto",
  "device_map": "auto"
}
```

**Response:**
```json
{
  "status": "success",
  "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
  "device": "cuda",
  "dtype": "auto",
  "parameters": 9000000000,
  "loaded": true
}
```

### 2. Check Status

```bash
GET /api/oasis/nemotron/status
```

**Response:**
```json
{
  "loaded": true,
  "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
  "device": "cuda",
  "tokenizer_loaded": true,
  "parameters": 9000000000
}
```

### 3. Generate Text

```bash
POST /api/oasis/nemotron/generate
```

**Request:**
```json
{
  "prompt": "Explain quantum computing:",
  "max_length": 512,
  "temperature": 0.7,
  "top_p": 0.9
}
```

**Response:**
```json
{
  "status": "success",
  "prompt": "Explain quantum computing:",
  "generated_text": "Quantum computing is...",
  "model": "nvidia/NVIDIA-Nemotron-Nano-9B-v2"
}
```

### 4. Get Embeddings

```bash
POST /api/oasis/nemotron/embeddings
```

**Request:**
```json
{
  "text": "OASIS is an advanced AI system"
}
```

**Response:**
```json
{
  "status": "success",
  "embeddings": [[0.123, -0.456, ...]],
  "shape": [1, 768],
  "text": "OASIS is an advanced AI system"
}
```

### 5. Unload Model

```bash
POST /api/oasis/nemotron/unload
```

**Response:**
```json
{
  "status": "success",
  "message": "Model unloaded"
}
```

## Python Usage

### Direct Usage

```python
from transformers import AutoModel
model = AutoModel.from_pretrained(
    "nvidia/NVIDIA-Nemotron-Nano-9B-v2", 
    dtype="auto"
)
```

### Via OASIS API

```python
import requests

# Load model
response = requests.post("http://localhost:3000/api/oasis/nemotron/load", json={
    "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
    "dtype": "auto"
})
print(response.json())

# Generate text
response = requests.post("http://localhost:3000/api/oasis/nemotron/generate", json={
    "prompt": "What is artificial intelligence?",
    "max_length": 256
})
print(response.json()["generated_text"])
```

## Test Script

Run the included test script:

```bash
python test_nemotron.py
```

This will:
- Check model status
- Load the model
- Test text generation
- Test embedding generation
- Show final status

## Configuration Options

### dtype Options
- `"auto"` - Automatically select best dtype
- `"float16"` - Half precision (faster, less memory)
- `"bfloat16"` - Brain float 16 (better for training)
- `"float32"` - Full precision (slower, more memory)

### device_map Options
- `"auto"` - Automatically distribute across available devices
- `"cpu"` - Force CPU usage
- `"cuda"` - Use NVIDIA GPU
- `"cuda:0"` - Use specific GPU

## Hardware Requirements

### Minimum (CPU)
- 32GB RAM
- 50GB disk space

### Recommended (GPU)
- NVIDIA GPU with 16GB+ VRAM
- 16GB+ system RAM
- 50GB disk space
- CUDA 11.8+

## Performance Tips

1. **Use GPU**: Model runs 10-100x faster on GPU
2. **Use float16**: Reduces memory usage by 50%
3. **Use device_map="auto"**: Enables model parallelism
4. **Batch processing**: Process multiple requests together

## Integration with OASIS

The Nemotron model is fully integrated with OASIS:

- ✅ Function calling support
- ✅ Memory system integration
- ✅ AutoGen Studio compatible
- ✅ CUDA acceleration
- ✅ REST API endpoints
- ✅ Python SDK

## Example Workflows

### 1. Q&A with Nemotron

```python
import requests

# Load model
requests.post("http://localhost:3000/api/oasis/nemotron/load")

# Ask question
response = requests.post("http://localhost:3000/api/oasis/nemotron/generate", json={
    "prompt": "Q: What is machine learning?\nA:",
    "max_length": 256,
    "temperature": 0.7
})

print(response.json()["generated_text"])
```

### 2. Semantic Search with Embeddings

```python
# Get embeddings for documents
docs = [
    "OASIS is an AI system",
    "Machine learning uses data",
    "Neural networks process information"
]

embeddings = []
for doc in docs:
    resp = requests.post("http://localhost:3000/api/oasis/nemotron/embeddings", 
                        json={"text": doc})
    embeddings.append(resp.json()["embeddings"])

# Use embeddings for similarity search
# ... cosine similarity calculation ...
```

## Troubleshooting

### Out of Memory

Reduce memory usage:
```json
{
  "dtype": "float16",
  "device_map": "auto"
}
```

### Slow Generation

Use GPU and optimize:
```json
{
  "device_map": "cuda",
  "dtype": "float16"
}
```

### Model Not Found

Install transformers:
```bash
pip install transformers torch
```

## References

- **Model Card**: https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2
- **Transformers Docs**: https://huggingface.co/docs/transformers
- **NVIDIA AI**: https://www.nvidia.com/en-us/ai/

## Support

For issues or questions:
1. Check model status: `GET /api/oasis/nemotron/status`
2. View OASIS logs: `sg docker -c "docker logs oasis"`
3. Test with script: `python test_nemotron.py`
