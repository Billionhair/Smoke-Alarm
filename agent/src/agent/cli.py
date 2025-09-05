"""Command-line interface for the Smoke Alarm agent."""

from datetime import date
from typing import List

import logging
import typer

from . import backup as backup_mod
from . import health as health_mod
from . import renewals as renewals_mod
from . import stripe_sync as stripe_sync_mod
from .config import cfg
from .router import optimize_route, plan_multi_day_routes
from .stripe_client import StripeClient
from .sheets import SheetDB
from .sms_client import SMSClient
from .routing import planner
from . import outreach
 codex/identify-repo-features-and-builds-016493
from .logging import configure as configure_logging

codex/identify-repo-features-and-builds-vj8jec
from .logging import configure as configure_logging

 main
 main


app = typer.Typer(help="Smoke Alarm AI Agent CLI")
logger = logging.getLogger("agent")


@app.callback()
def main(ctx: typer.Context) -> None:
    """Initialize common logging configuration."""
    configure_logging()


@app.command()
def ping() -> None:
    """Simple connectivity check printing the configured sheet ID."""
    logger.info("Agent online. Sheet: %s", cfg.sheet_id)
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def renewals(days: int) -> None:
    """Send reminders for inspections due in ``days`` days."""
    count = renewals_mod.send(days)
    logger.info("%s properties due in %s days.", count, days)


@app.command()
def overdue(days: int) -> None:
    """Send overdue chasers ``days`` days after due (negative)."""
    count = renewals_mod.chase(days)
    logger.info("Chased %s overdue at %s days.", count, abs(days))


@app.command()
def backup(
    out: str = typer.Option("/tmp/backup", "--out", help="Directory for CSV exports"),
) -> None:
    """Export core tabs to ``out`` as CSV files."""
    backup_mod.backup(out)
    logger.info("Backup written to %s", out)


@app.command()
def stripe_sync(days: int = typer.Option(14, "--days", help="Look back this many days")) -> None:
    """Reconcile Stripe payments with invoices."""
    stripe_sync_mod.sync(days)
    logger.info("Stripe sync completed for last %s days", days)


@app.command()
def health() -> None:
    """Run sheet invariant checks."""
    health_mod.check()
    logger.info("Health checks completed")
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def route(
    addresses: List[str] = typer.Argument(
        None, help="Addresses to visit; omit and use --date to fetch from sheet"
    ),
    days: int = typer.Option(1, "--days", help="Plan routes over this many days"),
    responses_file: str = typer.Option(
        None,
        "--responses-file",
        help="Optional JSON mapping of address to confirmation (true/false)",
    ),
    date_str: str = typer.Option(
        None,
        "--date",
        help="Load properties due on this date (YYYY-MM-DD or 'today')",
    ),
):
    """Plan an optimized route for given addresses or due properties.

    If ``--date`` is supplied, properties due on that date are loaded from the
    sheet. When ``--days`` is greater than one, the stops are distributed across
    multiple days using confirmation responses from ``--responses-file``.
    """
    if not addresses:
        if not date_str:
            logger.warning("Provide at least one address or use --date to load due properties")
            raise typer.Exit(code=1)
        db = SheetDB()
        target = date.today().isoformat() if date_str == "today" else date_str
        props = db.list_properties_due(target)
        addresses = [db.format_address(p) for p in props]
        if not addresses:
            logger.info("No properties due for %s", target)
            raise typer.Exit(code=0)

    if days <= 1:
        if len(addresses) < 2:
            logger.error("At least two addresses required")
            raise typer.Exit(code=1)
        result = optimize_route(addresses)
        for i, addr in enumerate(result.order, start=1):
            logger.info("%s. %s", i, addr)
        logger.info("Total distance: %.1f km", result.distance_km)
        logger.info("Total duration: %.1f min", result.duration_min)
        logger.info(result.url)
    else:
        import json

        responses = {}
        if responses_file:
            with open(responses_file) as f:
                responses = json.load(f)
        plan = plan_multi_day_routes(addresses, days=days, responses=responses)
        for day in sorted(plan.daily):
            res = plan.daily[day]
            logger.info("Day %s:", day)
            for i, addr in enumerate(res.order, start=1):
                logger.info("  %s. %s", i, addr)
            logger.info("  Distance: %.1f km", res.distance_km)
            logger.info("  Duration: %.1f min", res.duration_min)
            logger.info("  Map: %s", res.url)
        if plan.canceled:
            logger.info("Cancelled or unconfirmed: %s", ", ".join(plan.canceled))
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def invoice(property: str, alarms: int = 0, batteries: int = 0) -> None:
    """Create a Stripe checkout for a property service visit."""
    db = SheetDB()
    sc = StripeClient()
    prop = db.get_property(property)
    client = db.get_client(prop["ClientID"])
    items = [
        {
            "description": "Annual smoke alarm compliance check",
            "quantity": 1,
            "unitAmountCents": int(cfg.price_service_cents),
        }
    ]
    if int(alarms) > 0:
        items.append(
            {
                "description": "Photoelectric alarm replacement",
                "quantity": int(alarms),
                "unitAmountCents": int(cfg.price_alarm_cents),
            }
        )
    if int(batteries) > 0:
        items.append(
            {
                "description": "9V battery replacement",
                "quantity": int(batteries),
                "unitAmountCents": int(cfg.price_battery_cents),
            }
        )
    inv = sc.create_checkout(items)
    db.append_invoice(client["ClientID"], property, inv)
    logger.info(inv["url"])
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def leads_import(csv_path: str) -> None:
    """Import leads from a CSV file into the Leads sheet."""
    import pandas as pd

    df = pd.read_csv(csv_path)
    df.columns = pd.Index([c.strip().title() for c in df.columns])
    keep = ["Name", "Email", "Phone"]
    for k in keep:
        if k not in df.columns:
            df[k] = ""
    rows = df[keep].fillna("").values.tolist()
    if not rows:
        logger.warning("No leads found")
        return
    db = SheetDB()
    db._append("Leads", rows)
    logger.info("Imported %s leads.", len(rows))
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def leads_enrich(csv_path: str) -> None:
    """Normalize and de-duplicate a CSV of leads."""
    import pandas as pd

    df = pd.read_csv(csv_path)
    df.columns = pd.Index([c.strip().title() for c in df.columns])
    keep = ["Name", "Phone", "Email", "Website", "Suburb"]
    for k in keep:
        if k not in df.columns:
            df[k] = ""
    df = df[keep].drop_duplicates().reset_index(drop=True)
    out = csv_path.replace(".csv", "_enriched.csv")
    df.to_csv(out, index=False)
    logger.info("Saved %s", out)
 codex/identify-repo-features-and-builds-016493


 main

