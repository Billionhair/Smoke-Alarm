from __future__ import annotations
from typing import List
from googleapiclient.discovery import build
from .google_auth import get_credentials
from .config import cfg

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

def _sheets():
    creds = get_credentials(SCOPES)
    return build("sheets","v4", credentials=creds).spreadsheets()

class SheetDB:
    def __init__(self):
        self.sid = cfg.sheet_id
        self.ss = _sheets()

    def _get(self, sheet, range_a1):
        return self.ss.values().get(spreadsheetId=self.sid, range=f"{sheet}!{range_a1}").execute().get("values", [])

    def _append(self, sheet, rows: List[List[str]]):
        body = {"values": rows}
        return self.ss.values().append(spreadsheetId=self.sid, range=f"{sheet}!A1", valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body=body).execute()

    def _headers(self, sheet):
        vals = self._get(sheet, "1:1")
        return vals[0] if vals else []

    def _rows(self, sheet):
        vals = self._get(sheet, "2:10000")
        hdr = self._headers(sheet)
        out = []
        for r in vals:
            obj = {hdr[i]: (r[i] if i < len(r) else "") for i in range(len(hdr))}
            out.append(obj)
        return out

    def find_row(self, sheet: str, column: str, value: str):
        """Return ``(index, row)`` for ``sheet`` where ``column`` equals ``value``.

        The index is 1-based including the header row, matching Google Sheets
        API semantics. ``None`` is returned if no match is found.
        """
        rows = self._rows(sheet)
        for idx, row in enumerate(rows, start=2):
            if row.get(column) == value:
                return idx, row
        return None, None

    def update_row(self, sheet: str, index: int, row: dict) -> None:
        """Update ``sheet`` row ``index`` with the values from ``row``."""
        headers = self._headers(sheet)
        values = [[row.get(h, "") for h in headers]]
        body = {"values": values}
        self.ss.values().update(
            spreadsheetId=self.sid,
            range=f"{sheet}!A{index}",
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()

    def list_inspections(self):
        return self._rows("Inspections")

    def list_properties_due(self, iso_date: str):
        props = self._rows("Properties")
        return [p for p in props if p.get("NextDueDate","") == iso_date]

    def list_properties(self):
        return self._rows("Properties")

    def get_property(self, property_id: str):
        for p in self._rows("Properties"):
            if p.get("PropertyID") == property_id:
                return p
        raise KeyError("Property not found: " + property_id)

    def get_client(self, client_id: str):
        for c in self._rows("Clients"):
            if c.get("ClientID") == client_id:
                return c
        raise KeyError("Client not found: " + client_id)

    def append_invoice(self, client_id: str, property_id: str, inv: dict):
        issue = inv.get("created","")
        subtotal = inv.get("subtotal",0)/100
        tax = inv.get("tax",0)/100
        total = inv.get("total",0)/100
        row = [
            inv.get("id",""), client_id, property_id, issue, "", "Sent",
            f"{subtotal:.2f}", f"{tax:.2f}", f"{total:.2f}", inv.get("url",""), "", "", "", ""
        ]
        self._append("Invoices", [row])

    @staticmethod
    def format_address(p: dict) -> str:
        """Return a single-line address from property fields."""
        parts = [
            p.get("AddressLine1", ""),
            p.get("AddressLine2", ""),
            p.get("Suburb", ""),
            p.get("Postcode", ""),
            p.get("State", ""),
        ]
        return ", ".join(x for x in parts if x)
