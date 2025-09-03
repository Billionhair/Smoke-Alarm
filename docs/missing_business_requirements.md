# Missing Business Requirements

The repository lacks several components required for a production smoke alarm compliance business:

- **Routing resilience**: add caching and retry logic so the route CLI remains stable even when external services fail.
- **Operational commands**: implement renewals, outreach, invoicing, and messaging flows in the agent.
- **Testing and CI**: expand unit tests, add integration tests for Sheets and routing, and wire them into GitHub Actions.
- **Apps Script pipeline**: compile TypeScript to JavaScript and deploy via `clasp` while keeping Google Sheets the source of truth.
- **Documentation suite**: quickstart, contribution, security contact, and support docs collected into a docs site.
- **Release process**: semantic versioning and changelog so deploys can be tracked and rolled back safely.
- **Security hardening**: secret scanning, OAuth scope review, and SBOM generation for Python and Apps Script code.
- **Observability**: structured logs, metrics, and tracing to hit the 99.9% availability goal.
- **Data migration path**: repository layer and migrations to transition from Sheets to Postgres without breaking the UI.
- **Operator console**: accessible React interface for daily planning that respects the battery-only scope.

Addressing these gaps will provide a stable foundation for the business while preserving the battery-only focus and clean path from Google Sheets to a database later.
