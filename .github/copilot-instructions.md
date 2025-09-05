Repository instructions for GitHub Copilot

Use the root AGENTS.md as the source of truth for setup, build, test, lint, type check, routing, and PR rules.

Key invariants

Rebase on origin/main before push

No conflict markers

Run preflight and keep PRs small

Entry points

CLI python -m agent.cli route ...

UI streamlit run gui/streamlit_app.py

When proposing changes

Explain plan

Run tests and include artifacts such as plan samples and pdf samples

Follow Conventional Commits
