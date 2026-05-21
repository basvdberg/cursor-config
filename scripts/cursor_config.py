"""Resolve the cursor-config installation and consumer Git repository roots."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

CONFIG_DIR_NAME = "cursor-config"
GIT_CONFIG_KEY = "cursor.configPath"
REPO_CONFIG_FILE = ".cursor-config.json"


def git_repo_root(start: Path | None = None) -> Path:
    start = (start or Path.cwd()).resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip()).resolve()
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
    return start


def _read_repo_config(repo_root: Path) -> dict:
    path = repo_root / REPO_CONFIG_FILE
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _resolve_path(candidate: Path, repo_root: Path) -> Path | None:
    candidate = candidate.expanduser()
    if not candidate.is_absolute():
        candidate = (repo_root / candidate).resolve()
    if candidate.is_dir() and (candidate / "scripts" / "update_markdown_docs.py").is_file():
        return candidate
    return None


def config_root(repo_root: Path | None = None) -> Path:
    """
    Locate the cursor-config repository.

    Order: CURSOR_CONFIG_ROOT env, git cursor.configPath, .cursor-config.json,
    sibling ../cursor-config, ~/.cursor/cursor-config.
    """
    repo_root = (repo_root or git_repo_root()).resolve()

    env = os.environ.get("CURSOR_CONFIG_ROOT", "").strip()
    if env:
        found = _resolve_path(Path(env), repo_root)
        if found:
            return found

    git_cfg = subprocess.run(
        ["git", "config", "--get", GIT_CONFIG_KEY],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if git_cfg.returncode == 0 and git_cfg.stdout.strip():
        found = _resolve_path(Path(git_cfg.stdout.strip()), repo_root)
        if found:
            return found

    repo_cfg = _read_repo_config(repo_root)
    for key in ("cursorConfig", "cursor_config", "configPath"):
        raw = repo_cfg.get(key)
        if isinstance(raw, str) and raw.strip():
            found = _resolve_path(Path(raw.strip()), repo_root)
            if found:
                return found

    sibling = _resolve_path(repo_root.parent / CONFIG_DIR_NAME, repo_root)
    if sibling:
        return sibling

    home = _resolve_path(Path.home() / ".cursor" / CONFIG_DIR_NAME, repo_root)
    if home:
        return home

    raise FileNotFoundError(
        "cursor-config not found. Clone cursor-config, set CURSOR_CONFIG_ROOT, "
        f"or add {REPO_CONFIG_FILE} with \"cursorConfig\": \"../cursor-config\"."
    )


def pre_commit_mode(repo_root: Path | None = None) -> str:
    """Return pre-commit mode: 'strict' (naming + marker checks) or 'standard'."""
    repo_root = (repo_root or git_repo_root()).resolve()
    cfg = _read_repo_config(repo_root)
    mode = cfg.get("preCommit") or cfg.get("pre_commit")
    if isinstance(mode, str) and mode.strip():
        return mode.strip().lower()
    if repo_root.name == "data-engineering-design-patterns":
        return "strict"
    return "standard"
