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
