@echo off
echo.
echo Data Entry Pro Launcher
echo ========================
echo.
echo Choose version to run:
echo 1. Full Version (with real-time sync)
echo 2. Lite Version (manual refresh only - recommended for Windows)
echo 3. Debug Version (for troubleshooting)
echo.
set /p choice="Enter choice (1, 2, or 3): "

if "%choice%"=="1" (
    echo Starting Data Entry Pro - Full Version...
    ".\.venv\Scripts\python.exe" main.py
) else if "%choice%"=="2" (
    echo Starting Data Entry Pro - Lite Version...
    ".\.venv\Scripts\python.exe" main_lite.py
) else if "%choice%"=="3" (
    echo Starting Data Entry Pro - Debug Version...
    ".\.venv\Scripts\python.exe" main_debug.py
) else (
    echo Invalid choice. Starting Lite Version by default...
    ".\.venv\Scripts\python.exe" main_lite.py
)

echo.
echo Application closed.
pause