@app.command()
def outreach_sms(
    list: str,
    message: str = "We handle annual smoke alarm checks for $129/property. Trial 2-3 this month? Reply YES.",
) -> None:
    """Send a marketing SMS to numbers in ``list``."""
    import pandas as pd

    sms = SMSClient()
    df = pd.read_csv(list)
    sent = 0
    for _, r in df.iterrows():
        phone = str(r.get("Phone", "")).strip()
        if not phone or phone.lower() == "nan":
            continue
        try:
            sms.send(phone, message)
            sent += 1
        except Exception as e:
            logger.error("SMS error: %s", e)
    logger.info("SMS sent: %s", sent)


@app.command()
def outreach_sequence(name: str) -> None:
    """Run the outreach sequence ``name`` for all leads."""
    db = SheetDB()
    leads = db._rows("Leads")
    activities: set[tuple[str, int]] = set()

    def sms(to: str, body: str) -> None:
        logger.info("SMS to %s -> %s", to, body)

    outreach.run_sequence(name, leads, activities, send_sms=sms)


@app.command()
def plan_routes_simple(addresses: List[str]) -> None:
    """Plan a simple route for ``addresses`` and print the order."""
    res = planner.plan_route(addresses)
    for i, addr in enumerate(res["order"], start=1):
        logger.info("%s. %s", i, addr)
    if res["url"]:
        logger.info(res["url"])

 codex/identify-repo-features-and-builds-016493


@app.command()
def outreach_sequence(name: str) -> None:
    """Run the outreach sequence ``name`` for all leads."""
    db = SheetDB()
    leads = db._rows("Leads")
    activities: set[tuple[str, int]] = set()

    def sms(to: str, body: str) -> None:
        print("SMS to", to, "->", body)

    outreach.run_sequence(name, leads, activities, send_sms=sms)


@app.command()
def plan_routes_simple(addresses: List[str]) -> None:
    """Plan a simple route for ``addresses`` and print the order."""
    res = planner.plan_route(addresses)
    for i, addr in enumerate(res["order"], start=1):
        print(f"{i}. {addr}")
    if res["url"]:
        print(res["url"])
 main

if __name__ == "__main__":
    app()
