#!/bin/bash
# Launch the Smoke Alarm GUI development server.
# Installs dependencies on first run if needed.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$SCRIPT_DIR/../gui"
PORT=5173
HOST=0.0.0.0

cd "$GUI_DIR"
if [ ! -d node_modules ]; then
  npm install
fi

LOCAL_IP=$(ip route get 1 2>/dev/null | awk '{print $7; exit}')
if [ -n "$LOCAL_IP" ]; then
  echo "Access the GUI from other devices on the network: http://$LOCAL_IP:$PORT"
fi

npm run dev -- --host "$HOST"
