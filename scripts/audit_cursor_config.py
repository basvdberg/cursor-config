#!/usr/bin/env python3
"""Audit cursor-config rules and skills for consistency and policy compliance."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_paths import iter_rule_mdc, iter_skill_md  # noqa: E402

CONFIG_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = CONFIG_ROOT / "skills"
RULES_DIR = CONFIG_ROOT / "rules"
PRIVATE_REPOS_FILE = CONFIG_ROOT / "project-structure-external.json"
MAX_SKILL_LINES = 500

NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
REL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PRIVATE_GITHUB_RE = re.compile(
    r"https?://(?:www\.)?github\.com/[^/\s)]+/([^/\s)]+)"
)
CONTENT_MARKDOWN_MARKERS = (
    "<!-- markdown-toc:start -->",
    "<!-- markdown-project-structure:start -->",
)
SKIP_LINK_TARGETS = frozenset(
    {
        "chat-uuid",
        "readme.md",
        "relative/path.md",
        "relative/path/to/readme.md",
        "docs/markdown-automation.md",
    }
)


class Issue:
    def __init__(self, level: str, path: Path, message: str) -> None:
        self.level = level
        self.path = path
        self.message = message

    def __str__(self) -> str:
        rel = self.path.relative_to(CONFIG_ROOT)
        return f"{self.level} {rel}: {self.message}"


def load_private_repo_slugs() -> set[str]:
    if not PRIVATE_REPOS_FILE.is_file():
        return set()
    data = json.loads(PRIVATE_REPOS_FILE.read_text(encoding="utf-8"))
    return set(data.get("private", []))


def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks so examples do not fail policy checks."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def parse_skill_frontmatter(text: str) -> dict[str, str]:
    for match in re.finditer(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL | re.MULTILINE):
        block = match.group(1)
        if "name:" not in block:
            continue
        result: dict[str, str] = {}
        for line in block.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result
    return {}


def resolve_link(source: Path, target: str) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    file_part = target.split("#", 1)[0]
    if not file_part or file_part in SKIP_LINK_TARGETS:
        return None
    if file_part.startswith("/"):
        return Path(file_part)
    return (source.parent / file_part).resolve()


def audit_skill(skill_md: Path, issues: list[Issue], names: dict[str, Path]) -> None:
    text = skill_md.read_text(encoding="utf-8")

    if not text.startswith("---"):
        issues.append(
            Issue("ERROR", skill_md, "SKILL.md must start with YAML frontmatter (---)")
        )

    for marker in CONTENT_MARKDOWN_MARKERS:
        if marker in text:
            issues.append(
                Issue(
                    "ERROR",
                    skill_md,
                    f"SKILL.md must not contain content-doc marker {marker!r} "
                    "(Cursor skill convention: frontmatter + body only)",
                )
            )

    if len(text.splitlines()) > MAX_SKILL_LINES:
        issues.append(
            Issue(
                "WARN",
                skill_md,
                f"SKILL.md has {len(text.splitlines())} lines (>{MAX_SKILL_LINES})",
            )
        )

    fm = parse_skill_frontmatter(text)
    if not fm.get("name"):
        issues.append(Issue("ERROR", skill_md, "Missing frontmatter 'name'"))
    if not fm.get("description"):
        issues.append(Issue("ERROR", skill_md, "Missing frontmatter 'description'"))

    name_match = NAME_RE.search(text)
    if name_match:
        name = name_match.group(1).strip()
        if name in names:
            issues.append(
                Issue(
                    "ERROR",
                    skill_md,
                    f"Duplicate skill name '{name}' (also in {names[name].relative_to(CONFIG_ROOT)})",
                )
            )
        else:
            names[name] = skill_md

    for match in REL_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("#") or "relative/path" in target:
            continue
        resolved = resolve_link(skill_md, target)
        if resolved is not None and not resolved.is_file():
            issues.append(Issue("ERROR", skill_md, f"Broken link: {target}"))


def audit_private_links(path: Path, private_slugs: set[str], issues: list[Issue]) -> None:
    if path.suffix not in {".md", ".mdc"}:
        return
    text = strip_fenced_code(path.read_text(encoding="utf-8"))
    for match in PRIVATE_GITHUB_RE.finditer(text):
        slug = match.group(1).rstrip(")")
        if slug in private_slugs:
            issues.append(
                Issue(
                    "ERROR",
                    path,
                    f"Private repo link to github.com/.../{slug} (use name only per no-private-git-repo-links)",
                )
            )


def audit_rules(issues: list[Issue]) -> None:
    for rule in iter_rule_mdc():
        text = rule.read_text(encoding="utf-8")
        if not text.startswith("---"):
            issues.append(Issue("ERROR", rule, "Missing YAML frontmatter"))
        for match in REL_LINK_RE.finditer(text):
            target = match.group(1).strip()
            resolved = resolve_link(rule, target)
            if resolved is not None and not resolved.is_file():
                issues.append(Issue("ERROR", rule, f"Broken link: {target}"))


def audit_deploy_skill_exists(issues: list[Issue]) -> None:
    deploy = SKILLS_DIR / "basnas" / "deploy-data-solution-basnas" / "SKILL.md"
    if not deploy.is_file():
        issues.append(
            Issue(
                "ERROR",
                CONFIG_ROOT,
                "Missing skills/basnas/deploy-data-solution-basnas/SKILL.md",
            )
        )


def collect_audit_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ("**/*.md", "**/*.mdc"):
        files.extend(CONFIG_ROOT.glob(pattern))
    excluded = {".git", "node_modules"}
    return sorted(p for p in files if not any(part in excluded for part in p.parts))


def main() -> int:
    issues: list[Issue] = []
    private_slugs = load_private_repo_slugs()
    names: dict[str, Path] = {}

    audit_deploy_skill_exists(issues)
    audit_rules(issues)

    for skill_md in iter_skill_md():
        audit_skill(skill_md, issues, names)

    for path in collect_audit_files():
        audit_private_links(path, private_slugs, issues)

    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARN"]

    for issue in issues:
        print(issue)

    if warnings:
        print(f"\n{len(warnings)} warning(s)")
    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print("\nAudit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
