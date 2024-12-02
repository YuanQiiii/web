#!/bin/bash

# Automated process
echo "Starting task"
echo ".........."

# Run ppemail.py first
echo "Running email processor..."
python3 ppemail.py
if [ $? -ne 0 ]; then
    echo "Failed to process emails"
    exit 1
fi
echo "Email processing completed"

# Get current date and time up to minutes
currentDate=$(date +%Y-%m-%d)
currentTime=$(date +%H-%M)
# Combine date and time
datetime="${currentDate}_${currentTime}"

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