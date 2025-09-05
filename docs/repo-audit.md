# Repository Audit

## Top-level Structure

- `agent/` – Python source for automation agent, tests, templates.
- `apps_script/` – Google Apps Script utilities.
- `apps_script_addons/` – Additional Apps Script modules.
- `docs/` – Project documentation and rules.
- `gui/` – Streamlit prototypes and other UI experiments.
- `sheets/` – Spreadsheet templates and exports.
- `scripts/` – Shell and Python helper scripts.
- `templates/` – Document templates.
- `workflows/` – Automation scripts and GitHub workflows.

## Agent CLI Commands

The CLI is defined in `agent/src/agent/cli.py` and exposed via `typer`.

- `ping` – connectivity check reporting configured sheet ID.
- `renewals DAYS` – send reminders for inspections due in `DAYS` days.
- `overdue DAYS` – chase overdue inspections `DAYS` days after due.
- `backup --out PATH` – export core sheets to CSV files in `PATH`.
- `stripe-sync --days N` – reconcile Stripe payments for last `N` days.
- `health` – run spreadsheet invariant checks.
- `route [ADDRESSES] [--date YYYY-MM-DD] [--days N] [--responses-file FILE]` – optimize routes for given addresses or sheet properties.
- `invoice PROPERTY_ID [--alarms N] [--batteries N]` – create Stripe checkout for a property.

## Tests

Tests reside under `agent/tests/` and are executed with `pytest`. Current CI uses the workflow `.github/workflows/tests.yml` which installs dependencies, runs `ruff`, `mypy`, and `pytest`.

## External Services and Data Sources

- **Google Sheets API** via `googleapiclient` for data storage (`agent/src/agent/sheets.py`).
- **Stripe API** for payment processing (`agent/src/agent/stripe_client.py`).
- **SMS Providers** ClickSend or Twilio (`agent/src/agent/sms_client.py`).
- **Geocoding** via OpenStreetMap Nominatim (`agent/src/agent/router.py`).
- **Routing** via OSRM or Mapbox (`agent/src/agent/router_providers.py`).

These services may have rate limits (e.g. Nominatim requires rate limiting) and require API keys or user agents as configured in environment variables.
