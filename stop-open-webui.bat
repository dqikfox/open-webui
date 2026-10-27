Open your browser and navigate to http://localhost:3000@echo off
REM Stop OASIS Docker Compose services
echo Stopping OASIS...
echo.

docker compose down

echo.
echo OASIS has been stopped.
echo.
pause
