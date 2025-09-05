AGENTS.md (gui)

Scope: Streamlit dispatcher UI.

Run
streamlit run gui/streamlit_app.py

UI rules

Inputs for day, vehicles, shift bounds

Show table of jobs and current plan

Button Optimize that calls solver through python or API

Map preview of plan

Links to Google Maps for crews

No secrets in code. Read from env only.

Keep first contentful paint fast. Cache OSRM table and geocodes where possible.

Tests

Keep logic in pure functions and test them in agent tests

UI smoke test can run in CI with headless mode if practical
