#!/usr/bin/env bash
# Remove Git conflict markers from files.

set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $(basename "$0") <file> [file...]" >&2
  exit 1
fi

for file in "$@"; do
  # Skip non-existent files
  [[ -f "$file" ]] || continue
  sed -e '/^<<<<<<< .*/d' -e '/^=======/d' -e '/^>>>>>>> .*/d' -i "$file"
done

