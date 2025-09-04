from __future__ import annotations

import re
from typing import List, Dict

from .base import BaseScraper


class RealEstateAIScraper(BaseScraper):
    """Minimal scraper for realestate.com.au style pages."""

    line_re = re.compile(r"data-name=\"([^\"]+)\".*data-phone=\"([^\"]+)\"")

    def parse(self, html: str) -> List[Dict[str, str]]:
        results = []
        for line in html.splitlines():
            m = self.line_re.search(line)
            if m:
                results.append({"name": m.group(1), "phone": m.group(2)})
        return results
