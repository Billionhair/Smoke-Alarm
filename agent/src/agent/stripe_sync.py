from __future__ import annotations

from datetime import datetime, timedelta

from .sheets import SheetDB
from .stripe_client import StripeClient


def sync(days: int = 14) -> None:
    """Reconcile recent Stripe Checkout sessions with invoices."""
    sc = StripeClient()
    db = SheetDB()
    since = datetime.utcnow() - timedelta(days=days)
    # Placeholder: real implementation would call Stripe's API.
    print("Stripe sync placeholder since", since.isoformat())
    _ = (sc, db)
