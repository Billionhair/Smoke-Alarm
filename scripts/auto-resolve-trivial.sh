#!/usr/bin/env bash
set -euo pipefail

# Find paths with unmerged entries
conflicted="$(git status --porcelain | awk '/^UU /{print $2}')"
[ -z "${conflicted}" ] && exit 0

while read -r f; do
  [ -z "$f" ] && continue
  # If ours and theirs are identical ignoring whitespace and blank lines, accept ours and stage
  if diff -q -w -B :2:"$f" :3:"$f" >/dev/null 2>&1; then
    git checkout --ours -- "$f"
    git add -- "$f"
    continue
  fi

done <<< "${conflicted}"
