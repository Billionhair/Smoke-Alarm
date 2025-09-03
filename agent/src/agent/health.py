from __future__ import annotations

from .sheets import SheetDB

REQUIRED_COLUMNS = {
    "Clients": ["ClientID", "Name"],
    "Properties": ["PropertyID", "ClientID", "NextDueDate"],
    "Inspections": ["InspectionID", "PropertyID", "NextDueDate"],
}


def check() -> None:
    """Verify required tabs and columns exist in the sheet."""
    db = SheetDB()
    for tab, cols in REQUIRED_COLUMNS.items():
        headers = db._headers(tab)
        missing = [c for c in cols if c not in headers]
        if missing:
            raise RuntimeError(f"{tab} missing columns: {', '.join(missing)}")
