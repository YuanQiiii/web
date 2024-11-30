@echo off

REM Automated git push process
echo Starting task
echo .......... 

REM Get current date and time
for /f "tokens=1-2 delims= " %%a in ("%date% %time%") do set datetime=%%a_%%b
REM Replace colons with dashes in the time to avoid special characters in Git commit messages
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