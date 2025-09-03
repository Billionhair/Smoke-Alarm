#!/usr/bin/env bash
set -euo pipefail

# Start the GUI and create a desktop shortcut if possible
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$SCRIPT_DIR/../gui"
PORT=5173

cd "$GUI_DIR"
npm install --no-package-lock
npm run dev &
SERVER_PID=$!

# Give the server a moment to start
sleep 2
URL="http://localhost:$PORT"

# Open the application in the default browser
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then
  open "$URL"
fi

# Attempt to create a desktop shortcut on Linux
if command -v xdg-open >/dev/null 2>&1 && [ -d "$HOME/Desktop" ]; then
  SHORTCUT="$HOME/Desktop/smoke-alarm-gui.desktop"
  cat > "$SHORTCUT" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Smoke Alarm GUI
Exec=xdg-open $URL
Terminal=false
DESKTOP
  chmod +x "$SHORTCUT"
fi

wait $SERVER_PID
