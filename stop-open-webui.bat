@echo off
REM Stop Open WebUI Docker Compose services
echo Stopping Open WebUI...
echo.

docker compose down

echo.
echo Open WebUI has been stopped.
echo.
pause
