---
name: create-design-pattern
description: >-
  Creates compact, technology-agnostic design pattern markdown in
  data-engineering-design-patterns/design-patterns/. Use when adding or
  rewriting a pattern in Data Engineering Design Patterns.
---

# Create design pattern

## Target

- Repo: `data-engineering-design-patterns/`
- Path: `design-patterns/{kebab-case}.md`
- Title: `#` sentence case; filename kebab-case

## Style

- **Short and simple** — shortest correct text; one idea per sentence; cut filler and repetition.
- **Positive scope only** — describe what the pattern *is* and *does*. Do not state what it does *not* do. 
- **Generic** — no vendors, products, or solution-specific names in examples.
- **Declarative** — entities and constraints (*what*), not build steps (*how*).
- **Compact** — short sections; do not repeat the summary in every component.
- **Entities** — `` `EntityName` `` on first mention per component.
- **Examples** — at most two neutral bullets per component, only when they clarify.
- **Cross-links** — only to other patterns when the relationship matters (one line).

No `implementation/` content in pattern files.

## Rewrites

When the user edits a pattern file and asks for a rewrite or review:

- Treat their wording, entity names, section structure, and concepts as intentional — **keep** them unless they ask to change them.
- Improve spelling, structure, TOC/structure blocks, and brevity **around** their concepts; do not “restore” an older version of ideas they replaced.

## Sections

| Section | Guidance |
|---------|----------|
| Purpose | Problem + pattern intent (≤2 short paragraphs). |
| Benefits | 3–5 one-line bullets. |
| Summary | One paragraph; core idea only. |
| Components | 4–8 `###` subsections; 1–2 sentences each. Optional numbered flow as last subsection (≤5 steps). |
| Rules | Optional; 3–6 short `###` rules stating required behavior (not out-of-scope disclaimers). Omit for catalog-only patterns. |

Skip: Definitions, Assumptions, Processes unless essential.

## Workflow

1. Draft from [TEMPLATE.md](TEMPLATE.md).
2. Regenerate (repo root):

```bash
python ../cursor-config/scripts/update_markdown_docs.py --toc-only design-patterns/{stem}.md
python ../cursor-config/scripts/update_markdown_docs.py --structure-only
python ../cursor-config/scripts/review_markdown.py design-patterns/{stem}.md
```

3. Fix review **errors**; do not hand-edit TOC/structure markers.

## Related skills

`markdown-toc`, `markdown-project-structure`, `review-markdown-structure`

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Create Design Pattern
      - [Create design pattern](SKILL.md)
      - [{Title}](TEMPLATE.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
