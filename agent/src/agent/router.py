from urllib.parse import quote_plus
from dataclasses import dataclass, field
import re
import requests
from geopy.geocoders import Nominatim


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


_coord_re = re.compile(r"^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$")
_geocoder = Nominatim(user_agent="smoke-alarm-router")


def _geocode(addr: str) -> tuple[float, float]:
    """Return latitude/longitude for an address or 'lat,lon' string."""
    if _coord_re.match(addr.strip()):
        lat, lon = map(float, addr.split(","))
        return lat, lon
    loc = _geocoder.geocode(addr)
    if not loc:
        raise ValueError(f"Address not found: {addr}")
    return loc.latitude, loc.longitude


def optimize_route(addresses: list[str]) -> RouteResult:
    """Optimize address order using OSRM's trip solver."""
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
    resp = requests.get(
        f"https://router.project-osrm.org/trip/v1/driving/{coord_str}", params=params
    )
    data = resp.json()
    if data.get("code") != "Ok" or not data.get("trips"):
        raise RuntimeError(f"OSRM error: {data.get('message')}")
    waypoints = data["waypoints"]
    ordered = [None] * len(addresses)
    for idx, wp in enumerate(waypoints):
        ordered[wp["waypoint_index"]] = addresses[idx]
    trip = data["trips"][0]
    dist_km = trip["distance"] / 1000
    dur_min = trip["duration"] / 60
    url = build_route_url(ordered)
    return RouteResult(order=ordered, distance_km=dist_km, duration_min=dur_min, url=url)


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
            daily[day + 1] = RouteResult(order=day_addrs, distance_km=0, duration_min=0, url=url)

    return MultiDayPlan(daily=daily, canceled=cancelled)
