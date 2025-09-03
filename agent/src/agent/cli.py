import typer
from datetime import date, datetime, timedelta
from .config import cfg
from .sheets import SheetDB
from .stripe_client import StripeClient
from .sms_client import SMSClient
from .router import build_route_url

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
def route(date_str: str = "today"):
    """Build a map link for properties due on the given date.

    DATE_STR may be "today" or a date in YYYY-MM-DD format.
    """
    db = SheetDB()
    if date_str == "today":
        target = date.today()
    else:
        try:
            target = datetime.fromisoformat(date_str).date()
        except ValueError:
            print("Date must be YYYY-MM-DD or 'today'.")
            raise typer.Exit(code=1)
    props = db.list_properties_due(target.isoformat())
    addrs = [db.format_address(p) for p in props]
    if not addrs:
        print("No properties due for", target.isoformat())
        raise typer.Exit(code=0)
    url = build_route_url(addrs)
    print(url)

@app.command()
def invoice(property: str, alarms: int = 0, batteries: int = 0):
    db = SheetDB()
    sc = StripeClient()
    prop = db.get_property(property)
    client = db.get_client(prop["ClientID"])
    items = [{"description": "Annual smoke alarm compliance check", "quantity": 1, "unitAmountCents": int(cfg.price_service_cents)}]
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
