from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Set, Tuple

from .logging import configure

Logger = configure()


def render_template(path: str, context: Dict[str, str]) -> str:
    base = Path(__file__).resolve().parents[2] / "templates"
    path_obj = base / path
    text = path_obj.read_text()
    for key, value in context.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def run_sequence(
    name: str,
    leads: Iterable[Dict[str, str]],
    activities: Set[Tuple[str, int]],
    *,
    send_sms: Callable[[str, str], None] | None = None,
    send_email: Callable[[str, str], None] | None = None,
    today: datetime | None = None,
) -> List[Tuple[str, str]]:
    """Run outreach sequence ``name`` for ``leads``.

    ``activities`` tracks (lead_id, day) pairs already processed to enforce
    idempotency. The function returns a list of (lead_id, channel) tuples for
    steps that were executed.
    """
    today = today or datetime.utcnow()
    seq_path = Path(__file__).with_name("sequences.json")
    sequences = json.loads(seq_path.read_text())
    steps = sequences[name]

    performed: List[Tuple[str, str]] = []
    for lead in leads:
        created = datetime.fromisoformat(lead.get("CreatedAt"))
        for step in steps:
            due = created + timedelta(days=step["day"])
            if due.date() != today.date():
                continue
            marker = (lead["LeadID"], step["day"])
            if marker in activities:
                continue
            tmpl = render_template(step["template"], {"name": lead.get("Name", "")})
            if step["channel"] == "sms" and send_sms:
                send_sms(lead["Phone"], tmpl)
            elif step["channel"] == "email" and send_email:
                send_email(lead["Email"], tmpl)
            activities.add(marker)
            performed.append((lead["LeadID"], step["channel"]))
            Logger.info("%s step for %s", step["channel"], lead["LeadID"])
    return performed
