"""Notification utilities using Apprise."""

from __future__ import annotations

import os

import apprise

from ..config import cfg


def send(message: str, title: str = "Smoke Alarm") -> bool:
    """Send ``message`` via configured Apprise URLs.

    Returns ``True`` if at least one notification was sent.
    """
    urls = cfg.apprise_urls or os.getenv("APPRISE_URLS", "")
    if not urls:
        return False
    apobj = apprise.Apprise()
    for url in urls.split(","):
        apobj.add(url.strip())
    return apobj.notify(body=message, title=title)
