import typer
from typing import List
from datetime import date, datetime, timedelta
from .config import cfg
from .sheets import SheetDB
from .stripe_client import StripeClient
from .sms_client import SMSClient
from .router import optimize_route, plan_multi_day_routes

app = typer.Typer(help="Smoke Alarm AI Agent CLI")

@app.command()
def ping():
    print("Agent online. Sheet:", cfg.sheet_id)

@app.command()
def renewals(days: int):
    db = SheetDB()
    today = date.today()
    target = today + timedelta(days=days)
    inspections = db.list_inspections()
    hits = []
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
    print(f"{len(hits)} properties due in {days} days.")
    sms = SMSClient()
    for ins in hits:
        prop = db.get_property(ins["PropertyID"])
        client = db.get_client(prop["ClientID"])
        phone = client.get("Phone")
        if not phone:
            continue
        msg = f"Reminder: Property {ins['PropertyID']} due for smoke alarm check on {target.isoformat()}."
        try:
            sms.send(phone, msg)
            print("SMS sent to", phone)
        except Exception as e:
            print("SMS error:", e)

@app.command()
def route(
    addresses: List[str] = typer.Argument(...),
    days: int = typer.Option(1, "--days", help="Plan routes over this many days"),
    responses_file: str = typer.Option(
        None,
        "--responses-file",
        help="Optional JSON mapping of address to confirmation (true/false)",
    ),
):
    if len(addresses) < 1:
        print("At least one address required")
        raise typer.Exit(code=1)

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
def invoice(property: str, alarms: int = 0, batteries: int = 0):
    db = SheetDB()
    sc = StripeClient()
    prop = db.get_property(property)
    client = db.get_client(prop["ClientID"])
    items = [{
        "description": "Annual smoke alarm compliance check",
        "quantity": 1,
        "unitAmountCents": int(cfg.price_service_cents),
    }]
    if int(alarms) > 0:
        items.append({"description": "Photoelectric alarm replacement", "quantity": int(alarms), "unitAmountCents": int(cfg.price_alarm_cents)})
    inv = sc.create_checkout(items)
    db.append_invoice(client["ClientID"], property, inv)
    print(inv["url"])

@app.command()
def leads_enrich(csv_path: str):
    import pandas as pd
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().title() for c in df.columns]
    keep = ["Name","Phone","Email","Website","Suburb"]
    for k in keep:
        if k not in df.columns:
            df[k] = ""
    df = df[keep].drop_duplicates().reset_index(drop=True)
    out = csv_path.replace(".csv","_enriched.csv")
    df.to_csv(out, index=False)
    print("Saved", out)

@app.command()
def outreach_sms(list: str, message: str = "We handle annual smoke alarm checks for $129/property. Trial 2-3 this month? Reply YES."):
    import pandas as pd
    sms = SMSClient()
    df = pd.read_csv(list)
    sent = 0
    for _, r in df.iterrows():
        phone = str(r.get("Phone","")).strip()
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
