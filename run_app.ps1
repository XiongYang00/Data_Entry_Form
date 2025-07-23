# Data Entry Pro Launcher
Write-Host ""
Write-Host "Data Entry Pro Launcher" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose version to run:"
Write-Host "1. Full Version (with real-time sync)"
Write-Host "2. Lite Version (manual refresh only - recommended for Windows)" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter choice (1 or 2)"

switch ($choice) {
    "1" {
        Write-Host "Starting Data Entry Pro - Full Version..." -ForegroundColor Yellow
        & ".\.venv\Scripts\python.exe" main.py
    }
    "2" {
        Write-Host "Starting Data Entry Pro - Lite Version..." -ForegroundColor Yellow
        & ".\.venv\Scripts\python.exe" main_lite.py
    }
    default {
        Write-Host "Invalid choice. Starting Lite Version by default..." -ForegroundColor Yellow
        & ".\.venv\Scripts\python.exe" main_lite.py
    }
}

Write-Host ""
Write-Host "Application closed." -ForegroundColor Gray
Read-Host "Press Enter to exit"
