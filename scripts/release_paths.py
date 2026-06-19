"""Resolve release artifact paths (YYYY/MM/DD/<version>/ layout)."""

from __future__ import annotations

import re
from pathlib import Path

_VERSION_RE = re.compile(r"^v?(\d{4})\.(\d{2})\.(\d{2})\.(\d+)$")


def normalize_version(version: str) -> str:
    v = version.strip().lstrip("\ufeff")
    if not v:
        raise ValueError("Release version is empty.")
    if not v.startswith("v"):
        v = f"v{v}"
    if not _VERSION_RE.match(v):
        raise ValueError(f"Invalid release version (expected vYYYY.MM.DD.N): {version}")
    return v


def release_version_dir(repo_root: Path, version: str) -> Path:
    v = normalize_version(version)
    m = _VERSION_RE.match(v)
    assert m is not None
    year, month, day, _ = m.groups()
    return repo_root / "release" / year / month / day / v


def release_notes_path(repo_root: Path, version: str) -> Path:
    return release_version_dir(repo_root, version) / "notes.md"


def release_details_readme_path(repo_root: Path, version: str) -> Path:
    return release_version_dir(repo_root, version) / "readme.md"


def release_prompts_path(repo_root: Path, version: str) -> Path:
    return release_version_dir(repo_root, version) / "prompts.md"


def release_retrospective_path(repo_root: Path, version: str) -> Path:
    return release_version_dir(repo_root, version) / "retrospective.md"


def all_release_version_dirs(repo_root: Path) -> list[Path]:
    release_root = repo_root / "release"
    if not release_root.is_dir():
        return []
    version_re = re.compile(r"^v\d{4}\.\d{2}\.\d{2}\.\d+$")
    dirs = [p for p in release_root.rglob("*") if p.is_dir() and version_re.match(p.name)]
    return sorted(dirs)


_PLACEHOLDER_SCOPE = "Brief description of what is included in this release."
_PLACEHOLDER_COMMIT = "<fill-after-commit>"
_CHANGE_SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")
_SCOPE_RE = re.compile(r"^## Scope\s*\n+(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)


def release_notes_scope_ready(content: str) -> bool:
    match = _SCOPE_RE.search(content)
    if not match:
        return False
    lines = [
        line.strip()
        for line in match.group(1).splitlines()
        if line.strip() and line.strip() != "-"
    ]
    if not lines:
        return False
    return not any(line == _PLACEHOLDER_SCOPE for line in lines)


def release_notes_has_change_bullet(content: str) -> bool:
    changes_match = re.search(r"^## Changes\s*\n+(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
    if changes_match:
        for line in changes_match.group(1).splitlines():
            if re.match(r"^-\s+\S", line.strip()):
                return True

    for section in _CHANGE_SECTIONS:
        pattern = rf"^### {section}\s*\n+(.*?)(?=^### |^## |\Z)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if not match:
            continue
        for line in match.group(1).splitlines():
            if re.match(r"^-\s+\S", line.strip()):
                return True
    return False


def release_notes_ready(notes_path: Path) -> bool:
    if not notes_path.is_file():
        return False
    content = notes_path.read_text(encoding="utf-8-sig")
    if not content.strip():
        return False
    if _PLACEHOLDER_COMMIT in content:
        return False
    if not release_notes_scope_ready(content):
        return False
    return release_notes_has_change_bullet(content)


def release_retrospective_is_scaffold(retrospective_path: Path) -> bool:
    if not retrospective_path.is_file():
        return False
    return "pass / fail / partial" in retrospective_path.read_text(encoding="utf-8-sig")


def release_notes_scaffold(notes_path: Path) -> bool:
    if not notes_path.is_file():
        return True
    content = notes_path.read_text(encoding="utf-8-sig")
    if not content.strip():
        return True
    if not release_notes_scope_ready(content):
        return True
    return not release_notes_has_change_bullet(content)
