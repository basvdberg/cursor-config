#!/usr/bin/env python3
"""Load browser-relevant URLs from deploy-basnas service-url-map.yaml (stdlib only)."""

from __future__ import annotations

import re
from pathlib import Path

SERVICE_ID_RE = re.compile(r"^  ([a-z0-9][a-z0-9_-]*):\s*$")
URL_RE = re.compile(r"^    url:\s*(.+?)\s*$")
ACCESS_RE = re.compile(r"^    access_mode:\s*(\S+)\s*$")
STATUS_RE = re.compile(r"^    status:\s*(\S+)\s*$")

BROWSER_ACCESS = frozenset({"https_basnas", "https_office", "raw_lan_port"})

TITLE_OVERRIDES = {
    "admin-qts": "QNAP Admin",
    "kafka-ui": "Kafka UI",
    "airflow-standalone": "Airflow",
    "jobhunter-app": "Jobhunter",
    "immich_server": "Immich",
    "qbittorrent-1": "qBittorrent",
    "radarr-3": "Radarr",
    "nzbget-2": "NZBGet",
    "homebridge-2": "Homebridge",
    "adguard-home": "AdGuard Home",
    "basnas_postgress": "Postgres",
}


def service_title(service_id: str) -> str:
    if service_id in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[service_id]
    parts = service_id.replace("_", "-").split("-")
    return " ".join(p.capitalize() for p in parts if p and not p.isdigit())


def load_browser_urls(path: Path) -> list[tuple[str, str, str]]:
    """Return (service_id, title, url) sorted by title."""
    text = path.read_text(encoding="utf-8")
    entries: list[tuple[str, str, str]] = []
    current_id: str | None = None
    access: str | None = None
    url: str | None = None
    status: str | None = None

    def flush() -> None:
        nonlocal current_id, access, url, status
        if not current_id or not url:
            current_id = access = url = status = None
            return
        if access not in BROWSER_ACCESS:
            current_id = access = url = status = None
            return
        if not url.startswith(("http://", "https://")):
            current_id = access = url = status = None
            return
        title = service_title(current_id)
        if status == "planned":
            title = f"{title} (planned)"
        entries.append((current_id, title, url))
        current_id = access = url = status = None

    for line in text.splitlines():
        if line and not line.startswith(" ") and not line.startswith("#"):
            flush()
            continue
        m = SERVICE_ID_RE.match(line)
        if m:
            flush()
            current_id = m.group(1)
            access = url = status = None
            continue
        if current_id is None:
            continue
        if m := ACCESS_RE.match(line):
            access = m.group(1)
        elif m := URL_RE.match(line):
            url = m.group(1).strip("'\"")
        elif m := STATUS_RE.match(line):
            status = m.group(1)

    flush()
    entries.sort(key=lambda item: item[1].casefold())
    return entries
