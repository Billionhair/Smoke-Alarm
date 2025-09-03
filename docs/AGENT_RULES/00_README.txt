CONFORMANCE WITH CORE REPOSITORY DOCUMENTS
This file inherits and must conform to:
- core/Repo_Mega_Prompt.txt
- core/World_Class_Blueprint.txt

Mandatory repository rules
- Respect battery only scope. Refer hardwired alarms to licensed electricians.
- Keep Google Sheets the initial system of record. Design a clean path to Postgres without breaking UI.
- Keep the route CLI and outputs stable while adding tests and reliability.
- Keep Apps Script deployable with clasp and allow TypeScript builds.
- Do not break existing report and invoice templates. Provide a safe migration script.

Output rules
- Use unified diffs and exact commands for PRs. Keep prose minimal and structured.
- ASCII only. No secrets in client or code.

Smoke Alarm Agent Package
Date: 2025-09-03
ASCII only

WHAT THIS IS
A single folder you can upload to any agent. It contains a master repo prompt and blueprint, plus per-principle mega prompts and blueprints. Agents should always read core files first, then the relevant principle file for the task at hand.

HOW TO USE
1) Place this folder at repo root under docs/AGENT_RULES or upload all files to your agent.
2) Start your agent and say:
   - Use core/Repo_Mega_Prompt.txt as governing rules.
   - Use core/World_Class_Blueprint.txt as binding constraints.
   - For this task, load the matching principle prompt and blueprint from principles/... and follow them strictly.
   - Begin with PR 1 from the selected prompt. Output diffs and exact commands only.
3) Repeat per task. One PR at a time.

FOLDER MAP
- core: master repo prompt, master blueprint, and UI UX mega prompt.
- principles: per-principle prompts and blueprints.

TASK ROUTING
- Architecture tasks: principles/architecture
- UI UX tasks: principles/uiux
- Security and privacy tasks: principles/security
- Testing and quality: principles/testing
- Performance and reliability: principles/performance_reliability
- Developer experience and repo standards: principles/devex
- CI CD and releases: principles/cicd_release
- Data modeling and APIs: principles/data_api
- Documentation and governance: principles/docs_governance
- Product, pricing, and growth: principles/product_growth
- Accessibility and internationalization: principles/a11y_i18n
- Licensing and OSS compliance: principles/licensing_compliance

STOP RULES
- Never place secrets in client or in repo. Use env vars or Script Properties only.
- One PR per request. Do not batch unrelated changes.
- Respect acceptance criteria in each blueprint.
