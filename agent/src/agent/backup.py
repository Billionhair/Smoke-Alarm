from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from .sheets import SheetDB

TABS: List[str] = [
    "Clients",
    "Properties",
    "Inspections",
    "Invoices",
    "LineItems",
    "Settings",
    "Templates",
]

def backup(out_dir: str) -> None:
    """Export core tabs from the Google Sheet to ``out_dir`` as CSV files."""
    db = SheetDB()
    dest = Path(out_dir)
    dest.mkdir(parents=True, exist_ok=True)
    for tab in TABS:
        rows = db._rows(tab)
        headers = db._headers(tab)
        with open(dest / f"{tab}.csv", "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
