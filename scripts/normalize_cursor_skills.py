#!/usr/bin/env python3
"""Normalize SKILL.md to Cursor convention: YAML frontmatter first, no TOC/structure blocks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_paths import iter_skill_md  # noqa: E402

STRUCT_SECTION_RE = re.compile(
    r"\n## Project structure\s*\n[\s\S]*?<!-- markdown-project-structure:end -->\s*",
    re.IGNORECASE,
)
FRONTMATTER_RE = re.compile(r"^(---\s*\n(?:.*\n)*?---\s*\n)", re.MULTILINE)


def extract_skill_frontmatter(content: str) -> tuple[str, str] | None:
    for match in FRONTMATTER_RE.finditer(content):
        block = match.group(1)
        if "name:" not in block:
            continue
        return block, content[match.end() :]
    return None


def strip_project_structure(content: str) -> str:
    return STRUCT_SECTION_RE.sub("\n", content)


def normalize_skill_md(content: str) -> str | None:
    parsed = extract_skill_frontmatter(content)
    if parsed is None:
        return None
    frontmatter, body = parsed
    body = strip_project_structure(body)
    body = re.sub(
        r"^## Table of contents\s*\n+(?=<!-- markdown-toc:start -->)",
        "",
        body,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    body = re.sub(
        r"<!-- markdown-toc:start -->[\s\S]*?<!-- markdown-toc:end -->\s*",
        "",
        body,
        flags=re.MULTILINE,
    )
    body = body.strip()
    if body and not body.endswith("\n"):
        body += "\n"
    return frontmatter + body


def normalize_skill_support_md(content: str) -> str:
    """Supporting skill markdown: drop project-structure block only."""
    updated = strip_project_structure(content)
    if updated == content:
        return content
    return updated.rstrip() + "\n"


def main() -> int:
    changed = 0
    for skill_md in iter_skill_md():
        original = skill_md.read_text(encoding="utf-8")
        normalized = normalize_skill_md(original)
        if normalized is None:
            print(f"skip (no frontmatter): {skill_md}", file=sys.stderr)
            continue
        if normalized != original:
            skill_md.write_text(normalized, encoding="utf-8", newline="\n")
            print(f"normalized: {skill_md}")
            changed += 1

    skills_root = SCRIPT_DIR.parent / "skills"
    for path in sorted(skills_root.rglob("*.md")):
        if path.name == "SKILL.md":
            continue
        original = path.read_text(encoding="utf-8")
        updated = normalize_skill_support_md(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"stripped structure: {path}")
            changed += 1

    print(f"Done ({changed} file(s) updated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
