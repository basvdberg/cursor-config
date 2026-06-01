#!/usr/bin/env python3
"""Merge Chromium Bookmarks JSON (Chrome + Brave) into one Netscape HTML file."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

ROOT_KEYS = ("bookmark_bar", "other", "synced")


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or ""
    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, parsed.fragment))


def merge_url(existing: dict, incoming: dict) -> dict:
    out = dict(existing)
    if len(incoming.get("name", "")) > len(out.get("name", "")):
        out["name"] = incoming["name"]
    if int(incoming.get("date_added", "0")) > int(out.get("date_added", "0")):
        out["date_added"] = incoming["date_added"]
    return out


def merge_children(a: list[dict], b: list[dict]) -> list[dict]:
    folders: dict[str, dict] = {}
    folder_order: list[str] = []
    urls: dict[str, dict] = {}
    url_order: list[str] = []

    def add_folder(node: dict) -> None:
        key = node["name"].casefold()
        if key not in folders:
            folders[key] = dict(node)
            folders[key]["children"] = list(node.get("children", []))
            folder_order.append(key)
        else:
            folders[key]["children"] = merge_children(
                folders[key].get("children", []), node.get("children", [])
            )
            if int(node.get("date_added", "0")) > int(folders[key].get("date_added", "0")):
                folders[key]["date_added"] = node.get("date_added", "0")

    def add_url(node: dict) -> None:
        key = normalize_url(node.get("url", ""))
        if not key:
            return
        if key not in urls:
            urls[key] = dict(node)
            url_order.append(key)
        else:
            urls[key] = merge_url(urls[key], node)

    for source in (a, b):
        for node in source:
            if node.get("type") == "folder":
                add_folder(node)
            elif node.get("type") == "url":
                add_url(node)

    result: list[dict] = []
    for key in folder_order:
        result.append(folders[key])
    for key in url_order:
        result.append(urls[key])
    return result


def chromium_children(bookmarks: dict, root_key: str) -> list[dict]:
    root = bookmarks.get("roots", {}).get(root_key, {})
    return list(root.get("children", []))


def merge_roots(chrome: dict, brave: dict) -> dict[str, list[dict]]:
    merged: dict[str, list[dict]] = {}
    for key in ROOT_KEYS:
        chrome_children = chromium_children(chrome, key)
        brave_children = chromium_children(brave, key)
        if chrome_children or brave_children:
            merged[key] = merge_children(chrome_children, brave_children)
    return merged


def count_nodes(nodes: list[dict]) -> tuple[int, int]:
    folders = urls = 0
    for node in nodes:
        if node.get("type") == "folder":
            folders += 1
            f, u = count_nodes(node.get("children", []))
            folders += f
            urls += u
        elif node.get("type") == "url":
            urls += 1
    return folders, urls


def write_html_node(lines: list[str], node: dict, indent: int) -> None:
    pad = "  " * indent
    if node.get("type") == "folder":
        add = int(node.get("date_added", "0"))
        lines.append(f'{pad}<DT><H3 ADD_DATE="{add}">{html.escape(node.get("name", ""))}</H3>')
        lines.append(f"{pad}<DL><p>")
        for child in node.get("children", []):
            write_html_node(lines, child, indent + 1)
        lines.append(f"{pad}</DL><p>")
    elif node.get("type") == "url":
        add = int(node.get("date_added", "0"))
        name = html.escape(node.get("name", ""))
        url = html.escape(node.get("url", ""), quote=True)
        lines.append(f'{pad}<DT><A HREF="{url}" ADD_DATE="{add}">{name}</A>')


def to_netscape_html(merged_roots: dict[str, list[dict]]) -> str:
    labels = {
        "bookmark_bar": "Bookmarks bar",
        "other": "Other bookmarks",
        "synced": "Mobile bookmarks",
    }
    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
    ]
    for key in ROOT_KEYS:
        if key not in merged_roots:
            continue
        lines.append(
            '  <DT><H3 PERSONAL_TOOLBAR_FOLDER="true">'
            f'{html.escape(labels[key])}</H3>'
        )
        lines.append("  <DL><p>")
        for node in merged_roots[key]:
            write_html_node(lines, node, 2)
        lines.append("  </DL><p>")
    lines.append("</DL><p>")
    return "\n".join(lines) + "\n"


def merge_profiles(chrome_path: Path, brave_path: Path, out_html: Path, out_meta: Path) -> dict:
    chrome = json.loads(chrome_path.read_text(encoding="utf-8"))
    brave = json.loads(brave_path.read_text(encoding="utf-8"))
    merged_roots = merge_roots(chrome, brave)

    total_folders = total_urls = 0
    per_root: dict[str, dict[str, int]] = {}
    for key, children in merged_roots.items():
        f, u = count_nodes(children)
        per_root[key] = {"folders": f, "urls": u}
        total_folders += f
        total_urls += u

    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(to_netscape_html(merged_roots), encoding="utf-8")

    meta = {
        "sources": {"chrome": str(chrome_path), "brave": str(brave_path)},
        "merged": {
            "roots": per_root,
            "total_folders": total_folders,
            "total_urls": total_urls,
        },
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", type=Path, required=True)
    parser.add_argument("--brave", type=Path, required=True)
    parser.add_argument("--out-html", type=Path, required=True)
    parser.add_argument("--out-meta", type=Path, required=True)
    args = parser.parse_args()

    meta = merge_profiles(args.chrome, args.brave, args.out_html, args.out_meta)
    total_urls = meta["merged"]["total_urls"]
    total_folders = meta["merged"]["total_folders"]
    print(f"Wrote {args.out_html} ({total_urls} URLs, {total_folders} folders)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
