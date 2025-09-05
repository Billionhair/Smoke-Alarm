#!/usr/bin/env bash
set -euo pipefail

git fetch origin
BASE="origin/main"

# record and reuse resolutions
git config rerere.enabled true
git config rerere.autoUpdate true
git config merge.conflictstyle zdiff3

# loop rebase until clean or manual conflicts remain
while ! git rebase "$BASE"; do
  # try trivial bulk resolutions
  bash scripts/auto-resolve-trivial.sh || true
  # if still conflicted, stop for manual fix
  if git status --porcelain | grep -q '^UU '; then
    echo "Manual conflicts remain. Resolve, then run: git rebase --continue"
    exit 1
  fi
  git rebase --continue || true
done

# hard fail if conflict markers remain anywhere
if git grep -n -E '^(<{7}|={7}|>{7}|\|{7})' -- . >/dev/null; then
  echo "Conflict markers detected after rebase. Fix before pushing."
  git grep -n -E '^(<{7}|={7}|>{7}|\|{7})' -- .
  exit 1
fi

# run pre-commit checks on staged files if available
if command -v pre-commit >/dev/null; then
  pre-commit run --hook-stage manual --files $(git diff --name-only --cached)
fi

# optional smoke tests if pytest is available
if command -v pytest >/dev/null; then
  PYTHONPATH=agent/src pytest -q || true
fi

echo "Preflight complete. Ready to push."
