"""
Post-commit runner for Data Engineering repositories with release/VERSION.

Refreshes release/details/<version>/prompts.md and README metadata after each commit.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from cursor_config import config_root, git_repo_root

PROJECT_ROOT = git_repo_root()
CURSOR_CONFIG = config_root(PROJECT_ROOT)


def run_script(name: str, *extra: str) -> None:
    script = CURSOR_CONFIG / "scripts" / name
    cmd = [sys.executable, str(script), "--root", str(PROJECT_ROOT), *extra]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
    if result.returncode != 0:
        print(f"post-commit: failed to run {name}.", file=sys.stderr)
        sys.exit(result.returncode)


def run_release_details_refresh() -> None:
    version_file = PROJECT_ROOT / "release" / "VERSION"
    hook = PROJECT_ROOT / "release" / "scripts" / "post-commit-hook.ps1"
    if not version_file.is_file() or not hook.is_file():
        return
    if sys.platform != "win32":
        return
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(hook),
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )


def stage_release_detail_updates() -> None:
    version_file = PROJECT_ROOT / "release" / "VERSION"
    if not version_file.is_file():
        return
    version = version_file.read_text(encoding="utf-8").strip()
    if not version:
        return
    details_dir = PROJECT_ROOT / "release" / "details" / version
    for name in ("README.md", "prompts.md"):
        path = details_dir / name
        if not path.is_file():
            continue
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        os.system(f'git -C "{PROJECT_ROOT}" add "{rel}"')


def main() -> int:
    version_file = PROJECT_ROOT / "release" / "VERSION"
    if not version_file.is_file():
        return 0

    run_script("update_prompts.py")
    run_release_details_refresh()
    stage_release_detail_updates()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
