# Runbook

## Local Setup
1. Install Python 3.11 and [pre-commit](https://pre-commit.com/).
2. Create a virtual environment and install dependencies:
   ```bash
   cd agent
   pip install -r requirements.txt
   pre-commit install
   ```
3. Configure environment variables in a `.env` file (see `agent/src/agent/config.py`).
4. Start self-hosted OSRM (see `docs/osrm-self-host.md`).

## Solving Routes
1. Ensure `OSRM_BASE_URL` and `NOMINATIM_BASE_URL` are reachable.
2. Use the CLI to plan routes:
   ```bash
   PYTHONPATH=agent/src python -m agent.cli route "Address1" "Address2"
   ```
3. For multi-day planning with confirmations:
   ```bash
   PYTHONPATH=agent/src python -m agent.cli route --date 2024-01-01 --days 3 --responses-file responses.json
   ```
4. The dispatcher UI can be launched with:
   ```bash
   streamlit run dispatcher_ui/app.py
   ```

## Daily Operations
- `ping` to verify environment.
- `renewals` and `overdue` to send reminders.
- `stripe-sync` to reconcile payments.
- `backup` to export CSV backups.
- `health` to run data integrity checks.
- `python api/main.py` with uvicorn to expose `/solve` API:
  ```bash
  uvicorn api.main:app --reload
  ```
