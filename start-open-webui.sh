#!/bin/bash
# Start ARMORY with Docker Compose

echo "Starting ARMORY..."
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check if Docker is running (try with and without sg docker)
if ! docker ps &> /dev/null && ! sg docker -c "docker ps" &> /dev/null; then
    echo "Error: Docker is not running or not accessible."
    echo "Please start Docker and try again."
    echo "You may need to run: sudo systemctl start docker"
    exit 1
fi

# Start Docker Compose services
if sg docker -c "docker compose up -d"; then
    echo ""
    echo "Waiting for ARMORY to start..."
    sleep 10
    
    # Check if containers are running
    if sg docker -c "docker compose ps" | grep -q "oasis"; then
        echo ""
        echo "ARMORY is starting..."
        echo "Opening browser in 5 seconds..."
        sleep 5
        
        # Open browser (try xdg-open for Linux)
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:3000 &> /dev/null &
        elif command -v gnome-open &> /dev/null; then
            gnome-open http://localhost:3000 &> /dev/null &
        elif command -v open &> /dev/null; then
            open http://localhost:3000 &> /dev/null &
        else
            echo "Could not detect browser command. Please open manually:"
        fi
        
        echo ""
        echo "ARMORY is now running!"
        echo "Access it at: http://localhost:3000"
        echo ""
        echo "To stop ARMORY, run: docker compose down"
        echo "or use the ./stop-oasis.sh script"
        echo ""
    else
        echo ""
        echo "Error: Failed to start ARMORY containers."
        echo "Check Docker logs for details with: docker compose logs"
        exit 1
    fi
else
    echo ""
    echo "Error: Failed to start Docker Compose services."
    exit 1
fi
