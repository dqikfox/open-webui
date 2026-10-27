#!/bin/bash
# Quick Start: NVIDIA Nemotron-Nano-9B-v2 with OASIS

echo "🚀 NVIDIA Nemotron-Nano-9B-v2 Quick Start"
echo ""

# Check if OASIS is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "❌ OASIS is not running. Starting OASIS..."
    ./launch_oasis.sh
    sleep 10
fi

echo "✅ OASIS is running"
echo ""

# Load Nemotron model
echo "📥 Loading Nemotron-Nano-9B-v2 model..."
curl -X POST http://localhost:3000/api/oasis/nemotron/load \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
    "dtype": "auto",
    "device_map": "auto"
  }' | jq '.'

echo ""
echo "⏳ Waiting for model to load (this may take a few minutes)..."
sleep 5

# Check status
echo ""
echo "📊 Checking model status..."
curl -s http://localhost:3000/api/oasis/nemotron/status | jq '.'

# Generate text
echo ""
echo "💬 Testing text generation..."
curl -X POST http://localhost:3000/api/oasis/nemotron/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain artificial intelligence in one sentence:",
    "max_length": 128,
    "temperature": 0.7
  }' | jq '.generated_text'

echo ""
echo "✅ Nemotron model is ready!"
echo ""
echo "📖 See NEMOTRON_SETUP.md for full documentation"
echo "🧪 Run 'python test_nemotron.py' for comprehensive tests"
