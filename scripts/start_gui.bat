@echo off
REM Launch the Smoke Alarm GUI development server.
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%..\gui"
if not exist node_modules (
  npm install
)
npm run dev
