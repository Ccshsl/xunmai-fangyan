@echo off
chcp 65001 >nul
title 寻脉方言系统 - 前端输出预览（开发）
set "ROOT=%~dp0.."
set "OUTPUT=%ROOT%\backend\outputs"

set "PY=python"
if exist "%ROOT%\backend\venv\Scripts\python.exe" (
    set "PY=%ROOT%\backend\venv\Scripts\python.exe"
)

echo 正在预览 backend\outputs 目录（端口 8000）...
echo 访问地址：http://localhost:8000/dialect_map.html
cd /d "%OUTPUT%"
"%PY%" -m http.server 8000
pause