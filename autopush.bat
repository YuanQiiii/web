@echo off

echo Navigate to project directory
cd /d "C:\Users\exqin\Desktop\web"

echo

echo Add all changes
git add .

echo

echo Commit changes, skip if no changes
git commit -m "auto push" || echo No changes to commit.

echo

echo Push to remote repository
git push

echo

echo Complete the task
timeout /t 2