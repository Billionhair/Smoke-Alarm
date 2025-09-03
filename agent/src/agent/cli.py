"""Command-line interface for the Smoke Alarm agent."""

from datetime import date
from typing import List

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


app = typer.Typer(help="Smoke Alarm AI Agent CLI")

@app.command()
def ping():
    """Simple connectivity check printing the configured sheet ID."""
    print("Agent online. Sheet:", cfg.sheet_id)

@app.command()
def renewals(days: int) -> None:
    """Send reminders for inspections due in ``days`` days."""
    count = renewals_mod.send(days)
    print(f"{count} properties due in {days} days.")


@app.command()
def overdue(days: int) -> None:
    """Send overdue chasers ``days`` days after due (negative)."""
    count = renewals_mod.chase(days)
    print(f"Chased {count} overdue at {abs(days)} days.")


@app.command()
def backup(out: str = typer.Option("/tmp/backup", "--out", help="Directory for CSV exports")) -> None:
    """Export core tabs to ``out`` as CSV files."""
    backup_mod.backup(out)


@app.command()
def stripe_sync(days: int = typer.Option(14, "--days", help="Look back this many days")) -> None:
    """Reconcile Stripe payments with invoices."""
    stripe_sync_mod.sync(days)


@app.command()
def health() -> None:
    """Run sheet invariant checks."""
    health_mod.check()

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
            print("Provide at least one address or use --date to load due properties")
            raise typer.Exit(code=1)
        db = SheetDB()
        target = date.today().isoformat() if date_str == "today" else date_str
        props = db.list_properties_due(target)
        addresses = [db.format_address(p) for p in props]
        if not addresses:
            print("No properties due for", target)
            raise typer.Exit(code=0)

    if days <= 1:
        if len(addresses) < 2:
            print("At least two addresses required")
            raise typer.Exit(code=1)
        result = optimize_route(addresses)
        for i, addr in enumerate(result.order, start=1):
            print(f"{i}. {addr}")
        print(f"Total distance: {result.distance_km:.1f} km")
        print(f"Total duration: {result.duration_min:.1f} min")
        print(result.url)
    else:
        import json

        responses = {}
        if responses_file:
            with open(responses_file) as f:
                responses = json.load(f)
        plan = plan_multi_day_routes(addresses, days=days, responses=responses)
        for day in sorted(plan.daily):
            res = plan.daily[day]
            print(f"Day {day}:")
            for i, addr in enumerate(res.order, start=1):
                print(f"  {i}. {addr}")
            print(f"  Distance: {res.distance_km:.1f} km")
            print(f"  Duration: {res.duration_min:.1f} min")
            print(f"  Map: {res.url}")
        if plan.canceled:
            print("Cancelled or unconfirmed:", ", ".join(plan.canceled))

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
    print(inv["url"])

@app.command()
def leads_enrich(csv_path: str) -> None:
    """Normalize and de-duplicate a CSV of leads."""
    import pandas as pd

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().title() for c in df.columns]
    keep = ["Name", "Phone", "Email", "Website", "Suburb"]
    for k in keep:
        if k not in df.columns:
            df[k] = ""
    df = df[keep].drop_duplicates().reset_index(drop=True)
    out = csv_path.replace(".csv", "_enriched.csv")
    df.to_csv(out, index=False)
    print("Saved", out)

@app.command()
def outreach_sms(list: str, message: str = "We handle annual smoke alarm checks for $129/property. Trial 2-3 this month? Reply YES.") -> None:
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
            print("SMS error:", e)
    print("SMS sent:", sent)

if __name__ == "__main__":
    app()
