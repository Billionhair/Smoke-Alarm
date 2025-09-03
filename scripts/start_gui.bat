@echo off
REM Launch the Smoke Alarm GUI development server.
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%..\gui"

set PORT=5173
set HOST=0.0.0.0

if not exist node_modules (
  npm install
)

for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /R /C:"IPv4.*" ^| findstr /V "127.0.0.1"') do set IP=%%A
set IP=%IP: =%
if not "%IP%"=="" echo Access the GUI from other devices on the network: http://%IP%:%PORT%

npm run dev -- --host %HOST%
