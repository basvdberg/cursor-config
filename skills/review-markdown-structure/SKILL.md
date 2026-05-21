---
name: review-markdown-structure
description: >-
  Reviews Markdown files for spelling, kebab-case naming, heading hierarchy,
  orphan paragraphs, and required TOC/project-structure blocks. Use when
  reviewing markdown structure, documentation quality, or before committing docs.
---

# Review Markdown structure

## Goal

Validate and fix Markdown documentation across the Data Engineering repos so every content file is well structured, consistently named, and auto-maintained.

## Checks

| Check | Rule |
|-------|------|
| **Spelling** | Flag unknown English words (skip code fences, URLs, paths, `<!-- -->`, inline code). Allow domain terms in `scripts/domain-words.txt`. |
| **Naming** | Folders and `.md` stems use `kebab-case` (`[a-z0-9]+(-[a-z0-9]+)*`). Exceptions: `readme.md`, `prompts.md`, `*.handlebars.md` template stems. |
| **Document title** | Exactly one `#` title as the first non-empty line. |
| **Heading tree** | Headings are `##`–`######` only in body; no level skips (e.g. `##` then `####`); document title (`#`) not repeated in TOC. |
| **Paragraphs under headings** | No orphan prose between TOC/structure blocks and the first `##`, or between sections (prose must follow a heading). |
| **Table of contents** | Required on content `.md` files: `## Table of contents` + `markdown-toc` markers. Exempt: `prompts.md`, `*.handlebars.md` (ADL templates). |
| **Project structure** | Same exempt list: `## Project structure` + `markdown-project-structure` markers at end of file. |

## Run the reviewer

From any repo root (or pass paths):

```bash
python ../cursor-config/scripts/review_markdown.py
python ../cursor-config/scripts/review_markdown.py path/to/file.md
python ../cursor-config/scripts/review_markdown.py --fix
```

After `cursor-config/scripts/install-skills.ps1`, the same entry point is available as:

```bash
python ~/.cursor/skills/review-markdown-structure/scripts/review_markdown.py
```

`--fix` runs `cursor-config/scripts/update_markdown_docs.py` per repo and applies safe typo fixes from `cursor-config/scripts/typos.json`.

Workspace-wide (all three projects):

```bash
python ../cursor-config/scripts/review_markdown.py "c:/Dev2/Data Engineering 2.0/data-engineering-design-patterns" "c:/Dev2/Data Engineering 2.0/data-solution-2026" "c:/Dev2/Data Engineering 2.0/data-engineering-2026"
```

Requires: Python 3.10+. Spelling uses `pyspellchecker` if installed (`pip install pyspellchecker`).

## Agent workflow

1. Run the script without `--fix` and read the report.
2. Fix **errors** first: naming, missing markers, heading skips, orphan paragraphs.
3. Run `--fix` to refresh TOC/structure blocks, then re-run the reviewer.
4. Fix spelling and style manually where the script flags **warnings** (technical terms → add to `domain-words.txt`).
5. Summarize per repo: files OK, files fixed, remaining warnings.

## Report format

```
ERROR  readme.md: orphan paragraph before first heading (line 14)
WARN   readme.md: possible misspelling 'robuust' (line 31)
```

Exit code `1` if any ERROR; `0` if only warnings or clean.

## Related skills

- `markdown-toc` — regenerate heading TOC
- `markdown-project-structure` — regenerate site map block
- Project rule `markdown-folder-kebab-case.mdc` — naming standard
