@echo off
REM Start Open WebUI with Docker Compose
echo Starting Open WebUI...
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not running or not accessible.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Start Docker Compose services
docker compose up -d

REM Wait for services to be healthy
echo.
echo Waiting for Open WebUI to start...
timeout /t 10 /nobreak >nul

REM Check if containers are running
docker compose ps | findstr "open-webui" >nul
if %errorlevel% neq 0 (
    echo Error: Failed to start Open WebUI containers.
    echo Check Docker logs for details.
    pause
    exit /b 1
)

echo.
echo Open WebUI is starting...
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo Open WebUI is now running!
echo Access it at: http://localhost:3000
echo.
echo To stop Open WebUI, run: docker compose down
echo or use the stop-open-webui.bat file
echo.
pause
