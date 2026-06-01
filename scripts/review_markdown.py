#!/usr/bin/env python3
"""Review Markdown structure, naming, headings, TOC/structure blocks, and spelling."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DOMAIN_WORDS = SCRIPT_DIR / "domain-words.txt"
TYPOS_FILE = SCRIPT_DIR / "typos.json"

TOC_START = "<!-- markdown-toc:start -->"
TOC_END = "<!-- markdown-toc:end -->"
STRUCT_START = "<!-- markdown-project-structure:start -->"
STRUCT_END = "<!-- markdown-project-structure:end -->"

EXCLUDED_FROM_BLOCKS = frozenset({"prompts.md"})
EXCLUDED_FROM_STRUCTURE_CHECKS = frozenset({"prompts.md"})
HANDLEBARS_SUFFIX = ".handlebars.md"
DESIGN_PATTERNS_HEADING = re.compile(
    r"^##\s+Design patterns\s*(?:\r)?$",
    re.IGNORECASE | re.MULTILINE,
)
REPOS_REQUIRE_DESIGN_PATTERNS = frozenset(
    {"data-solution-2026", "data-engineering-2026"}
)
# Architecture/design docs only (not root readme, lessons learned, runbooks, etc.)
DESIGN_PATTERNS_REQUIRED_PREFIX = "doc/design/"
PATTERN_REPO_EXEMPT_PREFIXES = ("design-patterns/", "definitions/", "implementation/")
sys.path.insert(0, str(SCRIPT_DIR))
from cursor_config import folder_name_valid  # noqa: E402

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE = re.compile(r"^```")
PROSE_START = re.compile(r"^[A-Za-z\[\"]")
SKIP_SPELL_DIRS = frozenset({".git", ".cursor", "node_modules", "__pycache__"})


class Issue:
    def __init__(self, level: str, path: Path, message: str, line: int | None = None) -> None:
        self.level = level
        self.path = path
        self.message = message
        self.line = line

    def format(self, base: Path) -> str:
        rel = self.path
        try:
            rel = self.path.relative_to(base)
        except ValueError:
            pass
        loc = f" (line {self.line})" if self.line else ""
        return f"{self.level:5}  {rel}{loc}: {self.message}"


def load_domain_words() -> set[str]:
    words: set[str] = set()
    if DOMAIN_WORDS.is_file():
        for line in DOMAIN_WORDS.read_text(encoding="utf-8").splitlines():
            w = line.strip().lower()
            if w and not w.startswith("#"):
                words.add(w)
    return words


def load_typos() -> dict[str, str]:
    if not TYPOS_FILE.is_file():
        return {}
    return json.loads(TYPOS_FILE.read_text(encoding="utf-8"))


def get_spell_checker():
    try:
        from spellchecker import SpellChecker  # type: ignore

        return SpellChecker(distance=1)
    except ImportError:
        return None


def discover_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in paths:
        root = root.resolve()
        if root.is_file() and root.suffix.lower() == ".md":
            files.append(root)
            continue
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if any(part in SKIP_SPELL_DIRS or part.startswith(".") for part in path.parts):
                continue
            files.append(path)
    return sorted(set(files))


def strip_generated_sections(content: str) -> str:
    for start, end in (
        (TOC_START, TOC_END),
        (STRUCT_START, STRUCT_END),
    ):
        content = re.sub(
            re.escape(start) + r"[\s\S]*?" + re.escape(end),
            "",
            content,
            flags=re.MULTILINE,
        )
    content = re.sub(r"\n## Table of contents\s*\n+", "\n", content, flags=re.IGNORECASE)
    content = re.sub(r"\n## Project structure\s*\n+", "\n", content, flags=re.IGNORECASE)
    return content


def is_handlebars_template(path: Path) -> bool:
    return path.name.lower().endswith(HANDLEBARS_SUFFIX)


def is_exempt_structure_file(path: Path) -> bool:
    if path.name.lower() in EXCLUDED_FROM_STRUCTURE_CHECKS:
        return True
    return is_handlebars_template(path)


def requires_design_patterns_section(path: Path, repo_root: Path) -> bool:
    if path.name == "SKILL.md":
        return False
    if is_exempt_structure_file(path):
        return False
    if repo_root.name not in REPOS_REQUIRE_DESIGN_PATTERNS:
        return False
    if repo_root.name == "data-engineering-design-patterns":
        return False
    if path.suffix.lower() != ".md":
        return False
    try:
        rel = path.relative_to(repo_root).as_posix()
    except ValueError:
        return False
    return rel.startswith(DESIGN_PATTERNS_REQUIRED_PREFIX)


def check_design_patterns_section(
    path: Path, content: str, repo_root: Path, issues: list[Issue]
) -> None:
    if not requires_design_patterns_section(path, repo_root):
        return
    if repo_root.name == "data-engineering-design-patterns":
        try:
            rel = path.relative_to(repo_root).as_posix()
        except ValueError:
            rel = ""
        if rel.startswith(PATTERN_REPO_EXEMPT_PREFIXES):
            return
        if rel == "readme.md":
            return
    if not DESIGN_PATTERNS_HEADING.search(content):
        issues.append(
            Issue(
                "ERROR",
                path,
                "missing '## Design patterns' section after Table of contents",
            )
        )


def check_naming(path: Path, repo: Path, issues: list[Issue]) -> None:
    rel = path.relative_to(repo)
    stem = path.stem
    if path.name.lower() == "readme.md":
        return
    if is_handlebars_template(path):
        return
    if path.name in EXCLUDED_FROM_BLOCKS:
        return
    if not KEBAB.match(stem):
        issues.append(
            Issue("ERROR", path, f"file stem '{stem}' is not kebab-case")
        )
    for part in rel.parent.parts:
        if not folder_name_valid(part):
            issues.append(
                Issue("ERROR", path, f"folder '{part}' is not kebab-case")
            )


def check_blocks(path: Path, content: str, issues: list[Issue]) -> None:
    if is_exempt_structure_file(path):
        return
    lowered = content.lower()
    if TOC_START not in content or TOC_END not in content:
        issues.append(Issue("ERROR", path, "missing markdown-toc markers"))
    if STRUCT_START not in content or STRUCT_END not in content:
        issues.append(Issue("ERROR", path, "missing markdown-project-structure markers"))
    if "## table of contents" not in lowered:
        issues.append(Issue("ERROR", path, "missing '## Table of contents' heading"))
    if "## project structure" not in lowered:
        issues.append(Issue("ERROR", path, "missing '## Project structure' heading"))


def check_headings_and_orphans(path: Path, content: str, issues: list[Issue]) -> None:
    if is_exempt_structure_file(path):
        return
    body = strip_generated_sections(content)
    lines = body.splitlines()

    if not lines or not lines[0].startswith("# "):
        issues.append(Issue("ERROR", path, "document must start with a single # title", 1))
        return

    in_fence = False
    last_level = 1
    active_heading = False
    seen_content_heading = False

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if FENCE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith("<!--") or stripped.startswith("|") or stripped.startswith("- "):
            if active_heading:
                continue
            if stripped.startswith("- ") and seen_content_heading:
                continue
        hm = HEADING.match(line)
        if hm:
            level = len(hm.group(1))
            if level == 1:
                if i != 1:
                    issues.append(
                        Issue("ERROR", path, "only one # title allowed at top of file", i)
                    )
                last_level = 1
                active_heading = True
                if level >= 2:
                    seen_content_heading = True
                continue
            if level < 2:
                continue
            if level > last_level + 1:
                issues.append(
                    Issue(
                        "ERROR",
                        path,
                        f"heading level skip H{last_level} -> H{level}",
                        i,
                    )
                )
            last_level = level
            active_heading = True
            seen_content_heading = True
            continue

        if stripped.startswith(("#", "!", "```", "<!--", "|", "- ", "* ", ">")):
            continue
        if re.match(r"^[-\d]+\.\s", stripped):
            continue
        if (
            PROSE_START.match(stripped)
            and not seen_content_heading
            and not stripped.startswith("[")
        ):
            issues.append(
                Issue(
                    "ERROR",
                    path,
                    "orphan paragraph before first content heading (##)",
                    i,
                )
            )
            seen_content_heading = True
        elif PROSE_START.match(stripped) and not active_heading:
            issues.append(
                Issue("ERROR", path, "orphan paragraph not under a heading", i)
            )


def tokenize_words(text: str) -> list[tuple[str, int]]:
    results: list[tuple[str, int]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for match in re.finditer(r"[A-Za-z]{3,}", line):
            word = match.group(0)
            results.append((word, i))
    return results


def check_spelling(
    path: Path,
    content: str,
    issues: list[Issue],
    spell: object | None,
    domain: set[str],
    typos: dict[str, str],
) -> None:
    body = strip_generated_sections(content)
    in_fence = False
    for i, line in enumerate(body.splitlines(), start=1):
        if FENCE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in re.finditer(r"[A-Za-z]{4,}", line):
            raw = match.group(0)
            lower = raw.lower()
            if lower in domain:
                continue
            if lower in typos and typos[lower] != lower:
                issues.append(
                    Issue(
                        "WARN",
                        path,
                        f"known typo '{raw}' -> use '{typos[lower]}'",
                        i,
                    )
                )
                continue
            if spell is None or not raw.islower():
                continue
            if lower in spell:  # type: ignore[operator]
                continue
            issues.append(
                Issue("WARN", path, f"possible misspelling '{raw}'", i)
            )


def apply_typo_fixes(path: Path, typos: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text
    for wrong, right in typos.items():
        updated = re.sub(rf"\b{re.escape(wrong)}\b", right, updated, flags=re.IGNORECASE)
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def run_updater(repo: Path) -> None:
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import cursor_config

        config_root = cursor_config.config_root(repo)
    except (ImportError, FileNotFoundError):
        return
    script = config_root / "scripts" / "update_markdown_docs.py"
    subprocess.run(
        [sys.executable, str(script), "--root", str(repo)],
        cwd=repo,
        check=False,
    )


def review_file(
    path: Path,
    repo: Path,
    spell: object | None,
    domain: set[str],
    typos: dict[str, str],
) -> list[Issue]:
    issues: list[Issue] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(Issue("ERROR", path, f"cannot read file: {exc}"))
        return issues

    check_naming(path, repo, issues)
    check_blocks(path, content, issues)
    check_design_patterns_section(path, content, repo, issues)
    check_headings_and_orphans(path, content, issues)
    if not is_handlebars_template(path):
        check_spelling(path, content, issues, spell, domain, typos)
    return issues


def find_repo_root(path: Path) -> Path:
    for parent in [path, *path.parents]:
        if (parent / ".git").exists():
            return parent
    return path.parent if path.is_file() else path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or repo roots (default: current directory)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply typos.json fixes and run update_markdown_docs.py per repo",
    )
    args = parser.parse_args(argv)

    roots = args.paths or [Path.cwd()]
    files = discover_markdown(list(roots))
    if not files:
        print("No markdown files found.", file=sys.stderr)
        return 1

    typos = load_typos()
    domain = load_domain_words() | set(typos.keys())
    spell = get_spell_checker()
    if spell is None:
        print(
            "note: install pyspellchecker for full spelling checks (pip install pyspellchecker)",
            file=sys.stderr,
        )

    repos_to_fix: set[Path] = set()
    all_issues: list[Issue] = []

    for path in files:
        repo = find_repo_root(path)
        if args.fix:
            repos_to_fix.add(repo)
            apply_typo_fixes(path, typos)
        all_issues.extend(review_file(path, repo, spell, domain, typos))

    if args.fix:
        for repo in sorted(repos_to_fix):
            run_updater(repo)

    by_file: dict[Path, list[Issue]] = {}
    for issue in all_issues:
        by_file.setdefault(issue.path, []).append(issue)

    errors = 0
    warns = 0
    for path in sorted(by_file.keys()):
        for issue in by_file[path]:
            print(issue.format(find_repo_root(path)))
            if issue.level == "ERROR":
                errors += 1
            else:
                warns += 1

    print(
        f"\nReviewed {len(files)} file(s): {errors} error(s), {warns} warning(s).",
        file=sys.stderr,
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
