#!/usr/bin/env bash
set -euo pipefail

git ls-files -z | xargs -0 rg -l '^(<<<<<<<|=======|>>>>>>>)' | while read -r file; do
  echo "Removing conflict markers from $file"
  sed -e '/^<<<<<<< .*/d' -e '/^=======/d' -e '/^>>>>>>> .*/d' -i "$file"

done
