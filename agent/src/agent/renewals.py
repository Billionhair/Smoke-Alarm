from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import List

from .sheets import SheetDB
from .sms_client import SMSClient


def send(days: int) -> int:
    """Send renewal reminders for inspections due in ``days`` days."""
    db = SheetDB()
    today = date.today()
    target = today + timedelta(days=days)
    inspections = db.list_inspections()
    hits: List[dict] = []
    for ins in inspections:
        next_due = ins.get("NextDueDate")
        if not next_due:
            continue
        try:
            nd = datetime.fromisoformat(str(next_due)).date()
        except Exception:
            continue
        if nd == target:
            hits.append(ins)
    sms = SMSClient()
    for ins in hits:
        prop = db.get_property(ins["PropertyID"])
        client = db.get_client(prop["ClientID"])
        phone = client.get("Phone")
        if not phone:
            continue
        msg = (
            f"Reminder: Property {ins['PropertyID']} due for smoke alarm check on "
            f"{target.isoformat()}."
        )
        try:
            sms.send(phone, msg)
        except Exception:
            pass
    return len(hits)


def chase(days: int) -> int:
    """Send overdue chasers ``days`` days after due (negative days)."""
    if days >= 0:
        raise ValueError("days must be negative for overdue chasers")
    return send(days)
