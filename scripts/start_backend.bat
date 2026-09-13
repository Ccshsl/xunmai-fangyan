@echo off
chcp 65001 >nul
title 寻脉方言系统 - 仅启动后端
set "ROOT=%~dp0.."
set "BACKEND=%ROOT%\backend"

set "PY=python"
if exist "%BACKEND%\venv\Scripts\python.exe" (
    set "PY=%BACKEND%\venv\Scripts\python.exe"
)

echo 正在启动后端服务（端口 5000）...
cd /d "%BACKEND%"
"%PY%" run.py
pause