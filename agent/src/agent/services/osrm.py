"""Lightweight OSRM client."""

from __future__ import annotations

import os
from typing import List, Tuple

import requests

BASE_URL = os.getenv("OSRM_BASE_URL", "http://localhost:5000").rstrip("/")


def _url(path: str) -> str:
    return f"{BASE_URL}{path}"


def table(coords: List[Tuple[float, float]]) -> List[List[int]]:
    """Return travel time matrix in seconds for ``coords``."""
    coord_str = ";".join(f"{lon},{lat}" for lat, lon in coords)
    resp = requests.get(
        _url(f"/table/v1/driving/{coord_str}"), params={"annotations": "duration"}
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("durations", [])


def route(coords: List[Tuple[float, float]]) -> dict:
    """Return route polyline and durations for ``coords``."""
    coord_str = ";".join(f"{lon},{lat}" for lat, lon in coords)
    params = {"overview": "full", "geometries": "polyline"}
    resp = requests.get(_url(f"/route/v1/driving/{coord_str}"), params=params)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "Ok" or not data.get("routes"):
        raise RuntimeError(f"OSRM error: {data.get('message')}")
    route = data["routes"][0]
    return {
        "polyline": route["geometry"],
        "duration": route["duration"],
        "distance": route["distance"],
    }
