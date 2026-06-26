"""Discover skills and rules under cursor-config (supports nested category folders)."""

from __future__ import annotations

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = CONFIG_ROOT / "skills"
RULES_DIR = CONFIG_ROOT / "rules"

CATEGORY_LABELS: dict[str, str] = {
    "markdown": "markdown & documentation",
    "authoring": "authoring & templates",
    "basnas": "BasNAS & deployment",
    "operations": "operations & release",
    "sync": "bookmarks & sync",
    "coding-standards": "coding standards",
    "security": "security & policy",
}

GROUP_ORDER: list[str] = [
    "markdown & documentation",
    "authoring & templates",
    "BasNAS & deployment",
    "operations & release",
    "bookmarks & sync",
    "coding standards",
    "security & policy",
    "workspace custom",
    "authoring & migration (Cursor built-in)",
    "code review (Cursor built-in)",
    "automation & workflow (Cursor built-in)",
    "canvas & SDK (Cursor built-in)",
    "IDE & CLI config (Cursor built-in)",
    "Cursor built-in",
]


def category_group_label(category: str | None) -> str:
    if category:
        return CATEGORY_LABELS.get(category, category.replace("-", " "))
    return "workspace custom"


def iter_skill_md(skills_root: Path | None = None) -> list[Path]:
    root = skills_root or SKILLS_DIR
    if not root.is_dir():
        return []
    return sorted(root.rglob("SKILL.md"))


def iter_rule_mdc(rules_root: Path | None = None) -> list[Path]:
    root = rules_root or RULES_DIR
    if not root.is_dir():
        return []
    return sorted(root.rglob("*.mdc"))


def skill_name(skill_md: Path) -> str:
    return skill_md.parent.name


def rule_name(rule_mdc: Path) -> str:
    return rule_mdc.stem


def _category_from_nested_path(
    item_path: Path, root: Path, *, leaf_is_file: bool
) -> str | None:
    try:
        rel = item_path.parent.relative_to(root) if leaf_is_file else item_path.relative_to(root)
    except ValueError:
        return None
    if len(rel.parts) >= 1 and rel.parts[0] not in {".", ""}:
        return rel.parts[0]
    return None


def skill_category(skill_md: Path, skills_root: Path | None = None) -> str | None:
    root = skills_root or SKILLS_DIR
    try:
        rel = skill_md.parent.relative_to(root)
    except ValueError:
        return None
    if len(rel.parts) >= 2:
        return rel.parts[0]
    return None


def rule_category(rule_mdc: Path, rules_root: Path | None = None) -> str | None:
    return _category_from_nested_path(rule_mdc, rules_root or RULES_DIR, leaf_is_file=True)


def skill_group_label(skill_md: Path, skills_root: Path | None = None) -> str:
    return category_group_label(skill_category(skill_md, skills_root))


def rule_group_label(rule_mdc: Path, rules_root: Path | None = None) -> str:
    return category_group_label(rule_category(rule_mdc, rules_root))


def ordered_groups(groups: set[str] | dict[str, object]) -> list[str]:
    keys = set(groups) if isinstance(groups, dict) else groups
    ordered = [g for g in GROUP_ORDER if g in keys]
    ordered += sorted(g for g in keys if g not in ordered)
    return ordered
