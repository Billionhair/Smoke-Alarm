from __future__ import annotations

from abc import ABC, abstractmethod
from urllib.parse import quote_plus

import requests

from .config import cfg


class RouteProvider(ABC):
    @abstractmethod
    def optimize(self, addresses: list[str]):
        """Return RouteResult for addresses."""


class OSRMProvider(RouteProvider):
    def optimize(self, addresses: list[str]):
        from .router import RouteResult, _geocode

        if len(addresses) < 2:
            raise ValueError("At least two addresses are required")
        coords = [_geocode(a) for a in addresses]
        coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
        params = {
            "source": "first",
            "destination": "last",
            "roundtrip": "false",
            "overview": "false",
        }
        base = cfg.osrm_base_url.rstrip("/")
        resp = requests.get(f"{base}/trip/v1/driving/{coord_str}", params=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "Ok" or not data.get("trips"):
            raise RuntimeError(f"OSRM error: {data.get('message')}")
        waypoints = data["waypoints"]
        ordered: list[str] = [""] * len(addresses)
        for idx, wp in enumerate(waypoints):
            ordered[wp["waypoint_index"]] = addresses[idx]
        trip = data["trips"][0]
        dist_km = trip["distance"] / 1000
        dur_min = trip["duration"] / 60
        url = build_route_url(ordered)
        return RouteResult(
            order=ordered, distance_km=dist_km, duration_min=dur_min, url=url
        )


class MapboxProvider(RouteProvider):
    def __init__(self, token: str | None = None) -> None:
        self.token = token or cfg.mapbox_token
        if not self.token:
            raise RuntimeError("Missing MAPBOX_TOKEN")

    def optimize(self, addresses: list[str]):
        from .router import RouteResult, _geocode

        coords = [_geocode(a) for a in addresses]
        coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
        url = f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coord_str}"
        params = {
            "source": "first",
            "destination": "last",
            "roundtrip": "false",
            "access_token": self.token,
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "Ok" or not data.get("trips"):
            raise RuntimeError(f"Mapbox error: {data.get('message')}")
        waypoints = data["waypoints"]
        ordered: list[str] = [""] * len(addresses)
        for idx, wp in enumerate(waypoints):
            ordered[wp.get("waypoint_index", idx)] = addresses[idx]
        trip = data["trips"][0]
        dist_km = trip["distance"] / 1000
        dur_min = trip["duration"] / 60
        url = build_route_url(ordered)
        return RouteResult(
            order=ordered, distance_km=dist_km, duration_min=dur_min, url=url
        )


# simple build_route_url reuse


def build_route_url(addresses):
    if not addresses:
        return ""
    enc = [quote_plus(a) for a in addresses]
    waypoints = "%7C".join(enc[:-1]) if len(enc) > 1 else ""
    dest = enc[-1]
    url = f"https://www.google.com/maps/dir/?api=1&destination={dest}"
    if waypoints:
        url += f"&waypoints={waypoints}"
    return url
