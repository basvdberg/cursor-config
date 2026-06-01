#!/usr/bin/env python3
"""Inject BasNAS favicons into Chrome/Brave Favicons SQLite (bookmark bar icons)."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from basnas_bookmark_icons import icon_cache_dir, icon_png_bytes  # noqa: E402
from service_url_map import load_browser_urls  # noqa: E402

CONFIG_NAME = "browser-bookmarks-sync.json"
# Windows FILETIME-ish microseconds (Chromium favicon_bitmaps.last_*).
WIN_EPOCH_OFFSET = 11_644_473_600


def config_root() -> Path:
    env = os.environ.get("CURSOR_CONFIG_ROOT")
    if env:
        return Path(env).resolve()
    return SCRIPT_DIR.parent


def expand_path(raw: str, base: Path) -> Path:
    expanded = os.path.expandvars(raw.replace("/", os.sep))
    path = Path(expanded)
    if not path.is_absolute():
        path = (base / path).resolve()
    return path


def load_config() -> dict:
    path = config_root() / CONFIG_NAME
    return json.loads(path.read_text(encoding="utf-8"))


def chrome_timestamp_us() -> int:
    return int((time.time() + WIN_EPOCH_OFFSET) * 1_000_000)


def favicons_db_for_profile(chrome_bookmarks: Path) -> Path:
    # .../User Data/Default/Bookmarks -> .../User Data/Default/Favicons
    return chrome_bookmarks.parent / "Favicons"


def inject_favicon(conn: sqlite3.Connection, page_url: str, png: bytes) -> None:
    width = height = 32
    ts = chrome_timestamp_us()
    cur = conn.cursor()
    cur.execute("DELETE FROM icon_mapping WHERE page_url = ?", (page_url,))
    favicon_url = page_url.rstrip("/") + "/favicon.ico"
    cur.execute("INSERT INTO favicons (url, icon_type) VALUES (?, 1)", (favicon_url,))
    icon_id = cur.lastrowid
    cur.execute(
        """INSERT INTO favicon_bitmaps
           (icon_id, last_updated, image_data, width, height, last_requested)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (icon_id, ts, png, width, height, ts),
    )
    cur.execute(
        "INSERT INTO icon_mapping (page_url, icon_id) VALUES (?, ?)",
        (page_url, icon_id),
    )


def apply_to_db(db_path: Path, entries: list[tuple[str, str, str]], cache_dir: Path) -> tuple[int, int]:
    if not db_path.is_file():
        print(f"skip: no Favicons DB at {db_path}", file=sys.stderr)
        return 0, 0
    ok = fail = 0
    try:
        conn = sqlite3.connect(db_path, timeout=2)
        try:
            for service_id, _title, url in entries:
                png = icon_png_bytes(service_id, cache_dir)
                if not png:
                    fail += 1
                    continue
                inject_favicon(conn, url, png)
                ok += 1
            conn.commit()
        finally:
            conn.close()
    except sqlite3.OperationalError as exc:
        if "locked" in str(exc).lower():
            print(f"error: {db_path.name} is locked — close Chrome/Brave and retry.", file=sys.stderr)
            return 0, len(entries)
        raise
    return ok, fail


def run(*, chrome_only: bool = False, brave_only: bool = False) -> int:
    cfg = load_config()
    root = config_root()
    bookmarks_repo = expand_path(cfg["bookmarksRepo"], root)
    service_map = expand_path(cfg["serviceUrlMap"], root)
    chrome_bm = expand_path(cfg["chromeBookmarks"], root)
    brave_bm = expand_path(cfg["braveBookmarks"], root)
    cache = icon_cache_dir(bookmarks_repo)

    entries = load_browser_urls(service_map)
    if not entries:
        print("No BasNAS URLs in service-url-map.yaml", file=sys.stderr)
        return 1

    targets: list[tuple[str, Path]] = []
    if not brave_only:
        targets.append(("Chrome", favicons_db_for_profile(chrome_bm)))
    if not chrome_only:
        targets.append(("Brave", favicons_db_for_profile(brave_bm)))

    total_ok = total_fail = 0
    for label, db_path in targets:
        ok, fail = apply_to_db(db_path, entries, cache)
        print(f"{label}: {ok} favicon(s) set, {fail} skipped ({db_path})")
        total_ok += ok
        total_fail += fail

    if total_ok == 0 and total_fail > 0:
        return 1
    print("Restart the browser (or reload bookmarks) if icons do not appear immediately.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome-only", action="store_true", help="Only update Chrome")
    parser.add_argument("--brave-only", action="store_true", help="Only update Brave")
    args = parser.parse_args()
    return run(chrome_only=args.chrome_only, brave_only=args.brave_only)


if __name__ == "__main__":
    sys.exit(main())
