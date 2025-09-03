from __future__ import annotations
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
from .google_auth import get_credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class GmailClient:
    """Send email via the Gmail API using a service account."""

    def __init__(self) -> None:
        creds = get_credentials(SCOPES)
        self.service = build("gmail", "v1", credentials=creds)

    def send(self, to: str, subject: str, body: str) -> dict:
        msg = MIMEText(body)
        msg["to"] = to
        msg["subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        return (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": raw})
            .execute()
        )
