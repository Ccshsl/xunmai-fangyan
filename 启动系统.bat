@echo off
chcp 65001 >nul
rem 根目录快捷入口：仅调用 scripts\start.bat，不包含任何业务逻辑
call "%~dp0scripts\start.bat"