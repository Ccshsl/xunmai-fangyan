@echo off
title Xunmai Dialect System - Launcher
setlocal
echo ============================================
echo   Xunmai - Dialect Language Evolution Map
echo ============================================
echo.

rem Project root = the parent folder of this scripts/ folder
set "ROOT=%~dp0.."
set "BACKEND=%ROOT%\backend"
echo Backend : %BACKEND%

rem Prefer venv python, else command-line python, else absolute fallback
set "PY=python"
if exist "%BACKEND%\venv\Scripts\python.exe" set "PY=%BACKEND%\venv\Scripts\python.exe"
if "%PY%"=="python" (
    python --version >nul 2>&1
    if errorlevel 1 set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
)

echo Starting backend on port 5000 ...
start "xunmai-backend" /D "%BACKEND%" "%PY%" -u run.py

rem Wait for server, then open browser
timeout /t 3 /nobreak >nul
start "" "http://localhost:5000"

echo.
echo Browser opened. Close this window to stop the server.
echo.
pause