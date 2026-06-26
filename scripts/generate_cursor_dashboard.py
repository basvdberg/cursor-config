#!/usr/bin/env python3
"""Generate doc/cursor-dashboard.md — rules/skills inventory matrix and quality scores."""

from __future__ import annotations

import os
import re
import stat
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
import sys

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_paths import (  # noqa: E402
    iter_rule_mdc,
    iter_skill_md,
    ordered_groups,
    rule_group_label,
    skill_group_label,
)

CONFIG_ROOT = SCRIPT_DIR.parent
OUTPUT = CONFIG_ROOT / "doc" / "cursor-dashboard.md"
USER_CURSOR = Path(os.environ.get("USERPROFILE", "")) / ".cursor"
WORKSPACE = CONFIG_ROOT.parent

WORKSPACE_PROJECTS = [
    "cursor-config",
    "browser-bookmarks-sync",
    "data-solution-2026",
    "data-engineering-2026",
    "data-engineering-design-patterns",
    "adl-feedback",
]

SKIP_LINK = frozenset({"readme.md", "relative/path.md", "chat-uuid"})


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL | re.MULTILINE)
    if not match:
        return {}
    result: dict[str, str] = {}
    key: str | None = None
    val_lines: list[str] = []
    for line in match.group(1).splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:\s*", line) and not line.startswith((" ", "\t")):
            if key:
                result[key] = " ".join(val_lines).strip()
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            val_lines = [] if rest in (">-", "|", "") else [rest]
        elif key:
            val_lines.append(line.strip())
    if key:
        result[key] = " ".join(val_lines).strip()
    return result


def is_junction(path: Path) -> bool:
    """Windows directory junction (reparse point), not a plain folder."""
    try:
        return path.is_junction()  # type: ignore[attr-defined]
    except AttributeError:
        pass
    st = path.lstat()
    reparse = getattr(st, "st_file_attributes", 0) & 0x400
    return bool(reparse or (st.st_mode & stat.S_IFLNK))


