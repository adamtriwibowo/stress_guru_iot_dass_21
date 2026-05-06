@echo off
echo =====================================================
echo   IoT Stress Test System - Installation Script
echo   Sistem Informasi Uji Stress Guru Autis (DASS-21)
echo =====================================================
echo.

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python found!
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo OK: Dependencies installed!
echo.

echo [3/3] Verifying installation...
python test_app.py
if %errorlevel% neq 0 (
    echo WARNING: Some tests failed, but you can still try to run the server.
)
echo.

echo =====================================================
echo   Installation Complete!
echo =====================================================
echo.
echo To start the server, run:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
echo =====================================================
echo.
pause
