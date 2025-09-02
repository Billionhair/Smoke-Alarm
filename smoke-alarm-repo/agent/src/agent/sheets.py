from __future__ import annotations
import json
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .config import cfg

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

def _creds():
    with open(cfg.sa_path,"r") as f:
        info = json.load(f)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    if cfg.subject_email:
        creds = creds.with_subject(cfg.subject_email)
    return creds

def _sheets():
    return build("sheets","v4", credentials=_creds()).spreadsheets()

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

    def format_address(self, p: dict):
        parts = [p.get("AddressLine1",""), p.get("AddressLine2",""), p.get("Suburb",""), p.get("Postcode",""), p.get("State","")]
        return ", ".join([x for x in parts if x])
