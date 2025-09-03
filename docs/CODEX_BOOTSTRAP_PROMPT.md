Project bootstrap prompt for Codex AI

Objective
Create a private GitHub repository that contains:
1) A Google Sheets bound Apps Script project for the Smoke Alarm MVP.
2) A Python AI agent that automates renewals, routing, outreach, and invoicing.
3) CSV tab schemas and Google Doc text templates.
4) CI workflows for daily agent runs and Apps Script deployment.

Repo name
smoke-alarm

Top level tasks
1) Scaffold the repo with the directory layout.
2) Create all files exactly as specified.
3) Add two GitHub Actions workflows:
   - agent_cron.yaml runs daily at 08:30 Australia Melbourne time.
   - deploy_appsscript.yaml pushes Apps Script code via clasp when commit message contains [deploy apps_script].
4) Validate imports and YAML.
5) Output a checklist of GitHub Secrets.
6) Output a runbook with the one-time Google steps.

Directory layout
- apps_script/
- agent/
- sheets/
- templates/
- .github/workflows/
- scripts/
- docs/
- .gitignore

Acceptance criteria
- Repo created with all files.
- Workflows validate with a dry run.
- Python import graph resolves.
- Output a summary of next manual steps and secrets.
