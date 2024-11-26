@echo off
setlocal EnableDelayedExpansion

echo Generating navigation and actions...
call npm run generate-nav || goto :error
call node generate-actions.js || goto :error

echo Running Python scripts...
call python check.py || goto :error
call python alter.py || goto :error

echo Building documentation...
call npm run docs:build || goto :error

echo Starting development server...

timeout /t 1 > nul
call npm run docs:dev || goto :error

:error
if %errorlevel% neq 0 (
    echo Error occurred. Error code: %errorlevel%
    pause
    exit /b %errorlevel%
)

timeout /t 1