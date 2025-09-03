# Smoke Alarm Compliance Monorepo

## Contents
- apps_script: Google Sheets bound Apps Script for reports, invoices, SMS, reminders.
- agent: Python AI agent for renewals, routing, outreach, and Stripe invoicing.
- sheets: CSV tab schemas to initialise the Sheet.
- templates: Google Doc text templates for report and invoice.
- .github/workflows: CI for daily agent runs and Apps Script deployments.
- scripts: helper for clasp pushes.

## First run quick start
1) Create target Google Sheet and import CSVs from sheets to create tabs. Or run oneTimeSetup in Apps Script to create headers.
2) Create a Google Doc from templates/Compliance_Report_TEMPLATE.txt. Put its Doc ID into Templates sheet row with Name=ComplianceReport.
3) Fill Settings tab: BUSINESS_*, GST_RATE, PRICE_* (in cents), REPORTS_FOLDER_ID, provider keys.
4) Authorise Apps Script scopes when prompted. Run ensureTriggers once.
5) Add GitHub Secrets listed here and push.

## Safety and scope
- Battery-only workflow. No electrical work. Refer hardwired to a licensed electrician.

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
## Routing
Use the agent's `route` command to optimise visits. Addresses may be provided directly or loaded from the Sheet using `--date`.

Routing
-------
Use the agent's ``route`` command to optimise visits. Addresses may be
provided directly or loaded from the Sheet using ``--date``.
 main

```
PYTHONPATH=agent/src python -m agent.cli route [ADDRESS...]
                             [--date YYYY-MM-DD|today]
                             [--days N]
                             [--responses-file FILE]
```

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
- `--date` loads properties due on the given day instead of supplying addresses on the command line.
- `--days` splits confirmed stops across multiple days.
- `--responses-file` points to a JSON mapping of address to confirmation (`true` or `false`) used when planning multi-day routes.

Routing relies on the public OSRM demo server and OpenStreetMap's Nominatim geocoder. Internet access is required, and heavy usage should provide self-hosted services.

- ``--date`` loads properties due on the given day instead of supplying
  addresses on the command line.
- ``--days`` splits confirmed stops across multiple days.
- ``--responses-file`` points to a JSON mapping of address to
  confirmation (``true`` or ``false``) used when planning multi-day
  routes.

Routing relies on the public OSRM demo server and OpenStreetMap's
Nominatim geocoder. Internet access is required, and heavy usage should
provide self-hosted services.
 main

Example single-day output:

```
1. 10 Downing St, London
2. Buckingham Palace, London
3. St Paul's Cathedral, London
Total distance: 5.5 km
Total duration: 15.1 min
 codex/update-readme.md-with-documentation-and-examples-ldgzgw
Map: https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London%7CBuckingham+Palace%2C+London

https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London%7CBuckingham+Palace%2C+London
 main
```

Example multi-day output:

```
Day 1:
  1. 10 Downing St, London
  2. St Paul's Cathedral, London
  Distance: 2.9 km
  Duration: 8.0 min
  Map: https://www.google.com/maps/dir/?api=1&destination=St+Paul%27s+Cathedral%2C+London&waypoints=10+Downing+St%2C+London
 codex/update-readme.md-with-documentation-and-examples-ldgzgw


 main
Day 2:
  1. Buckingham Palace, London
  2. London Eye, London
  Distance: 2.4 km
  Duration: 6.6 min
  Map: https://www.google.com/maps/dir/?api=1&destination=London+Eye%2C+London&waypoints=Buckingham+Palace%2C+London
```

 codex/update-readme.md-with-documentation-and-examples-ldgzgw
## Testing

Testing
-------
 main
Run the unit tests from the repository root:

```
PYTHONPATH=agent/src python -m unittest discover agent/tests -v
```
