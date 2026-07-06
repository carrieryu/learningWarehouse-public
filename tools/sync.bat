@echo off
cd /d "%~dp0.."
python tools\sync.py
if errorlevel 1 (
  echo Sync failed.
  pause
  exit /b 1
)
echo Sync completed.
pause
