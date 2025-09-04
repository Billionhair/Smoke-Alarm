from __future__ import annotations

from datetime import datetime, timedelta

from .sheets import SheetDB
from .stripe_client import StripeClient


def update_invoice_status(db: SheetDB, invoice_id: str, paid: bool = True) -> None:
    """Update the ``Invoices`` row matching ``invoice_id``."""
    idx, row = db.find_row("Invoices", "InvoiceID", invoice_id)
    if idx is None:
        return
    row["Status"] = "Paid" if paid else "Unpaid"
    row["PaidAt"] = datetime.utcnow().isoformat() if paid else ""
    db.update_row("Invoices", idx, row)


def sync(days: int = 14) -> None:
    """Reconcile recent Stripe Checkout sessions with invoices."""
    sc = StripeClient()
    db = SheetDB()
    since = datetime.utcnow() - timedelta(days=days)
    sessions = sc.list_checkout_sessions(since) if hasattr(sc, "list_checkout_sessions") else []
    for sess in sessions:
        inv_id = sess.get("client_reference_id")
        if inv_id and sess.get("payment_status") == "paid":
            update_invoice_status(db, inv_id, paid=True)
