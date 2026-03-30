@echo off
setlocal
cd /d "%~dp0"

REM Minimal launcher to avoid encoding issues with Korean paths in batch files.
python setup_env.py --launch
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Setup or Launch failed.
    pause
    exit /b %ERRORLEVEL%
)
