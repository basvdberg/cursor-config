#!/usr/bin/env python3
"""BasNAS favicon PNGs (32×32) for Chromium Favicons DB and optional HTML import."""

from __future__ import annotations

import base64
import io
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[misc, assignment]

ICON_SIZE = 32

# walkxcode/dashboard-icons (homelab-friendly)
ICON_SLUG: dict[str, str] = {
    "admin-qts": "qnap",
    "airflow-standalone": "apache-airflow",
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


def resize_png(raw: bytes, size: int = ICON_SIZE) -> bytes:
    if Image is None:
        return raw
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


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


def icon_png_bytes(service_id: str, cache_dir: Path, refresh: bool = False) -> bytes | None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{service_id}.png"
    if not refresh and cache_file.is_file():
        return cache_file.read_bytes()
    raw = fetch_icon_png(service_id)
    if not raw:
        return None
    png = resize_png(raw)
    cache_file.write_bytes(png)
    return png


def icon_data_uri(service_id: str, cache_dir: Path, refresh: bool = False) -> str | None:
    png = icon_png_bytes(service_id, cache_dir, refresh=refresh)
    if not png:
        return None
    b64 = base64.standard_b64encode(png).decode("ascii")
    return f"data:image/png;base64,{b64}"
