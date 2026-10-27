# 🚀 OASIS Quick Start Guide

## Launch OASIS

**Option 1 (Easiest)**: Double-click the **OASIS** icon on your desktop

**Option 2 (Terminal)**:
```bash
cd ~/projects/openui/open-webui
./launch_oasis.sh
```

The launcher will automatically:
- ✅ Check if Docker is running (starts it if needed)
- ✅ Start OASIS and Ollama containers
- ✅ Wait for services to be ready
- ✅ Open http://localhost:3000 in your browser

## Stop OASIS

```bash
cd ~/projects/openui/open-webui
./stop_oasis.sh
```

## First Time Setup

1. Launch OASIS (see above)
2. Browser opens to http://localhost:3000
3. Click "Sign up" or "Join OASIS"
4. Create admin account:
   - **Name**: dqikst
   - **Email**: dqikst@gmail.com
   - **Password**: Havikz11
5. Start using OASIS!

## Troubleshooting

### Desktop icon doesn't work
```bash
chmod +x ~/Desktop/OASIS.desktop
gio set ~/Desktop/OASIS.desktop metadata::trusted true
```

### Can't enter credentials on login page
If the input fields don't work, create account via API:
```bash
curl -X POST http://localhost:3000/api/v1/auths/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"dqikst","email":"dqikst@gmail.com","password":"Havikz11"}'
```

### Check if running
```bash
sg docker -c "docker ps"
```
Should show `oasis` and `ollama` containers.

### View logs
```bash
sg docker -c "docker logs oasis"
sg docker -c "docker logs ollama"
```

## What's Included

- 🤖 **51 Ollama Models** - Local LLMs with function calling
- 🎨 **Ultron Theme** - Red/black cyberpunk interface  
- 🔧 **20+ Functions** - Screenshot, web search, image gen, memory, etc.
- 🚀 **AutoGen Studio** - Multi-agent automation
- 🎮 **NVIDIA Features** - 3D generation, NeMo agents, CUDA support
- 🖼️ **MiniMax AI** - HD image generation
- 💾 **Knowledge Base** - Persistent learning system

## Key URLs

- **Main UI**: http://localhost:3000
- **Chat**: http://localhost:3000/chat  
- **Auth**: http://localhost:3000/auth
- **API**: http://localhost:3000/api/oasis/*

## Files Reference

- **Desktop Launcher**: `~/Desktop/OASIS.desktop`
- **Launch Script**: `~/projects/openui/open-webui/launch_oasis.sh`
- **Stop Script**: `~/projects/openui/open-webui/stop_oasis.sh`
- **Icon SVG**: `~/projects/openui/open-webui/static/assets/ultron/oasis_icon.svg`
- **Icon PNG**: `~/projects/openui/open-webui/static/assets/ultron/oasis_icon.png`

## Next Steps

After logging in:
1. **Chat** - Try chatting with llama3:latest model
2. **Tools** - Browse 20+ available functions
3. **Dashboard** - Explore OASIS control panel
4. **AutoGen** - Get automated suggestions
5. **Settings** - Configure your preferences

Enjoy your **Omniscient AI System**! 🎯
