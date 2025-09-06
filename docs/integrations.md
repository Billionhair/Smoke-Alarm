# Integrations

## OpenHands
- `docker compose -f agent/openhands/docker-compose.yml up`
- Works on the mounted repo; instruct it to branch, implement, test, and push.

## Open-Interpreter
- `agent/openinterpreter/run.ps1` (PowerShell). Grants file + shell access in this repo.

## Semantic PRs
- Enforces Conventional Commit titles on PRs.

## MegaLinter
- Run on-demand from Actions tab (`mega-linter` workflow) for a broad lint pass.

## SWE-bench (smoke)
- Manual workflow to keep an evaluation lane ready without slowing normal CI.
