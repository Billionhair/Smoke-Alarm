"""Google Sheets helpers using gspread."""

from __future__ import annotations

import csv
from typing import List

import gspread

from ..config import cfg

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def client() -> gspread.Client:
    return gspread.service_account(filename=cfg.sa_path, scopes=SCOPES)


def export_csv(worksheet: str, out_path: str) -> None:
    """Export a worksheet to a CSV file."""
    gc = client()
    ws = gc.open_by_key(cfg.sheet_id).worksheet(worksheet)
    rows: List[List[str]] = ws.get_all_values()
    with open(out_path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
