AGENTS.md (agent services)

Scope: service modules that talk to external systems.

OSRM client

Base URL from OSRM_BASE_URL

Use /table for matrix and /route for geometry and ETA

Timeout 5 seconds per request

Retries with backoff for transient errors

Strict schema for responses

Never call the public OSRM demo in production

Geocoding

Base URL from NOMINATIM_BASE_URL

Always send GEOCODE_USER_AGENT

Rate limit using GEOCODE_RPS

Retries with backoff

Cache successful results on disk or in memory

Sheets

Use gspread with service account at GOOGLE_SA_PATH

Read jobs by date and write back assignments and ETAs only in allowed columns

Handle network failures with retries and idempotent writes

Notifications

Use Apprise URLs from APPRISE_URLS

Support dry run mode for tests

Testing

Mock HTTP at module boundary

Add integration tests that hit localhost OSRM if available
