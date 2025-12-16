#!/bin/bash

# OASIS Launcher Script
# Starts all OASIS components including Docker containers

echo "🚀 Starting OASIS - Omniscient AI System..."
echo ""

# Navigate to OASIS directory
cd /home/ultro/projects/openui/open-webui

# Check if Docker is running, if not try to start it
if ! sg docker -c "docker info" > /dev/null 2>&1; then
    echo "⚙️  Docker is not running. Attempting to start Docker..."
    
    # Try systemd service
    if systemctl is-active --quiet docker 2>/dev/null; then
        echo "✅ Docker service is active"
    else
        sudo systemctl start docker 2>/dev/null || systemctl --user start docker 2>/dev/null || {
            echo "❌ Could not start Docker automatically. Please start Docker Desktop manually."
            exit 1
        }
        echo "⏳ Waiting for Docker to be ready..."
        sleep 5
    fi
    
    # Verify Docker is now running
    if ! sg docker -c "docker info" > /dev/null 2>&1; then
        echo "❌ Docker still not accessible. Please check Docker installation."
        exit 1
    fi
fi

echo "✅ Docker is running"
echo ""

# Start OASIS containers
echo "📦 Starting OASIS containers (oasis + ollama)..."
sg docker -c "docker compose up -d"

# Wait for containers to be healthy
echo "⏳ Waiting for OASIS to be ready..."
sleep 15

# Check container status
echo ""
echo "📊 Container Status:"
sg docker -c "docker ps --filter name=oasis --format '  ✅ {{.Names}} - {{.Status}}'"
sg docker -c "docker ps --filter name=ollama --format '  ✅ {{.Names}} - {{.Status}}'"

# Open OASIS in default browser
echo ""
echo "🌐 Opening OASIS in browser..."
sleep 2
xdg-open http://localhost:3000 2>/dev/null || firefox http://localhost:3000 2>/dev/null || google-chrome http://localhost:3000 2>/dev/null

echo ""
echo "✅ OASIS is now running!"
echo "📍 Access at: http://localhost:3000"
echo ""
echo "To stop OASIS, run: sg docker -c 'docker compose down'"
