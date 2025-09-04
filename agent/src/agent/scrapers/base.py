from __future__ import annotations

import httpx


class BaseScraper:
    """Simple HTTP wrapper with polite defaults."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=10.0)

    def fetch(self, url: str) -> str:
        resp = self.client.get(url)
        resp.raise_for_status()
        return resp.text

    def scrape(self, url: str):
        html = self.fetch(url)
        return self.parse(html)

    # subclasses must implement parse
    def parse(self, html: str):  # pragma: no cover - interface
        raise NotImplementedError
