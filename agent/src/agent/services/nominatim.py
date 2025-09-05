"""Nominatim geocoding adapter with rate limiting."""

from __future__ import annotations

import os
import threading
import time
from typing import Tuple

import requests

BASE_URL = os.getenv(
    "NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org"
).rstrip("/")
USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", "smoke-alarm/1.0")
RATE = float(os.getenv("NOMINATIM_RATE_LIMIT", "1"))  # requests per second
_lock = threading.Lock()
_last_call = 0.0


def _throttle() -> None:
    global _last_call
    with _lock:
        wait = 1.0 / RATE - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.time()


def geocode(address: str) -> Tuple[float, float]:
    """Return ``(lat, lon)`` for ``address`` or raise ``ValueError``."""
    _throttle()
    params = {"format": "json", "limit": 1, "q": address}
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(f"{BASE_URL}/search", params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError(f"Address not found: {address}")
    item = data[0]
    return float(item["lat"]), float(item["lon"])
