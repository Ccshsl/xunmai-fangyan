@echo off
chcp 65001 >nul
title 寻脉方言系统 - 停止服务
echo 正在停止寻脉后端与分析预览服务...
rem 仅停止命令行匹配 run.py 或 http.server 8000 的 python 进程，避免误杀其他 python
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match 'run\.py|http\.server 8000' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo 已停止相关服务。
pause