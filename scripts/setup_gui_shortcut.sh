#!/usr/bin/env bash
set -euo pipefail
# Determine repository root
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GUI_DIR="$REPO_DIR/gui"

# Install dependencies
cd "$GUI_DIR"
npm install >/dev/null 2>&1 || npm install
cd "$REPO_DIR"

DESKTOP="$HOME/Desktop"
mkdir -p "$DESKTOP"

OS="$(uname)"
if [[ "$OS" == "Darwin" ]]; then
  SHORTCUT="$DESKTOP/Smoke\ Alarm\ GUI.command"
  cat <<SCRIPT > "$SHORTCUT"
#!/bin/bash
cd "$REPO_DIR/scripts"
./start_gui.sh
SCRIPT
  chmod +x "$SHORTCUT"
  echo "Created macOS shortcut at $SHORTCUT"
elif [[ "$OS" == "Linux" ]]; then
  SHORTCUT="$DESKTOP/Smoke-Alarm-GUI.desktop"
  cat <<SCRIPT > "$SHORTCUT"
[Desktop Entry]
Type=Application
Name=Smoke Alarm GUI
Exec=$REPO_DIR/scripts/start_gui.sh
Terminal=true
SCRIPT
  chmod +x "$SHORTCUT"
  echo "Created Linux desktop shortcut at $SHORTCUT"
else
  echo "Unsupported OS: $OS"
  exit 1
fi
