"""
Pre-commit runner for Data Engineering repositories.

Runs Markdown TOC/structure refresh and prompts.md update from cursor-config.
In strict mode, also validates kebab-case naming and required markers.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

RELEASE_METADATA_ONLY = re.compile(
    r"^release/details/[^/]+/(README|prompts)\.md$|^release/details/README\.md$"
)

from cursor_config import (
    KEBAB_CASE_PATTERN,
    config_root,
    folder_name_valid,
    git_repo_root,
    pre_commit_mode,
)

PROJECT_ROOT = git_repo_root()
CURSOR_CONFIG = config_root(PROJECT_ROOT)

EXCLUDED_FILES = {"prompts.md"}
LOCAL_TOC_EXEMPT = {"readme.md"}
EXCLUDED_DIRS = {".git", "scripts", "node_modules", ".cursor", "cursor-config"}

TOC_START = "<!-- markdown-toc:start -->"
TOC_END = "<!-- markdown-toc:end -->"
STRUCT_START = "<!-- markdown-project-structure:start -->"
STRUCT_END = "<!-- markdown-project-structure:end -->"

def get_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in PROJECT_ROOT.rglob("*.md"):
        rel = path.relative_to(PROJECT_ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files)


def get_content_files() -> list[Path]:
    return [f for f in get_markdown_files() if f.name not in EXCLUDED_FILES]


def check_naming_conventions() -> list[str]:
    errors: list[str] = []
    for path in get_markdown_files():
        rel = path.relative_to(PROJECT_ROOT)
        stem = path.stem
        if stem != "readme" and not KEBAB_CASE_PATTERN.match(stem):
            errors.append(f"  File does not follow kebab-case: {rel}")
        for part in rel.parent.parts:
            if not folder_name_valid(part):
                errors.append(f"  Folder does not follow kebab-case: {part} (in {rel})")
    if errors:
        seen: set[str] = set()
        unique: list[str] = []
        for e in errors:
            if e not in seen:
                seen.add(e)
                unique.append(e)
        print("NAMING CONVENTION ERRORS:")
        print("\n".join(unique))
        return unique
    return []


def check_toc_structure() -> list[str]:
    errors: list[str] = []
    for path in get_content_files():
        rel = path.relative_to(PROJECT_ROOT)
        content = path.read_text(encoding="utf-8")
        if TOC_START not in content or TOC_END not in content:
            errors.append(f"  Missing table of contents markers: {rel}")
        if STRUCT_START not in content or STRUCT_END not in content:
            errors.append(f"  Missing project structure markers: {rel}")
        if STRUCT_END in content:
            remaining = content.split(STRUCT_END, maxsplit=1)[-1].strip()
            if remaining:
                errors.append(f"  Project structure is not at end of file: {rel}")
        if TOC_START in content:
            lines = content.split("\n")
            title_found = False
            toc_near_title = False
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    title_found = True
                    for j in range(i + 1, min(i + 20, len(lines))):
                        if TOC_START in lines[j]:
                            toc_near_title = True
                            break
                    break
            if title_found and not toc_near_title:
                errors.append(f"  Table of contents not positioned near title: {rel}")
    if errors:
        print("TOC STRUCTURE ERRORS:")
        print("\n".join(errors))
    return errors


def run_script(name: str, *extra: str) -> None:
    script = CURSOR_CONFIG / "scripts" / name
    cmd = [sys.executable, str(script), "--root", str(PROJECT_ROOT), *extra]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=False)
    if result.returncode != 0:
        print(f"Failed to run {name}.", file=sys.stderr)
        sys.exit(result.returncode)


def get_git_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return (result.stdout or "").strip()


def get_staged_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def should_bump_release() -> bool:
    version_file = PROJECT_ROOT / "release" / "VERSION"
    script = PROJECT_ROOT / "release" / "scripts" / "new-release.ps1"
    if not version_file.is_file() or not script.is_file():
        return False
    if get_git_branch() != "main":
        return False
    staged = get_staged_paths()
    if not staged:
        return False
    if all(RELEASE_METADATA_ONLY.match(path) for path in staged):
        return False
    if os.environ.get("SKIP_RELEASE", "").strip().lower() in {"1", "true", "yes"}:
        return False
    return True


def run_new_release() -> None:
    script = PROJECT_ROOT / "release" / "scripts" / "new-release.ps1"
    if not script.is_file() or sys.platform != "win32":
        return
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )


def run_release_details_sync() -> None:
    version_file = PROJECT_ROOT / "release" / "VERSION"
    script = PROJECT_ROOT / "release" / "scripts" / "update-release-details.ps1"
    if not version_file.is_file() or not script.is_file():
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
            str(script),
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )


def stage_markdown_updates() -> None:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--", "*.md"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    for line in result.stdout.splitlines():
        rel = line.strip()
        if rel:
            os.system(f'git -C "{PROJECT_ROOT}" add "{rel}"')


def main() -> int:
    mode = pre_commit_mode(PROJECT_ROOT)
    errors: list[str] = []

    if should_bump_release():
        run_new_release()

    run_script("update_markdown_docs.py")
    run_script("update_prompts.py")
    run_release_details_sync()

    if mode == "strict":
        errors.extend(check_naming_conventions())
        errors.extend(check_toc_structure())

    stage_markdown_updates()

    if errors:
        print(f"\n{len(errors)} error(s) found. Commit aborted.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
