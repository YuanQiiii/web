#!/bin/bash

# Automated process
echo "Starting task"
echo ".........."

# Set timezone to Beijing time
export TZ="Asia/Shanghai"

# Get current date and time up to minutes
currentDate=$(date +%Y-%m-%d)
currentTime=$(date +%H-%M)
# Combine date and time
datetime="${currentDate}_${currentTime}"

echo "Stashing local changes"
git stash || { echo "Failed to stash changes"; exit 1; }

echo ".........."

echo "Pulling from remote repository"
git pull || { echo "Failed to pull changes"; git stash pop; exit 1; }

echo ".........."

echo "Applying stashed changes"
git stash pop || { echo "Failed to apply stashed changes"; exit 1; }

echo ".........."

echo "Adding all changes"
git add . || { echo "Failed to add changes"; exit 1; }

echo ".........."

echo "Committing changes, skip if no changes"
git commit -m "$datetime" || echo "No changes to commit."

echo ".........."

echo "Pushing to remote repository"
git push || { echo "Failed to push changes"; exit 1; }

echo ".........."

echo "Task completed"
sleep 2