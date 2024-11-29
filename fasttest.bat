@echo off
setlocal EnableDelayedExpansion

echo Running Python scripts...
python preprocess.py || goto :error

echo Building documentation...
npm run docs:build || goto :error

echo Starting development server...
timeout /t 1 > nul
npm run docs:dev || goto :error

echo done
exit /b 0

timeout /t 3

:error
echo error at : %errorlevel%
pause
exit /b %errorlevel%