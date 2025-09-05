import re
from dataclasses import dataclass, field

import requests

from .config import cfg
from .router_providers import (
    MapboxProvider,
    OSRMProvider,
    RouteProvider,
    build_route_url,
)
from .services import nominatim


@dataclass
class RouteResult:
    """Result of an optimized route."""

    order: list[str]
    distance_km: float
    duration_min: float
    url: str


@dataclass
class MultiDayPlan:
    """Plan for routes over multiple days."""

    daily: dict[int, RouteResult] = field(default_factory=dict)
    canceled: list[str] = field(default_factory=list)


def _provider() -> RouteProvider:
    if cfg.routing_provider == "mapbox":
        return MapboxProvider()
    return OSRMProvider()


_coord_re = re.compile(r"^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$")


def _geocode(addr: str) -> tuple[float, float]:
    """Return latitude/longitude for an address or 'lat,lon' string."""
    if _coord_re.match(addr.strip()):
        lat, lon = map(float, addr.split(","))
        return lat, lon
    lat, lon = nominatim.geocode(addr)
    return lat, lon


def optimize_route(addresses: list[str]) -> RouteResult:
    """Optimize address order using the configured routing provider."""
    provider = _provider()
    try:
        return provider.optimize(addresses)
    except requests.RequestException as exc:
        raise RuntimeError(f"Route request failed: {exc}") from exc


def plan_multi_day_routes(
    addresses: list[str],
    days: int = 7,
    responses: dict[str, bool] | None = None,
) -> MultiDayPlan:
    """Plan routes over multiple days.

    Addresses with a response of ``False`` or missing are treated as cancelled
    and excluded from the plan. Remaining stops are distributed round-robin
    across the requested number of days and each day's route is optimized
    individually.

    Args:
        addresses: List of address strings.
        days: Number of days to plan ahead.
        responses: Optional mapping of address to confirmation status where
            ``True`` means confirmed and ``False`` means cancelled/no response.

    Returns:
        A :class:`MultiDayPlan` containing optimized routes for each day and a
        list of addresses that were cancelled.
    """

    responses = responses or {}
    confirmed: list[str] = []
    cancelled: list[str] = []
    for addr in addresses:
        if responses.get(addr, False):
            confirmed.append(addr)
        else:
            cancelled.append(addr)

    daily: dict[int, RouteResult] = {}
    if not confirmed:
        return MultiDayPlan(daily=daily, canceled=cancelled)

    for day in range(days):
        day_addrs = confirmed[day::days]
        if not day_addrs:
            continue
        if len(day_addrs) >= 2:
            daily[day + 1] = optimize_route(day_addrs)
        else:
            # Single stop – no routing needed
            url = build_route_url(day_addrs)
            daily[day + 1] = RouteResult(
                order=day_addrs, distance_km=0, duration_min=0, url=url
            )

    return MultiDayPlan(daily=daily, canceled=cancelled)
