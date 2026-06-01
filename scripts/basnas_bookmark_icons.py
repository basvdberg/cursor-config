#!/usr/bin/env python3
"""Favicon data URIs for BasNAS service bookmarks (cached PNG files)."""

from __future__ import annotations

import base64
import urllib.error
import urllib.request
from pathlib import Path

# walkxcode/dashboard-icons (homelab-friendly)
ICON_SLUG: dict[str, str] = {
    "admin-qts": "qnap",
    "kafka-ui": "kafka",
    "airflow-standalone": "apache-airflow",
    "jobhunter-app": "homepage",
    "immich_server": "immich",
    "plex": "plex",
    "qbittorrent-1": "qbittorrent",
    "radarr-3": "radarr",
    "nzbget-2": "nzbget",
    "homebridge-2": "homebridge",
    "adguard-home": "adguard-home",
}

CDN = "https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/{slug}.png"


def icon_cache_dir(bookmarks_repo: Path) -> Path:
    return bookmarks_repo / "bookmarks" / "basnas-icons"


def fetch_icon_png(service_id: str) -> bytes | None:
    slug = ICON_SLUG.get(service_id)
    if not slug:
        return None
    url = CDN.format(slug=slug)
    req = urllib.request.Request(url, headers={"User-Agent": "cursor-config/sync_browser_bookmarks"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return None
            data = resp.read()
            return data if data else None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def icon_data_uri(service_id: str, cache_dir: Path, refresh: bool = False) -> str | None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{service_id}.png"
    if not refresh and cache_file.is_file():
        raw = cache_file.read_bytes()
    else:
        raw = fetch_icon_png(service_id)
        if not raw:
            return None
        cache_file.write_bytes(raw)
    b64 = base64.standard_b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"
