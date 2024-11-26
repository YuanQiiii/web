@echo off
echo Generating navigation and actions...
npm run generate-nav
node generate-actions.js

echo Running Python scripts...
python check.py
python alter.py

echo Building documentation...
npm run docs:build

echo Starting development server...
start http://localhost:5173
npm run docs:dev