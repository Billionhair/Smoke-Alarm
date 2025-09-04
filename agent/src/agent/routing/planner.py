from __future__ import annotations

from typing import Iterable, List

from ..router import optimize_route


def plan_route(addresses: Iterable[str]) -> dict:
    """Return an optimized order and Google Maps link for ``addresses``."""
    addresses = list(addresses)
    if len(addresses) < 2:
        return {"order": addresses, "url": ""}
    res = optimize_route(addresses)
    return {"order": res.order, "url": res.url}
