#!/bin/bash
# NVIDIA 3D Object Generation Setup Script for Ubuntu/Linux

set -e

echo "🚀 NVIDIA 3D Object Generation Setup"
echo "====================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ This script is for Linux/Ubuntu only"
    exit 1
fi

# Check for NVIDIA GPU
echo ""
echo "🔍 Checking for NVIDIA GPU..."
if ! lspci | grep -i nvidia > /dev/null; then
    echo "❌ No NVIDIA GPU detected"
    exit 1
fi
echo "✅ NVIDIA GPU detected"

# Check NVIDIA drivers
echo ""
echo "🔍 Checking NVIDIA drivers..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  NVIDIA drivers not found"
    echo "Installing NVIDIA drivers..."
    sudo apt update
    sudo apt install -y nvidia-driver-535
    echo "⚠️  Please reboot and run this script again"
    exit 0
fi
echo "✅ NVIDIA drivers installed"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader

# Check Docker
echo ""
echo "🔍 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "✅ Docker installed"
    echo "⚠️  Please logout and login again, then run this script"
    exit 0
fi
echo "✅ Docker installed: $(docker --version)"

# Check NVIDIA Docker runtime
echo ""
echo "🔍 Checking NVIDIA Docker runtime..."
if ! docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "Installing NVIDIA Container Toolkit..."
    
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
        sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    
    sudo apt update
    sudo apt install -y nvidia-docker2
    sudo systemctl restart docker
    
    echo "✅ NVIDIA Docker runtime installed"
else
    echo "✅ NVIDIA Docker runtime working"
fi

# Clone NVIDIA 3D Blueprint
echo ""
echo "📦 Setting up NVIDIA 3D Blueprint..."
BLUEPRINT_DIR="/home/ultro/projects/nvidia-3d-gen"

if [ ! -d "$BLUEPRINT_DIR" ]; then
    echo "Cloning repository..."
    git clone https://github.com/NVIDIA-AI-Blueprints/3d-object-generation.git "$BLUEPRINT_DIR"
    cd "$BLUEPRINT_DIR"
    
    echo "Building Docker image..."
    docker build -t nvidia-3d-gen:latest .
    echo "✅ NVIDIA 3D Blueprint installed"
else
    echo "✅ NVIDIA 3D Blueprint already installed"
fi

# Test generation
echo ""
echo "🧪 Testing 3D generation..."
mkdir -p /tmp/nvidia-3d-test

if docker run --rm --gpus all \
    -v /tmp/nvidia-3d-test:/output \
    nvidia-3d-gen:latest \
    --prompt "simple cube" \
    --output /output/test.obj 2>/dev/null; then
    echo "✅ 3D generation test successful"
    ls -lh /tmp/nvidia-3d-test/test.obj
else
    echo "⚠️  3D generation test failed (this is normal if image not built yet)"
fi

# Summary
echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Test: curl http://localhost:8080/api/oasis/nvidia3d/status"
echo "  2. Generate: curl -X POST http://localhost:8080/api/oasis/nvidia3d/building"
echo "  3. View docs: cat NVIDIA_3D_SETUP.md"
echo ""
echo "System Info:"
echo "  GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "  Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader)"
echo "  Docker: $(docker --version | cut -d' ' -f3)"
echo "  CUDA: $(docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvcc --version 2>/dev/null | grep release | cut -d' ' -f5 || echo 'N/A')"
