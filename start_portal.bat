@echo off
rem TMP Check portal - double-click to start. Keep this window open while you use the portal.
cd /d "%~dp0"
title TMP Check portal

echo [1/3] Getting the latest version...
git pull
if errorlevel 1 echo    (Could not update - starting the version already on this PC.)

echo [2/3] Checking Python packages...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo.
  echo Python or pip is not working. Install Python 3.11+ from python.org, tick "Add python.exe to PATH", then try again.
  pause
  exit /b 1
)

if "%ANTHROPIC_API_KEY%"=="" (
  echo    NOTE: ANTHROPIC_API_KEY is not set, so only the rule-based checks will run.
) else (
  if "%TMPCHECK_AI_PASSES%"=="" set TMPCHECK_AI_PASSES=A,B,C,D
)

rem Local build only until hosting is approved (Gate 6).
set TMPCHECK_ENV=local
echo [3/3] Starting the portal at http://localhost:8000 ...
start "" cmd /c "timeout /t 5 >nul & start http://localhost:8000/login"
python -m uvicorn src.portal.app:app --port 8000
echo.
echo The portal has stopped. If you see an error above, copy it to Claude.
pause
