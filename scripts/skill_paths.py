"""Discover SKILL.md files under cursor-config/skills (supports nested category folders)."""

from __future__ import annotations

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = CONFIG_ROOT / "skills"

CATEGORY_LABELS: dict[str, str] = {
    "markdown": "markdown & documentation",
    "authoring": "authoring & templates",
    "basnas": "BasNAS & deployment",
    "operations": "operations & release",
    "sync": "bookmarks & sync",
    "coding-standards": "coding standards",
}


def iter_skill_md(skills_root: Path | None = None) -> list[Path]:
    root = skills_root or SKILLS_DIR
    if not root.is_dir():
        return []
    return sorted(root.rglob("SKILL.md"))


def skill_name(skill_md: Path) -> str:
    return skill_md.parent.name


def skill_category(skill_md: Path, skills_root: Path | None = None) -> str | None:
    root = skills_root or SKILLS_DIR
    try:
        rel = skill_md.parent.relative_to(root)
    except ValueError:
        return None
    if len(rel.parts) >= 2:
        return rel.parts[0]
    return None


def skill_group_label(skill_md: Path, skills_root: Path | None = None) -> str:
    category = skill_category(skill_md, skills_root)
    if category:
        return CATEGORY_LABELS.get(category, category.replace("-", " "))
    return "workspace custom"
