from __future__ import annotations

from typing import List, Dict

from .base import BaseScraper


class MapsScraper(BaseScraper):
    """Stub scraper that expects a JSON response of agencies."""

    def parse(self, text: str) -> List[Dict[str, str]]:
        # The maps API might return JSON; here we parse a minimal subset.
        import json

        data = json.loads(text)
        out: List[Dict[str, str]] = []
        for item in data.get("results", []):
            out.append({"name": item.get("name", ""), "phone": item.get("phone", "")})
        return out
