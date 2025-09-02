Smoke Alarm Compliance Monorepo

Contents
- apps_script: Google Sheets bound Apps Script for reports, invoices, SMS, reminders.
- agent: Python AI agent for renewals, routing, outreach, and Stripe invoicing.
- sheets: CSV tab schemas to initialise the Sheet.
- templates: Google Doc text templates for report and invoice.
- .github/workflows: CI for daily agent runs and Apps Script deployments.
- scripts: helper for clasp pushes.

First run quick start
1) Create target Google Sheet and import CSVs from sheets to create tabs. Or run oneTimeSetup in Apps Script to create headers.
2) Create a Google Doc from templates/Compliance_Report_TEMPLATE.txt. Put its Doc ID into Templates sheet row with Name=ComplianceReport.
3) Fill Settings tab: BUSINESS_*, GST_RATE, PRICE_* (in cents), REPORTS_FOLDER_ID, provider keys.
4) Authorise Apps Script scopes when prompted. Run ensureTriggers once.
5) Add GitHub Secrets listed here and push.

Safety and scope
- Battery-only workflow. No electrical work. Refer hardwired to a licensed electrician.
