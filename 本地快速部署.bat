@echo off
setlocal EnableDelayedExpansion

echo Running Python scripts...
call python preprocess.py || goto :error

echo Building documentation...
call npm run docs:build || goto :error

echo Starting development server...

timeout /t 3 > nul
call npm run docs:dev || goto :error

:error
if %errorlevel% neq 0 (
    echo Error occurred. Error code: %errorlevel%
    pause
    exit /b %errorlevel%
)

timeout /t 2