## Table of contents

<!-- markdown-toc:start -->
- [Goal](#goal)
- [Document layout](#document-layout)
- [Design patterns section](#design-patterns-section)
- [Checks](#checks)
- [Run the reviewer](#run-the-reviewer)
- [Agent workflow](#agent-workflow)
- [Report format](#report-format)
- [Related skills](#related-skills)
<!-- markdown-toc:end -->

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

## Document layout

Standard order for solution and engineering content files:

1. `#` document title  
2. `## Table of contents` (auto-generated block)  
3. **`## Design patterns`** — only on architecture/design docs (see below)  
4. Body sections (`##` …)  
5. `## Project structure` (auto-generated block)

## Design patterns section

Use this section only when the document describes **architecture or design** (how the solution is structured, metadata layout, CI/CD design, orchestration plans, and similar). Place **`## Design patterns` immediately after the table of contents** and before any other body section.

**Purpose:** Link to the patterns this document applies. Do **not** redefine what a design pattern is or restate pattern rules here—that belongs in [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) ([Purpose](https://github.com/basvdberg/data-engineering-design-patterns/blob/main/readme.md#purpose) and each pattern file).

**Content (keep brief):**

- One short intro sentence: this doc describes *how this repo* applies the patterns (optional).
- A bullet list of **used** patterns only, each linking to  
  `https://github.com/basvdberg/data-engineering-design-patterns/blob/main/design-patterns/{data-engineering|generic}/{kebab-name}.md`
- Per bullet: **one line** on the PoC-specific role (path, tool, or file)—not a second definition of the pattern.

**Authoring rules:**

| Do | Don't |
|----|--------|
| Name and link an existing pattern when the doc implements or configures it | Invent a new concept name when a pattern already covers it |
| Point readers to the pattern for purpose, rules, and benefits | Copy the pattern’s Purpose, Summary, or Rules into implementation docs |
| Add a new pattern in `data-engineering-design-patterns` when the idea is reusable | Document one-off PoC behaviour as if it were a new pattern |

**Required** on `.md` files under `doc/design/` in `data-solution-2026` and `data-engineering-2026` (for example `meta-data-design.md`, `ci-cd.md`, `architecture.md`).

**Do not add** a Design patterns section to the repo root `readme.md`, `lessons-learned.md`, runbooks (`getting-started.md`), implementation readmes, data-mapping docs, or other non-design content—even when those files mention patterns in prose.

**Exempt** everywhere: `prompts.md`, `*.handlebars.md`, `SKILL.md`, files under `data-engineering-design-patterns/design-patterns/`, `definitions/`, `implementation/`, and the design-patterns repo root `readme.md`.

Example:

```markdown
## Design patterns

This document describes how DSA metadata is laid out in Git. Definitions: [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns/blob/main/readme.md#purpose).

- [Data solution](https://github.com/basvdberg/data-engineering-design-patterns/blob/main/design-patterns/data-engineering/data-solution.md) — `connection/`, `data-object/`, `data-object-mapping/` folders in this repo.
- [Separate what and how](https://github.com/basvdberg/data-engineering-design-patterns/blob/main/design-patterns/generic/separate-what-and-how.md) — path IDs in JSON; Python extractors implement *how*.
```

Regenerate the TOC after adding the section (`markdown-toc` skill).

## Checks

| Check | Rule |
|-------|------|
| **Spelling** | Flag unknown English words (skip code fences, URLs, paths, `<!-- -->`, inline code). Allow domain terms in `scripts/domain-words.txt`. |
| **Naming** | Folders and `.md` stems use `kebab-case` (`[a-z0-9]+(-[a-z0-9]+)*`). Exceptions: `readme.md`, `prompts.md`, `*.handlebars.md` template stems. |
| **Document title** | Exactly one `#` title as the first non-empty line. |
| **Heading tree** | Headings are `##`–`######` only in body; no level skips (e.g. `##` then `####`); document title (`#`) not repeated in TOC. |
| **Paragraphs under headings** | No orphan prose between TOC/structure blocks and the first `##`, or between sections (prose must follow a heading). |
| **Table of contents** | Required on content `.md` files: `## Table of contents` + `markdown-toc` markers. Exempt: `prompts.md`, `*.handlebars.md` (ADL templates). |
| **Design patterns** | Required `## Design patterns` after TOC only under `doc/design/` (see [Design patterns section](#design-patterns-section)). Listed in the TOC when present. |
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
2. Fix **errors** first: naming, missing markers, missing Design patterns section, heading skips, orphan paragraphs.
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

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](../browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Deploy Basnas Container
      - Templates
      - [Fix `admin.basnas` not resolving](../deploy-basnas-container/dns-basnas-setup.md)
      - [Examples](../deploy-basnas-container/examples.md)
      - [NGINX as HTTPS edge on port 443 (BasNAS / QNAP)](../deploy-basnas-container/nginx-on-443.md)
      - [BasNAS deployment reference](../deploy-basnas-container/reference.md)
      - [Deploy container service on BasNAS](../deploy-basnas-container/SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.basnas)](../deploy-basnas-container/troubleshooting-tls.md)
      - [BasNAS URL map](../deploy-basnas-container/url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](SKILL.md)
- Related repositories
  - [Browser bookmarks sync](https://github.com/basvdberg/browser-bookmarks-sync)
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
