@echo off
chcp 65001 >nul
title 寻脉方言系统 - 一键启动
echo ============================================
echo   寻脉 - 方言地理分布与语言演变可视化平台
echo ============================================
echo.

setlocal enabledelayedexpansion
rem 定位项目根目录（本脚本位于 scripts/，上一级即项目根）
set "ROOT=%~dp0.."
set "BACKEND=%ROOT%\backend"

rem 优先使用虚拟环境，否则回退到命令行的 python
set "PY=python"
if exist "%BACKEND%\venv\Scripts\python.exe" set "PY=%BACKEND%\venv\Scripts\python.exe"
rem 若命令行 python 不可用，兜底到本机默认安装路径
if "%PY%"=="python" (
    python --version >nul 2>&1 || set "PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
)

echo 后端目录  : %BACKEND%
echo 正在启动后端服务（端口 5000）...
start "寻脉-后端" /D "%BACKEND%" "%PY%" -u run.py

rem 等待服务就绪后打开浏览器
timeout /t 2 /nobreak >nul
start "" "http://localhost:5000"

echo.
echo 后端已启动，浏览器将自动打开。
echo 如需停止，请运行 scripts\stop.bat
echo.
pause
