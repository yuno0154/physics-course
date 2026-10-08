@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo [안내] 누리호 다단·페어링 분리 가상실험실을 시작합니다...
python setup_env.py --launch --file "physics_sim\nuri_rocket_staging_sim.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [오류] 실행에 실패했습니다.
    pause
    exit /b %ERRORLEVEL%
)
