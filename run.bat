@echo off
title IoT Stress Test Server
color 0A

echo =====================================================
echo   Starting IoT Stress Test Server...
echo =====================================================
echo.
echo Server will start at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo =====================================================
echo.

python app.py

pause
