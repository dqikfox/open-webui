#!/bin/bash

echo "🛑 Stopping OASIS..."
cd /home/ultro/projects/openui/open-webui
sg docker -c "docker compose down"
echo "✅ OASIS stopped"
