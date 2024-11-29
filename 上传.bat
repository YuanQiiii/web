@echo off

REM automate the git push process
echo Start the task
echo ..........

echo Add all changes
git add . || (echo Failed to add changes & exit /b 1)

echo ..........

echo Commit changes, skip if no changes
git commit -m "auto push" || echo No changes to commit.

echo ..........

echo Push to remote repository
git push || (echo Failed to push changes & exit /b 1)

echo ..........

echo Complete the task
timeout /t 2