Usage Guide

Prereqs
- Google account with Drive, Sheets, Docs, Gmail access
- Stripe account
- ClickSend or Twilio account
- GitHub account with Actions enabled
- Python 3.10+ on your machine

One time setup
1) Create the Google Sheet
- Import each CSV from the sheets folder to create tabs:
  Clients, Properties, Alarms, Inspections, LineItems, Invoices, Events, Settings, Templates.

2) Create the Google Doc template
- In Docs, paste templates/Compliance_Report_TEMPLATE.txt into a new Doc.
- Copy the Doc ID from the URL and set it as Templates.DocTemplateId where Name=ComplianceReport.

3) Bind Apps Script and authorise scopes
- In the Sheet, open Extensions -> Apps Script.
- Create files matching apps_script folder. Paste each file's content.
- Save, then run oneTimeSetup if you did not import CSVs.
- Run ensureTriggers once and accept permissions.

4) Fill Settings tab
- BUSINESS_NAME, BUSINESS_EMAIL, BUSINESS_PHONE, BUSINESS_ADDRESS
- GST_RATE 0.00 if not registered, 0.10 if registered
- PRICE_SERVICE_CENTS 12900, PRICE_ALARM_CENTS 4500
- REPORTS_FOLDER_ID Drive folder for PDF storage
- STRIPE_SECRET_KEY and success/cancel URLs
- SMS_PROVIDER and provider keys

5) Add the Google Form
- Link a Form to the Sheet with exact field names:
  PropertyID, Technician, Findings, Actions, BatteriesReplacedCount, AlarmsReplacedCount, PhotosFolderUrl, ComplianceStatus.
- Add an installable trigger for onInspectionFormSubmit.

6) GitHub Secrets for CI
- GOOGLE_SHEET_ID
- SERVICE_ACCOUNT_JSON (full JSON content of the service account)
- GOOGLE_SUBJECT_EMAIL (optional)
- STRIPE_SECRET_KEY, STRIPE_SUCCESS_URL, STRIPE_CANCEL_URL
- SMS_PROVIDER, CLICKSEND_USER, CLICKSEND_KEY
- TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM
- APPS_SCRIPT_ID (bound scriptId)
- CLASP_RC_JSON (contents of ~/.clasprc.json after clasp login)

Local agent usage
1) Install
  cd agent
  python -m venv .venv
  . .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
  # place service_account.json in agent

2) Check
  python -m agent.cli ping
  python -m agent.cli route --date today

Day to day
- Prospecting
  - Put PMs into agent/data/agencies_seed.csv
  - python -m agent.cli leads_enrich agent/data/agencies_seed.csv
  - python -m agent.cli outreach_sms --list agent/data/agencies_enriched.csv
- Field work
  - Submit the Form on-site.
  - The script appends an Inspections row, creates a PDF report, makes a Stripe checkout, emails the client.
- Renewals
  - CI runs renewals at 30, 7, and 0 days. You can also run locally:
    python -m agent.cli renewals 30
    python -m agent.cli renewals 7
    python -m agent.cli renewals 0

Troubleshooting
- Report missing: ensure Templates.DocTemplateId is set and REPORTS_FOLDER_ID is valid.
- Stripe error: check STRIPE_SECRET_KEY and Checkout Session permissions.
- Form handler not firing: ensure trigger installed and field names match exactly.

Staging and production (optional)
- Duplicate the Sheet and Doc for staging.
- Add a second set of secrets with suffix STAGING.
- Duplicate workflows targeting staging secrets.