def count_project_rules_skills(project: Path) -> tuple[int, int, list[str]]:
    notes: list[str] = []
    if project.name == "cursor-config":
        rules = len(list((project / "rules").rglob("*.mdc")))
        skills = len(iter_skill_md(project / "skills"))
        return rules, skills, notes

    rules = 0
    skills = 0
    cursor_dir = project / ".cursor"
    if (cursor_dir / "rules").is_dir():
        rules = len(list((cursor_dir / "rules").glob("*.mdc")))
    if (cursor_dir / "skills").is_dir():
        skills = len(list((cursor_dir / "skills").glob("*/SKILL.md")))
    if cursor_dir.is_dir():
        for f in cursor_dir.rglob("*"):
            if f.is_file() and f.suffix in {".mdc"}:
                continue
            if f.is_file() and f.name not in {"troubleshooting-errors.md"}:
                rel = str(f.relative_to(project))
                if ".cursor" in rel and not rel.endswith("troubleshooting-errors.md"):
                    notes.append(rel)
    if (cursor_dir / "troubleshooting-errors.md").is_file():
        notes.append(".cursor/troubleshooting-errors.md (ERR log artifact, not a rule)")
    return rules, skills, notes


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def audit_links(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", strip_fenced_code(text)):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part or file_part in SKIP_LINK or "relative/path" in file_part:
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.is_file():
            issues.append(f"broken link: `{target}`")
    return issues


def score_item(
    kind: str,
    lines: int,
    desc: str,
    issues: list[str],
    *,
    has_fm: bool,
    toc_before_fm: bool,
    disable_invoke: str | None,
) -> tuple[float, list[str]]:
    score = 10.0
    notes: list[str] = []

    if not has_fm:
        score -= 3
        notes.append("missing YAML frontmatter")
    if not desc or desc in {">-", ">"}:
        score -= 2
        notes.append("description empty or not parsed")
    elif len(desc) < 50:
        score -= 1
        notes.append("short description; weak WHEN triggers")
    if kind == "skill":
        if lines > 500:
            score -= 3
            notes.append(f"{lines} lines (>500 guideline)")
        elif lines > 250:
            score -= 1.5
            notes.append(f"{lines} lines (verbose)")
        elif lines > 200:
            score -= 0.5
        if toc_before_fm:
            score -= 1
        if kind == "skill" and disable_invoke is None and "cursor-config" in str(CONFIG_ROOT):
            pass  # optional field
    else:
        if lines > 50:
            score -= 1
            notes.append("rule >50 lines; consider a skill")

    for issue in issues:
        low = issue.lower()
        if "broken link" in low:
            score -= 2
        elif "duplicate" in low:
            score -= 1
        elif ">500" in low:
            score -= 1

    return max(1.0, min(10.0, round(score, 1))), notes


def load_skill(path: Path, source: str, group: str) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    lines = len(text.splitlines())
    desc = fm.get("description", "")
    toc_before = bool(
        re.search(r"## Table of contents[\s\S]*?---\s*\nname:", text, re.MULTILINE)
    )
    issues = audit_links(path, text)
    if lines > 500:
        issues.append(f"WARN: {lines} lines (>500)")
    if toc_before:
        issues.append("TOC before frontmatter (move YAML to line 1)")
    if not fm.get("name"):
        issues.append("missing `name` in frontmatter")
    if not fm.get("description"):
        issues.append("missing `description` in frontmatter")
    score, score_notes = score_item(
        "skill",
        lines,
        desc,
        issues,
        has_fm=bool(fm),
        toc_before_fm=toc_before,
        disable_invoke=fm.get("disable-model-invocation"),
    )
    return {
        "id": fm.get("name", path.parent.name),
        "path": path,
        "source": source,
        "group": group,
        "summary": desc or "(no description)",
        "lines": lines,
        "score": score,
        "issues": issues,
        "score_notes": score_notes,
    }


def load_rule(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    lines = len(text.splitlines())
    desc = fm.get("description", "")
    issues = audit_links(path, text)
    if not text.startswith("---"):
        issues.append("missing YAML frontmatter")
    if not desc:
        issues.append("missing `description` in frontmatter")
    group = rule_group_label(path)
    score, score_notes = score_item(
        "rule",
        lines,
        desc,
        issues,
        has_fm=bool(fm),
        toc_before_fm=False,
        disable_invoke=None,
    )
    return {
        "id": path.stem,
        "path": path,
        "source": "cursor-config",
        "group": group,
        "summary": desc,
        "lines": lines,
        "score": score,
        "issues": issues,
        "score_notes": score_notes,
        "always_apply": fm.get("alwaysApply", ""),
        "globs": fm.get("globs", ""),
    }


def user_home_counts() -> dict:
    skills_dir = USER_CURSOR / "skills"
    entries = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.is_dir() else []
    junctions = sum(1 for d in entries if is_junction(d))
    real = sum(1 for d in entries if not is_junction(d))
    rules_dir = USER_CURSOR / "rules"
    rules = len(list(rules_dir.glob("*.mdc"))) if rules_dir.is_dir() else 0
    skills_cursor = (
        len(list((USER_CURSOR / "skills-cursor").glob("*/SKILL.md")))
        if (USER_CURSOR / "skills-cursor").is_dir()
        else 0
    )
    return {
        "skills_junctions": junctions,
        "skills_real": real,
        "rules": rules,
        "skills_cursor": skills_cursor,
    }


def rel_link(path: Path) -> str:
    try:
        return str(path.relative_to(CONFIG_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def skill_group(name: str, source: str) -> str:
    if source == "skills-cursor":
        if name in {"review", "review-bugbot", "review-security"}:
            return "code review (Cursor built-in)"
        if name in {"create-skill", "create-rule", "create-hook", "create-subagent", "migrate-to-skills"}:
            return "authoring & migration (Cursor built-in)"
        if name in {"automate", "loop", "babysit", "split-to-prs", "shell"}:
            return "automation & workflow (Cursor built-in)"
        if name in {"canvas", "sdk"}:
            return "canvas & SDK (Cursor built-in)"
        if name in {"statusline", "update-cursor-settings", "update-cli-config"}:
            return "IDE & CLI config (Cursor built-in)"
        return "Cursor built-in"
    return "workspace custom"


def build() -> str:
    today = date.today().isoformat()
    uh = user_home_counts()
    cc_rules = len(iter_rule_mdc())
    cc_skills = len(iter_skill_md())
    merged_rules = cc_rules + uh["rules"]
    merged_skills = cc_skills + uh["skills_real"]

    lines: list[str] = [
        "# Cursor rules & skills dashboard",
        "",
        f"Generated: {today}. Re-run: `python scripts/generate_cursor_dashboard.py` from cursor-config.",
        "",
        "## Inventory matrix",
        "",
        "Counts of `.mdc` rules and `SKILL.md` skills. **Merged (effective custom)** = cursor-config plus non-junction entries under `%USERPROFILE%\\.cursor\\skills` and `rules` (if any).",
        "",
        "| Location | Rules | Skills | Notes |",
        "|----------|------:|-------:|-------|",
    ]

    project_rows: list[tuple[str, int, int, str]] = []
    for name in WORKSPACE_PROJECTS:
        proj = WORKSPACE / name
        if not proj.is_dir():
            continue
        r, s, notes = count_project_rules_skills(proj)
        note = "; ".join(notes) if notes else "—"
        project_rows.append((name, r, s, note))
        lines.append(f"| workspace / {name} | {r} | {s} | {note} |")

    lines.extend(
        [
            f"| **cursor-config** (canonical) | **{cc_rules}** | **{cc_skills}** | Shared rules + skills source of truth |",
            f"| user home `~/.cursor/skills` | — | {uh['skills_junctions']} junctions + {uh['skills_real']} real | "
            f"All {uh['skills_junctions']} installed skills are junctions → cursor-config |",
            f"| user home `~/.cursor/skills-cursor` | — | {uh['skills_cursor']} | Cursor-managed built-ins (not merged) |",
            f"| user home `~/.cursor/rules` | {uh['rules']} | — | "
            + (
                "directory absent"
                if uh["rules"] == 0 and not (USER_CURSOR / "rules").is_dir()
                else "local rules"
            )
            + " |",
            f"| **Merged effective custom** | **{merged_rules}** | **{merged_skills}** | cursor-config + non-symlink user-home skills/rules |",
            f"| **Total available to agent** | **{merged_rules}** | **{merged_skills + uh['skills_cursor']}** | custom + Cursor built-in skills |",
            "",
            "### Symlink policy",
            "",
            "- `install-cursor.ps1` junctions `~/.cursor/skills/<name>` → `cursor-config/skills/<group>/<name>/` (flat by skill name).",
            "- Rules are **not** junctioned; they load when `cursor-config` is in the workspace.",
            f"- Non-junction user-home skills: **{uh['skills_real']}** (should be migrated into cursor-config per `create-skill`).",
            "",
            "## Scoring legend",
            "",
            "Score 1–10 for **compactness + effectiveness** (higher is better).",
            "",
            "| Factor | Effect |",
            "|--------|--------|",
            "| Missing frontmatter or description | −2 to −3 |",
            "| Ambiguous or short description (weak WHEN triggers) | −1 |",
            "| Skill >250 lines (verbose) or >500 lines | −0.5 to −3 |",
            "| Rule >50 lines | −1 (prefer skill) |",
            "| TOC before YAML frontmatter | −1 |",
            "| Broken relative links | −2 |",
            "",
            "Audit: `python scripts/audit_cursor_config.py` (cursor-config skills/rules).",
            "",
        ]
    )

    rules = [load_rule(p) for p in iter_rule_mdc()]
    skills: list[dict] = []
    for skill_md in iter_skill_md():
        skills.append(
            load_skill(skill_md, "cursor-config", skill_group_label(skill_md))
        )
    if (USER_CURSOR / "skills-cursor").is_dir():
        for skill_md in sorted((USER_CURSOR / "skills-cursor").glob("*/SKILL.md")):
            name = skill_md.parent.name
            skills.append(
                load_skill(
                    skill_md,
                    "skills-cursor",
                    skill_group(name, "skills-cursor"),
                )
            )

    # Rules section
    lines.append("## Rules (cursor-config)")
    lines.append("")
    by_group: dict[str, list[dict]] = {}
    for r in rules:
        by_group.setdefault(r["group"], []).append(r)
    for group in ordered_groups(by_group):
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| Rule | Score | Lines | Summary | Issues |")
        lines.append("|------|------:|------:|---------|--------|")
        for r in sorted(by_group[group], key=lambda x: x["id"]):
            issues = "; ".join(r["issues"] + r["score_notes"]) or "—"
            lines.append(
                f"| [{r['id']}]({rel_link(r['path'])}) | {r['score']} | {r['lines']} | {r['summary']} | {issues} |"
            )
        lines.append("")

    # Skills section grouped
    lines.append("## Skills")
    lines.append("")
    skill_groups: dict[str, list[dict]] = {}
    for s in skills:
        skill_groups.setdefault(s["group"], []).append(s)

    for group in ordered_groups(skill_groups):
        items = skill_groups[group]
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| Skill | Source | Score | Lines | Summary | Issues |")
        lines.append("|-------|--------|------:|------:|---------|--------|")
        for s in sorted(items, key=lambda x: (x["source"], x["id"])):
            if s["source"] == "cursor-config":
                link = f"[{s['id']}]({rel_link(s['path'])})"
            else:
                link = f"`{s['id']}` (`~/.cursor/skills-cursor/{s['id']}/`)"
            issues = "; ".join(s["issues"] + s["score_notes"]) or "—"
            dup = ""
            if s["id"] == "create-skill" and s["source"] == "skills-cursor":
                dup = "; overlaps cursor-config `create-skill` (different scope)"
                issues = (issues + dup) if issues != "—" else dup.strip("; ")
            lines.append(
                f"| {link} | {s['source']} | {s['score']} | {s['lines']} | {s['summary'][:120]}{'…' if len(s['summary'])>120 else ''} | {issues} |"
            )
        lines.append("")

    # Cross-cutting notes
    lines.extend(
        [
            "## Cross-cutting findings",
            "",
            "### Duplicate / overlapping names",
            "",
            "| Name | Locations | Recommendation |",
            "|------|-----------|----------------|",
            "| `create-skill` | cursor-config (workspace canonical) + skills-cursor (generic Cursor template) | Use cursor-config skill for shared workspace skills; built-in for global Cursor authoring. |",
            "| `review` vs `review-bugbot` / `review-security` | skills-cursor | `review` is a router; prefer specific review skills when intent is known. |",
            "",
            "### Policy alignment",
            "",
            "- Consumer repos have **no** `.cursor/rules` or `.cursor/skills` — aligned with cursor-config readme.",
            "- `data-solution-2026/.cursor/troubleshooting-errors.md` is an ERR log artifact referenced by `issue-inventory` rule, not a Cursor rule file.",
            "- `issue-inventory` glob `data-solution-2026/**` requires multi-root workspace with cursor-config present.",
            "",
            "### Skills with TOC before frontmatter",
            "",
            "Several cursor-config skills place the generated TOC above YAML frontmatter (valid for docs, non-standard for skill discovery). Consider moving frontmatter to line 1 per `create-skill` template.",
            "",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
