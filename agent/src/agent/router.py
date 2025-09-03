from urllib.parse import quote_plus

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
