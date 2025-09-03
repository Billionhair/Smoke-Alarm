# Platform integrations

## Current capabilities

- **Google Sheets and Drive**: The Python `SheetDB` and Apps Script scripts use service account credentials to read and write sheets and to store generated reports in Drive.
- **Routing and geocoding**: `router.py` calls OSRM for trip optimisation and Nominatim for address lookup, producing Google Maps links for operators.
- **SMS providers**: `SMSClient` selects ClickSend or Twilio based on configuration and Apps Script provides a matching `sendSMS_` helper.
- **Payments**: `StripeClient` creates checkout sessions and Apps Script invoices append results back to the sheet.
- **Email**: Apps Script uses `sendEmail_` to deliver reports and reminders via Gmail. The Python agent can also send email directly via a new `GmailClient`.
- **Webhook processing**: `StripeWebhook` verifies payment notifications for automatic invoice reconciliation.
- **Routing adapters**: `router` selects between OSRM and Mapbox providers via configuration for improved reliability.
- **Data repository**: `SheetRepository` is the default Google Sheets-backed store with an optional `PostgresRepository`.
- **Scheduling**: `Scheduler` can create inspection events in Google Calendar.

## Gaps and proposals

- **Additional providers**: add OpenRouteService support and pluggable email/SMS backends to avoid vendor lock-in.
- **Monitoring**: integrate logging and error tracking (e.g., Sentry) for all external requests.
- **Background queue**: use a lightweight job queue (RQ, Celery) to retry failed communications.
