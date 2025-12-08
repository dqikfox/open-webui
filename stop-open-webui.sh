#!/bin/bash
# Stop ARMORY Docker Compose services

echo "Stopping ARMORY..."
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Stop Docker Compose services
if sg docker -c "docker compose down"; then
    echo ""
    echo "ARMORY has been stopped."
    echo ""
else
    echo ""
    echo "Error: Failed to stop Docker Compose services."
    exit 1
fi
