## Table of contents

<!-- markdown-toc:start -->
- [Target](#target)
- [Style](#style)
- [Rewrites](#rewrites)
- [Sections](#sections)
- [Workflow](#workflow)
- [Related skills](#related-skills)
<!-- markdown-toc:end -->

## Table of contents


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
- Path: `design-patterns/{data-engineering|generic}/{kebab-case}.md`
- Title: `#` sentence case; filename kebab-case
- Naming rule: never include the words `design pattern` in the pattern name, title, or filename.

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
  - Rules
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](../browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](SKILL.md)
      - [{Title}](TEMPLATE.md)
    - Create Skill
      - [Create skill (cursor-config)](../create-skill/SKILL.md)
    - Deploy Basnas Container
      - Templates
      - [Fix admin hostname not resolving](../deploy-basnas-container/dns-basnas-setup.md)
      - [Examples](../deploy-basnas-container/examples.md)
      - [NGINX as HTTPS edge on port 443 (local server / QNAP)](../deploy-basnas-container/nginx-on-443.md)
      - [local server deployment reference](../deploy-basnas-container/reference.md)
      - [Deploy container service on local server](../deploy-basnas-container/SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.example)](../deploy-basnas-container/troubleshooting-tls.md)
      - [local server URL map](../deploy-basnas-container/url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Pretty Color Logging
      - [Pretty Color Logging](../pretty-color-logging/SKILL.md)
    - Release Details Updater
      - [Release Details Updater](../release-details-updater/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
    - Troubleshooting Error Log
      - [Examples](../troubleshooting-error-log/examples.md)
      - [Troubleshooting error reference](../troubleshooting-error-log/reference.md)
      - [Troubleshooting error log](../troubleshooting-error-log/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
