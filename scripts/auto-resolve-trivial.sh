#!/usr/bin/env bash
set -euo pipefail

# Find paths with unmerged entries and attempt trivial resolutions
git diff --name-only --diff-filter=U -z |
  while IFS= read -r -d '' f; do
    # If ours and theirs are identical ignoring whitespace and blank lines, accept ours and stage
    if diff -q -w -B :2:"$f" :3:"$f" >/dev/null 2>&1; then
      git checkout --ours -- "$f"
      git add -- "$f"
    fi
  done
