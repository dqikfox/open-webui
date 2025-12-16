# CUDA Setup for OASIS

Complete CUDA 13.0 integration with NVIDIA GPU acceleration.

## Requirements

- NVIDIA GPU (Compute Capability 3.5+)
- NVIDIA Driver 525+ (for CUDA 13.0)
- Docker with nvidia-docker2
- Ubuntu 22.04/24.04

## Quick Setup

```bash
./scripts/setup_cuda.sh
```

This script will:
1. Check NVIDIA driver
2. Install nvidia-docker2
3. Build CUDA-enabled image
4. Start services with GPU support

## Manual Setup

### 1. Install NVIDIA Driver

```bash
# Check current driver
nvidia-smi

# Install if needed
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

### 2. Install nvidia-docker2

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 3. Build CUDA Image

```bash
docker build -f Dockerfile.cuda -t oasis:cuda13 .
```

### 4. Start Services

```bash
docker-compose -f docker-compose.cuda.yml up -d
```

## Docker Images

### Base Image
- **nvcr.io/nvidia/cuda-dl-base:25.11-cuda13.0-devel-ubuntu24.04**
- CUDA 13.0.2
- cuDNN 9.x
- Ubuntu 24.04
- Pre-configured for deep learning

### Included Packages

**CUDA Libraries:**
- cupy-cuda13x
- nvidia-cuda-runtime-cu13
- nvidia-cudnn-cu13
- nvidia-cublas-cu13
- nvidia-cufft-cu13
- nvidia-curand-cu13
- nvidia-cusolver-cu13
- nvidia-cusparse-cu13

**ML Frameworks:**
- PyTorch 2.x with CUDA 13.0
- TensorFlow with CUDA support
- JAX with CUDA 13
- Transformers with GPU acceleration
- Accelerate, bitsandbytes, xformers
- Flash Attention

**Vector Databases:**
- ChromaDB
- Qdrant
- Milvus
- FAISS-GPU

## API Endpoints

### Get CUDA Status
```bash
curl http://localhost:8080/api/oasis/cuda/status
```

Response:
```json
{
  "available": true,
  "device_count": 1,
  "devices": [{
    "id": 0,
    "name": "NVIDIA GeForce RTX 4090",
    "capability": [8, 9],
    "memory": 24.0,
    "memory_allocated_gb": 2.5,
    "memory_reserved_gb": 3.0
  }],
  "current_device": 0,
  "cuda_version": "13.0",
  "cudnn_version": 90100
}
```

### Clear CUDA Cache
```bash
curl -X POST http://localhost:8080/api/oasis/cuda/clear-cache
```

### Set Active Device
```bash
curl -X POST http://localhost:8080/api/oasis/cuda/set-device \
  -H "Content-Type: application/json" \
  -d '{"device_id": 0}'
```

## Frontend Component

```svelte
<script>
  import CUDAMonitor from '$lib/components/qasy/CUDAMonitor.svelte';
</script>

<CUDAMonitor />
```

## Features

✅ **CUDA 13.0 Support** - Latest CUDA toolkit
✅ **Multi-GPU** - Support for multiple GPUs
✅ **Real-time Monitoring** - Live GPU stats and memory usage
✅ **Auto-optimization** - Automatic model optimization for GPU
✅ **Cache Management** - Clear CUDA cache on demand
✅ **Device Selection** - Switch between GPUs dynamically

## GPU Optimization

### Automatic Model Optimization
```python
from oasis.utils.cuda_utils import cuda_manager

# Optimize model for GPU
model = cuda_manager.optimize_model(model, device_id=0)
```

Features:
- Automatic device placement
- torch.compile() optimization
- cuDNN benchmark mode
- Memory-efficient inference

### Memory Management
```python
# Clear cache
cuda_manager.clear_cache()

# Get status
status = cuda_manager.get_status()
```

## Docker Compose Configuration

```yaml
services:
  oasis-cuda:
    image: oasis:cuda13
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - USE_CUDA=true
```

## Troubleshooting

### NVIDIA Driver Issues
```bash
# Check driver
nvidia-smi

# Reinstall if needed
sudo apt purge nvidia-*
sudo apt install nvidia-driver-535
sudo reboot
```

### Docker GPU Access
```bash
# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:13.0.2-base-ubuntu22.04 nvidia-smi
```

### Memory Issues
```bash
# Clear cache via API
curl -X POST http://localhost:8080/api/oasis/cuda/clear-cache

# Or restart container
docker-compose -f docker-compose.cuda.yml restart
```

## Performance Tips

1. **Use Flash Attention** - 2-4x faster for transformers
2. **Enable torch.compile()** - JIT compilation for speed
3. **Batch Processing** - Process multiple items together
4. **Mixed Precision** - Use FP16/BF16 for faster inference
5. **Clear Cache Regularly** - Prevent memory fragmentation

## Monitoring

### Real-time GPU Stats
- GPU utilization
- Memory usage (allocated/reserved)
- Temperature (via nvidia-smi)
- Power consumption

### Logs
```bash
# Container logs
docker-compose -f docker-compose.cuda.yml logs -f

# CUDA logs
docker exec oasis-cuda nvidia-smi
```

## Status

✅ **Operational** - CUDA 13.0 with full GPU acceleration
