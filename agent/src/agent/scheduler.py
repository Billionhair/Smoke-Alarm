from __future__ import annotations
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from .google_auth import get_credentials
from .config import cfg

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

class Scheduler:
    """Schedule inspection events using Google Calendar."""

    def __init__(self) -> None:
        creds = get_credentials(SCOPES)
        self.service = build("calendar", "v3", credentials=creds)
        self.calendar_id = cfg.calendar_id

    def schedule_inspection(
        self, summary: str, start: datetime, duration_minutes: int = 30
    ) -> dict:
        end = start + timedelta(minutes=duration_minutes)
        event = {
            "summary": summary,
            "start": {"dateTime": start.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end.isoformat(), "timeZone": "UTC"},
        }
        return (
            self.service.events()
            .insert(calendarId=self.calendar_id or "primary", body=event)
            .execute()
        )
