@echo off
echo Navigate to project directory
cd /d "C:\Users\exqin\Desktop\web"

echo Add all changes
git add .

echo Commit changes, skip if no changes
git commit -m "auto push" || echo No changes to commit.

echo Push to remote repository
git push

echo Complete the task
pause