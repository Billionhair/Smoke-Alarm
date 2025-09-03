from __future__ import annotations
from typing import Protocol, List
from .sheets import SheetDB
from .config import cfg

try:
    import psycopg2
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None

class Repository(Protocol):
    def list_inspections(self) -> List[dict]: ...
    def list_properties_due(self, iso_date: str) -> List[dict]: ...
    def list_properties(self) -> List[dict]: ...
    def get_property(self, property_id: str) -> dict: ...
    def get_client(self, client_id: str) -> dict: ...
    def append_invoice(self, client_id: str, property_id: str, inv: dict) -> None: ...

class SheetRepository:
    def __init__(self) -> None:
        self.db = SheetDB()

    def list_inspections(self) -> List[dict]:
        return self.db.list_inspections()

    def list_properties_due(self, iso_date: str) -> List[dict]:
        return self.db.list_properties_due(iso_date)

    def list_properties(self) -> List[dict]:
        return self.db.list_properties()

    def get_property(self, property_id: str) -> dict:
        return self.db.get_property(property_id)

    def get_client(self, client_id: str) -> dict:
        return self.db.get_client(client_id)

    def append_invoice(self, client_id: str, property_id: str, inv: dict) -> None:
        self.db.append_invoice(client_id, property_id, inv)

class PostgresRepository:
    def __init__(self, dsn: str | None = None) -> None:
        if psycopg2 is None:
            raise RuntimeError("psycopg2 not installed")
        self.conn = psycopg2.connect(dsn or cfg.pg_dsn)

    def list_inspections(self) -> List[dict]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM inspections")
            cols = [c.name for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    # Additional methods would mirror SheetRepository using SQL queries
