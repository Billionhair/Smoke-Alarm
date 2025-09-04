from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from .ids import new_id

STAGES = ["New", "Contacted", "Trial", "Active", "Renewal"]


def score_lead(lead: Dict[str, str]) -> int:
    """Return a simple score based on lead attributes.

    The rules loosely follow the description in the design document. Each rule
    contributes to the score if the condition evaluates to truthy.
    """
    score = 0
    email = lead.get("Email", "")
    phone = lead.get("Phone", "")
    doors = int(lead.get("Doors", 0) or 0)
    if "@" in email:
        score += 30
    if phone:
        score += 20
    if doors > 100:
        score += 20
    if lead.get("Engaged"):
        score += 20
    if lead.get("Source", "").lower() == "inbound":
        score += 10
    return score


def advance_stage(lead: Dict[str, str], new_stage: str) -> Dict[str, str]:
    """Advance ``lead`` to ``new_stage`` and update timestamps.

    ``lead`` is modified in-place and returned for convenience. A ``ValueError``
    is raised if ``new_stage`` is not part of ``STAGES``.
    """
    if new_stage not in STAGES:
        raise ValueError(f"Unknown stage: {new_stage}")
    lead["Stage"] = new_stage
    lead["LastActivityAt"] = datetime.utcnow().isoformat()
    if new_stage == "New":
        lead["NextActionAt"] = (datetime.utcnow() + timedelta(days=2)).isoformat()
    else:
        lead["NextActionAt"] = ""
    return lead


def upsert_company_contact(
    lead: Dict[str, str],
    companies: List[Dict[str, str]],
    contacts: List[Dict[str, str]],
) -> Tuple[str, str]:
    """Ensure company and contact exist, returning their IDs.

    ``companies`` and ``contacts`` are mutated in-place to include new entries
    when necessary. Deduplication uses company ``Name`` and contact ``Email``.
    """
    company_name = lead.get("CompanyName", "").strip()
    contact_email = lead.get("Email", "").strip().lower()

    company_id = ""
    for c in companies:
        if c.get("Name", "").strip().lower() == company_name.lower():
            company_id = c["CompanyID"]
            break
    if not company_id:
        company_id = new_id("C")
        companies.append({"CompanyID": company_id, "Name": company_name})

    contact_id = ""
    for c in contacts:
        if c.get("Email", "").strip().lower() == contact_email:
            contact_id = c["ContactID"]
            break
    if not contact_id:
        contact_id = new_id("CT")
        contacts.append({"ContactID": contact_id, "CompanyID": company_id, "Email": contact_email})
    return company_id, contact_id
