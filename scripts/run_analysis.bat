@echo off
chcp 65001 >nul
title 寻脉方言系统 - 运行数据分析流水线
set "ROOT=%~dp0.."
set "ANALYSIS=%ROOT%\backend\analysis_scripts"

set "PY=python"
if exist "%ROOT%\backend\venv\Scripts\python.exe" (
    set "PY=%ROOT%\backend\venv\Scripts\python.exe"
)

cd /d "%ANALYSIS%"

echo 运行数据分析流水线（1-9 步，产物写入 backend\outputs）...
echo.
for %%f in (1_data_preparation.py 2_data_cleaning.py 3_statistics.py 4_spatial_analysis.py 5_matplotlib_viz.py 6_folium_map.py 7_similarity_analysis.py 8_evolution_sim.py 9_tts_module.py) do (
    echo [运行] %%f
    "%PY%" "%%f"
    if errorlevel 1 echo   [警告] %%f 执行出错，继续下一步
)
echo.
echo 分析流水线执行完毕。
pause