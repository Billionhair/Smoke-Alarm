from __future__ import annotations

from datetime import datetime
import itertools

_counter = itertools.count(1)


def new_id(prefix: str) -> str:
    """Return a unique ID using ``prefix`` and the current date."""
    date = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{date}-{next(_counter):03d}"
