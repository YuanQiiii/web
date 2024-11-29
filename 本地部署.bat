@echo off
setlocal EnableDelayedExpansion

echo Cleaning previous installations...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json
timeout /t 2 > nul

echo Installing dependencies...
call npm install || goto :error
timeout /t 2 > nul

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