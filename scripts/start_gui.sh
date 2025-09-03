#!/bin/bash
# Launch the Smoke Alarm GUI development server.
# Installs dependencies on first run if needed.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUI_DIR="$SCRIPT_DIR/../gui"
cd "$GUI_DIR"
if [ ! -d node_modules ]; then
  npm install
fi
npm run dev
