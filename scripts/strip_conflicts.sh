#!/usr/bin/env bash
set -euo pipefail

files=$(git ls-files -z | xargs -0 rg -l '^(<<<<<<<|=======|>>>>>>>)' || true)

if [[ -n "$files" ]]; then
  while IFS= read -r file; do
    echo "Removing conflict markers from $file"
    sed -e '/^<<<<<<< .*/d' -e '/^=======/d' -e '/^>>>>>>> .*/d' -i "$file"
  done <<<"$files"
fi
