@echo off

REM Automated process
echo Starting task
echo .......... 

REM Get current date and time up to minutes
for /f "tokens=1" %%a in ("%date%") do set currentDate=%%a
set currentTime=%time:~0,5%
REM Combine date and time
set "datetime=%currentDate%_%currentTime%"
REM Replace colons with dashes to avoid special characters in Git commit messages
set "datetime=%datetime::=-%"

echo Adding all changes
git add . || (echo Failed to add changes & exit /b 1)

echo .......... 

echo Committing changes, skip if no changes
git commit -m "%datetime%" || echo No changes to commit.

echo .......... 

echo Pushing to remote repository
git push || (echo Failed to push changes & exit /b 1)

echo .......... 

echo Task completed
timeout /t 2