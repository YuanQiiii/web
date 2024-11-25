@echo off
REM Navigate to project directory
cd /d "C:\Users\exqin\Desktop\web"

REM Add all changes
git add .

REM Commit changes, skip if no changes
git commit -m "auto push" || echo No changes to commit.

REM Push to remote repository
git push

echo git push done.
pause