@echo off
chcp 65001 >nul
title 寻脉方言系统 - 一键启动
echo ============================================
echo  寻脉 - 方言地理分布与语言演变可视化平台
echo ============================================
echo.

rem 定位项目根目录（本脚本位于 scripts/，上一级即项目根）
set "ROOT=%~dp0.."
set "BACKEND=%ROOT%\backend"

rem 优先使用虚拟环境，否则回退到系统 Python
set "PY=python"
if exist "%BACKEND%\venv\Scripts\python.exe" (
    set "PY=%BACKEND%\venv\Scripts\python.exe"
)

echo 启动目录：%BACKEND%
echo 正在启动后端服务（端口 5000）...

rem 在新窗口中启动后端
start "寻脉后端" /D "%BACKEND%" "%PY%" run.py

rem 等待服务就绪后打开浏览器
timeout /t 2 /nobreak >nul
start "" "http://localhost:5000"

echo.
echo 后端已启动，浏览器将自动打开。
echo 如需停止，请运行 scripts\stop.bat
echo.
pause