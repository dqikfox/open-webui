#!/bin/bash

echo "🚀 Setting up CUDA for OASIS..."

# Check NVIDIA driver
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ NVIDIA driver not found. Install NVIDIA drivers first."
    exit 1
fi

echo "✅ NVIDIA driver found"
nvidia-smi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install Docker first."
    exit 1
fi

echo "✅ Docker found"

# Install nvidia-docker2
echo "📦 Installing nvidia-docker2..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

echo "✅ nvidia-docker2 installed"

# Test CUDA in Docker
echo "🧪 Testing CUDA in Docker..."
docker run --rm --gpus all nvcr.io/nvidia/cuda:13.0.2-base-ubuntu22.04 nvidia-smi

if [ $? -eq 0 ]; then
    echo "✅ CUDA Docker test passed"
else
    echo "❌ CUDA Docker test failed"
    exit 1
fi

# Build CUDA image
echo "🏗️ Building OASIS CUDA image..."
cd /home/ultro/projects/openui/oasis
docker build -f Dockerfile.cuda -t oasis:cuda13 .

if [ $? -eq 0 ]; then
    echo "✅ CUDA image built successfully"
else
    echo "❌ CUDA image build failed"
    exit 1
fi

# Start services
echo "🚀 Starting OASIS with CUDA..."
docker-compose -f docker-compose.cuda.yml up -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Check GPU status:"
echo "   curl http://localhost:8080/api/oasis/cuda/status"
echo ""
echo "🔧 Manage services:"
echo "   docker-compose -f docker-compose.cuda.yml logs -f"
echo "   docker-compose -f docker-compose.cuda.yml down"
echo ""
