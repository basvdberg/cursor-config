#!/usr/bin/env python3
"""Sync Chrome/Brave merge and BasNAS URLs into the browser-bookmarks-sync repo."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from basnas_bookmark_icons import icon_cache_dir, icon_data_uri, icon_png_bytes  # noqa: E402
from merge_chromium_bookmarks import merge_profiles  # noqa: E402
from service_url_map import load_browser_urls  # noqa: E402
BASNAS_MARKERS = ("<!-- cursor-config:basnas:start -->", "<!-- cursor-config:basnas:end -->")
BASNAS_MANAGED_FOLDER_RE = re.compile(
    r"<DT><H3[^>]*>\s*(?:basnas|BasNAS)\s*</H3>\s*<DL><p>(.*?)</DL><p>",
    re.DOTALL | re.IGNORECASE,
)
BASNAS_LINK_RE = re.compile(r'<DT><A HREF="([^"]*)"', re.IGNORECASE)
CONFIG_NAME = "browser-bookmarks-sync.json"


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
    if not path.is_file():
        raise FileNotFoundError(f"Missing config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def basnas_folder_html(entries: list[tuple[str, str, str]]) -> str:
    """Floccus Git sync only keeps title + URL; favicons need apply_chromium_favicons.py."""
    lines = [
        "<!-- cursor-config:basnas:start -->",
        '<DT><H3 ADD_DATE="0">BasNAS</H3>',
        "<DL><p>",
    ]
    for _service_id, title, url in entries:
        safe_url = html.escape(url, quote=True)
        safe_title = html.escape(title)
        lines.append(f'  <DT><A HREF="{safe_url}" ADD_DATE="0">{safe_title}</A>')
    lines.append("</DL><p>")
    lines.append("<!-- cursor-config:basnas:end -->")
    return "\n".join(lines) + "\n"


def basnas_favicon_import_html(
    entries: list[tuple[str, str, str]],
    icons: dict[str, str],
) -> str:
    """Optional Chrome import file (Bookmark Manager → Import). Floccus ignores ICON."""
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>BasNAS favicons</TITLE>",
        "<H1>BasNAS favicons</H1>",
        "<DL><p>",
        '<DT><H3 ADD_DATE="0">BasNAS favicons (import then delete this folder)</H3>',
        "<DL><p>",
    ]
    for service_id, title, url in entries:
        safe_url = html.escape(url, quote=True)
        safe_title = html.escape(title)
        icon = icons.get(service_id)
        if icon:
            safe_icon = html.escape(icon, quote=True)
            lines.append(
                f'<DT><A HREF="{safe_url}" ADD_DATE="0" ICON="{safe_icon}">{safe_title}</A>'
            )
        else:
            lines.append(f'<DT><A HREF="{safe_url}" ADD_DATE="0">{safe_title}</A>')
    lines.extend(["</DL><p>", "</DL><p>"])
    return "\n".join(lines) + "\n"


def _is_managed_basnas_folder(inner: str) -> bool:
    links = BASNAS_LINK_RE.findall(inner)
    if not links:
        return False
    return all(".basnas/" in u.casefold() for u in links)


def inject_basnas_block(html_text: str, block: str) -> str:
    start, end = BASNAS_MARKERS
    if start in html_text and end in html_text:
        pattern = re.compile(
            re.escape(start) + r".*?" + re.escape(end) + r"\n?",
            re.DOTALL,
        )
        return pattern.sub(block, html_text)

    def replace_managed_folder(match: re.Match[str]) -> str:
        inner = match.group(1)
        if _is_managed_basnas_folder(inner):
            return block.rstrip("\n")
        return match.group(0)

    updated, count = BASNAS_MANAGED_FOLDER_RE.subn(replace_managed_folder, html_text, count=1)
    if count:
        return updated

    # Insert before "Other bookmarks" root section when markers are absent.
    anchor = '  <DT><H3 PERSONAL_TOOLBAR_FOLDER="true">Other bookmarks</H3>'
    if anchor in html_text:
        return html_text.replace(anchor, block + anchor, 1)

    # Fallback: append inside bookmarks bar (before its closing DL).
    bar_close = "  </DL><p>\n  <DT><H3 PERSONAL_TOOLBAR_FOLDER"
    if bar_close in html_text:
        return html_text.replace(bar_close, block + bar_close, 1)
    raise ValueError("Could not locate insertion point for BasNAS bookmarks block")


def git_commit_push(repo: Path, message: str, push: bool) -> None:
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, check=True
    )
    if not status.stdout.strip():
        print("No bookmark changes to commit.")
        return
    subprocess.run(["git", "commit", "-m", message], cwd=repo, check=True)
    print(f"Committed in {repo}")
    if push:
        subprocess.run(["git", "push"], cwd=repo, check=True)
        print("Pushed to origin.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge Chrome + Brave into merged-bookmarks.html",
    )
    parser.add_argument(
        "--basnas",
        action="store_true",
        help="Refresh BasNAS folder from service-url-map.yaml",
    )
    parser.add_argument(
        "--apply-favicons",
        action="store_true",
        help="Inject BasNAS icons into Chrome/Brave Favicons DB (close browsers first)",
    )
    parser.add_argument("--commit", action="store_true", help="Git commit in bookmarks repo")
    parser.add_argument("--push", action="store_true", help="Git push after commit")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    args = parser.parse_args()

    if not args.merge and not args.basnas and not args.apply_favicons:
        args.merge = args.basnas = True

    cfg = load_config()
    root = config_root()
    bookmarks_repo = expand_path(cfg["bookmarksRepo"], root)
    merged_html = expand_path(cfg["mergedHtml"], bookmarks_repo)
    merge_meta = expand_path(cfg.get("mergeMeta", "bookmarks/merge-meta.json"), bookmarks_repo)
    service_map = expand_path(cfg["serviceUrlMap"], root)
    chrome = expand_path(cfg["chromeBookmarks"], root)
    brave = expand_path(cfg["braveBookmarks"], root)

    if args.dry_run:
        print(f"config root: {root}")
        print(f"bookmarks repo: {bookmarks_repo}")
        print(f"merged html: {merged_html}")
        print(f"service map: {service_map}")
        return 0

    if not bookmarks_repo.is_dir():
        print(f"error: bookmarks repo not found: {bookmarks_repo}", file=sys.stderr)
        print("Clone https://github.com/basvdberg/browser-bookmarks-sync beside cursor-config.", file=sys.stderr)
        return 1

    changed = False

    if args.merge:
        if not chrome.is_file() or not brave.is_file():
            print(f"error: Chrome or Brave bookmarks missing:\n  {chrome}\n  {brave}", file=sys.stderr)
            return 1
        merge_profiles(chrome, brave, merged_html, merge_meta)
        print(f"Merged Chrome + Brave -> {merged_html}")
        changed = True

    if args.basnas:
        if not merged_html.is_file():
            print(f"error: run --merge first; missing {merged_html}", file=sys.stderr)
            return 1
        if not service_map.is_file():
            print(f"error: missing {service_map}", file=sys.stderr)
            return 1
        entries = load_browser_urls(service_map)
        cache = icon_cache_dir(bookmarks_repo)
        icons: dict[str, str] = {}
        for service_id, _title, _url in entries:
            icon_png_bytes(service_id, cache, refresh=True)
            uri = icon_data_uri(service_id, cache)
            if uri:
                icons[service_id] = uri
        block = basnas_folder_html(entries)
        html_text = merged_html.read_text(encoding="utf-8")
        updated = inject_basnas_block(html_text, block)
        merged_html.write_text(updated, encoding="utf-8")
        import_html = expand_path("bookmarks/basnas-favicon-import.html", bookmarks_repo)
        import_html.write_text(basnas_favicon_import_html(entries, icons), encoding="utf-8")
        print(f"Updated BasNAS folder ({len(entries)} links) in {merged_html}")
        print(f"Wrote favicon import helper: {import_html}")
        print("Floccus does not sync ICON attributes — run with --apply-favicons after closing Chrome/Brave.")
        changed = True

    if args.apply_favicons:
        from apply_chromium_favicons import run as apply_favicons  # noqa: E402

        rc = apply_favicons()
        if rc != 0:
            return rc

    if args.commit and changed:
        msg = "Sync bookmarks"
        if args.merge and args.basnas:
            msg = "Sync merged Chrome/Brave bookmarks and BasNAS service URLs"
        elif args.basnas:
            msg = "Update BasNAS bookmarks from service-url-map.yaml"
        elif args.merge:
            msg = "Merge Chrome and Brave bookmarks"
        git_commit_push(bookmarks_repo, msg, args.push)
    elif args.push:
        print("warning: --push without --commit has no effect", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
