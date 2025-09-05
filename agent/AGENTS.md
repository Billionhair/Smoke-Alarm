AGENTS.md (agent)

Scope: Python package code under agent.

Module map

src/agent/cli.py CLI entry points

src/agent/services OSRM client, geocode adapter, sheets sync, notifications

src/agent/optimizer VRP and time window solver

src/agent/reports.py HTML to PDF reports

tests unit and integration tests

Contracts

Python 3.11 or newer

All public functions and data models are type hinted

Use Pydantic models for external IO and configs

Use requests or httpx with timeouts and retry policy

Error policy

Fail fast for missing env or required columns

Wrap external HTTP errors with clear messages

Never swallow exceptions silently

Return value must not be None unless documented

Performance

Cache OSRM table calls when matrix size repeats

Rate limit geocoding at 1 rps

Keep cold start under 2 seconds for CLI

Logging

Use logging.getLogger(name)

Include route id or batch id in log context where possible

Testing

Unit tests in agent/tests for each module

Use Hypothesis for parsers and small pure functions

Use pytest markers to skip slow tests by default

Acceptance

ruff and mypy pass

CLI route command works against a small sample csv

Reports render a valid PDF in build folder
