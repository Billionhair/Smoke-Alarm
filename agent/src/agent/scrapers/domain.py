from __future__ import annotations

import re
from typing import List, Dict

from .base import BaseScraper


class DomainScraper(BaseScraper):
    """Simplistic parser for domain.com.au style output."""

    line_re = re.compile(r"<li class=\"agency\">([^<]+)<span>([^<]+)</span>")

    def parse(self, html: str) -> List[Dict[str, str]]:
        results = []
        for line in html.splitlines():
            m = self.line_re.search(line)
            if m:
                results.append({"name": m.group(1).strip(), "phone": m.group(2).strip()})
        return results
