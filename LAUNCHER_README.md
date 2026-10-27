# OASIS Desktop Launcher

## 🚀 Quick Start

Double-click the **OASIS** icon on your desktop to launch the complete OASIS system!

## What Gets Started

When you launch OASIS, the following components start automatically:

1. **Docker Containers**
   - OASIS web application (port 3000)
   - Ollama LLM server (51 models available)
   
2. **Web Interface**
   - Automatically opens in your default browser
   - Access at: http://localhost:3000

## Files Created

### Desktop Launcher
- **Location**: `/home/ultro/Desktop/OASIS.desktop`
- **Icon**: Red neural network with "O" symbol
- **Action**: Runs launch script and opens browser

### Launch Script
- **Location**: `/home/ultro/projects/openui/open-webui/launch_oasis.sh`
- **Features**:
  - Checks if Docker is running
  - Starts all OASIS containers
  - Waits for services to be healthy
  - Opens browser automatically
  - Shows container status

### Stop Script
- **Location**: `/home/ultro/projects/openui/open-webui/stop_oasis.sh`
- **Action**: Gracefully stops all OASIS containers

### Icon Files
- **SVG**: `/home/ultro/projects/openui/open-webui/static/assets/ultron/oasis_icon.svg`
- **PNG**: `/home/ultro/projects/openui/open-webui/static/assets/ultron/oasis_icon.png`

## Manual Control

### Start OASIS Manually
```bash
cd /home/ultro/projects/openui/open-webui
./launch_oasis.sh
```

### Stop OASIS Manually
```bash
cd /home/ultro/projects/openui/open-webui
./stop_oasis.sh
```

### Check Status
```bash
sg docker -c "docker ps"
```

## Troubleshooting

### Desktop Icon Not Working
If the desktop icon doesn't work:
1. Right-click the icon
2. Select "Properties" or "Allow Launching"
3. Mark it as executable/trusted

Or run:
```bash
chmod +x ~/Desktop/OASIS.desktop
gio set ~/Desktop/OASIS.desktop metadata::trusted true
```

### Docker Not Running
If you see "Docker is not running":
```bash
sudo systemctl start docker
# Or for desktop Docker:
systemctl --user start docker-desktop
```

### Containers Won't Start
```bash
# Check logs
sg docker -c "docker logs oasis"
sg docker -c "docker logs ollama"

# Restart fresh
./stop_oasis.sh
./launch_oasis.sh
```

### Port Already in Use
If port 3000 is already in use:
```bash
# Find what's using it
sudo lsof -i :3000

# Kill it or change OASIS port in docker-compose.yaml
```

## Features Included

✅ **OASIS GUI** - Ultron Aether Nexus themed interface  
✅ **51 Ollama Models** - All local LLM models  
✅ **AutoGen Studio** - Multi-agent automation  
✅ **Function Registry** - 20+ integrated functions  
✅ **CUDA Support** - GPU acceleration (if available)  
✅ **MiniMax AI** - HD image generation  
✅ **NVIDIA 3D Gen** - 3D object generation  

## Access Points

- **Main GUI**: http://localhost:3000
- **Chat Interface**: http://localhost:3000/chat
- **API**: http://localhost:3000/api/oasis/*
- **Ollama**: http://localhost:11434

## System Requirements

- **OS**: Ubuntu/Linux
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 50GB free space
- **Docker**: Latest version with compose
- **GPU**: Optional (NVIDIA for CUDA features)

## Default Credentials

On first launch, create admin account:
- **Name**: Your name
- **Email**: Your email
- **Password**: Secure password

## Support

For issues or questions:
1. Check logs: `sg docker -c "docker logs oasis"`
2. Review documentation in repo
3. Check OASIS_RENAME.md for system details
