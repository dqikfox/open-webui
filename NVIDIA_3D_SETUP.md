# NVIDIA 3D Object Generation Setup
## Ubuntu/Linux Installation Guide

## Prerequisites
- Ubuntu 20.04+ or compatible Linux
- NVIDIA GPU (RTX series recommended)
- Docker installed
- NVIDIA drivers installed

---

## Step 1: Install NVIDIA Drivers

```bash
# Check current driver
nvidia-smi

# If not installed, install NVIDIA drivers
sudo apt update
sudo apt install nvidia-driver-535

# Reboot
sudo reboot

# Verify installation
nvidia-smi
```

---

## Step 2: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

---

## Step 3: Install NVIDIA Container Toolkit

```bash
# Add NVIDIA package repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-docker2
sudo apt update
sudo apt install -y nvidia-docker2

# Restart Docker
sudo systemctl restart docker

# Test NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

## Step 4: Clone NVIDIA 3D Blueprint

```bash
# Clone repository
cd /home/ultro/projects
git clone https://github.com/NVIDIA-AI-Blueprints/3d-object-generation.git
cd 3d-object-generation

# Build Docker image
docker build -t nvidia-3d-gen:latest .
```

---

## Step 5: Test 3D Generation

```bash
# Generate a simple object
docker run --rm --gpus all \
  -v $(pwd)/output:/output \
  nvidia-3d-gen:latest \
  --prompt "futuristic building with red neon lights" \
  --output /output/building.obj

# Check output
ls -lh output/building.obj
```

---

## Step 6: Integrate with QA$Y$

```bash
# Test via API
curl -X POST http://localhost:8080/api/oasis/nvidia3d/status

# Generate 3D object
curl -X POST http://localhost:8080/api/oasis/nvidia3d/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cyberpunk building with glowing red circuits",
    "output_path": "/tmp/building.obj"
  }'

# Generate city building
curl -X POST http://localhost:8080/api/oasis/nvidia3d/building \
  -H "Content-Type: application/json" \
  -d '{
    "style": "futuristic",
    "height": 150
  }'
```

---

## Troubleshooting

### NVIDIA Driver Issues
```bash
# Check driver version
nvidia-smi

# Reinstall if needed
sudo apt purge nvidia-*
sudo apt install nvidia-driver-535
sudo reboot
```

### Docker Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login
```

### NVIDIA Docker Not Working
```bash
# Check nvidia-docker2 installed
dpkg -l | grep nvidia-docker

# Reinstall if needed
sudo apt install --reinstall nvidia-docker2
sudo systemctl restart docker
```

### GPU Not Detected
```bash
# Check GPU
lspci | grep -i nvidia

# Check CUDA
nvcc --version

# Install CUDA if needed
sudo apt install nvidia-cuda-toolkit
```

---

## Performance Tips

### GPU Memory
```bash
# Check GPU memory
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# Limit Docker GPU memory
docker run --gpus '"device=0"' --memory=8g ...
```

### Multi-GPU
```bash
# Use specific GPU
docker run --gpus '"device=0"' ...

# Use all GPUs
docker run --gpus all ...
```

---

## Integration with Ultron City Scene

```javascript
// In UltronCityScene.svelte
async function generate3DBuilding() {
  const res = await fetch('/api/oasis/nvidia3d/building', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      style: 'futuristic',
      height: 150
    })
  });
  
  const data = await res.json();
  console.log('3D building generated:', data.output_path);
}
```

---

## System Requirements

### Minimum
- GPU: NVIDIA GTX 1060 (6GB VRAM)
- RAM: 16GB
- Storage: 50GB free
- OS: Ubuntu 20.04+

### Recommended
- GPU: NVIDIA RTX 3060+ (12GB+ VRAM)
- RAM: 32GB
- Storage: 100GB SSD
- OS: Ubuntu 22.04

---

## Verification Checklist

- [ ] NVIDIA drivers installed (`nvidia-smi` works)
- [ ] Docker installed (`docker --version`)
- [ ] NVIDIA Docker runtime installed
- [ ] Test container runs successfully
- [ ] 3D blueprint cloned and built
- [ ] Test generation works
- [ ] QA$Y$ API endpoints respond
- [ ] Ultron city scene loads

---

## Resources

- [NVIDIA 3D Blueprint](https://github.com/NVIDIA-AI-Blueprints/3d-object-generation)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Docker Installation](https://docs.docker.com/engine/install/ubuntu/)
- [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)

---

**Status**: Ready for Ubuntu/Linux deployment
**Last Updated**: 2025-01-16
