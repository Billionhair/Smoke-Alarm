from __future__ import annotations
import hmac
import hashlib
import json
from .config import cfg

class StripeWebhook:
    """Validate and parse Stripe webhook events."""

    def __init__(self, secret: str | None = None) -> None:
        self.secret = secret or cfg.stripe_webhook_secret
        if not self.secret:
            raise RuntimeError("Missing STRIPE_WEBHOOK_SECRET")

    def verify(self, payload: bytes, header: str) -> dict:
        try:
            items = dict(item.split("=") for item in header.split(","))
            timestamp = items["t"]
            sig = items["v1"]
        except Exception as exc:
            raise RuntimeError("Invalid signature header") from exc
        signed = f"{timestamp}.{payload.decode()}".encode()
        expected = hmac.new(self.secret.encode(), signed, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, sig):
            raise RuntimeError("Signature mismatch")
        return json.loads(payload)
