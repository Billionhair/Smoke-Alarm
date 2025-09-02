#!/usr/bin/env bash
set -euo pipefail
# Push apps_script/ to a bound Apps Script project via clasp.
# Prereqs: npm i -g @google/clasp; clasp login locally to capture ~/.clasprc.json

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR/apps_script"

echo '{"rootDir":"."}' > ../.clasp.json
echo "Run locally once: clasp create --type sheets --title 'Smoke MVP' --rootDir ."
echo "Then: clasp push"
