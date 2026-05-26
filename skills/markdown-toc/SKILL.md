---
name: markdown-toc
description: >-
  Generates and refreshes Markdown table-of-contents blocks from ##–###### headings only.
  Never includes the document # title, Table of contents, or Project structure in the TOC.
  Use when adding or editing .md files, TOC requests, or automatic TOC updates on commit.
---

# Markdown table of contents

## Goal

Keep a **Table of contents** near the top of each Markdown file, synced to **`##` through `######` headings only** in the body. The document **`#` title is never a TOC entry.**

## Rules (mandatory)

### 1. Exclude the document title (h1)

- The first line of the file is `# Document title`. That line is **not** part of the TOC.
- **Never** add `- [Document Title](#document-title)` to the TOC (editors and templates often suggest this—reject it).
- The updater ignores every `#` / h1 line and drops any `##`–`######` heading whose anchor matches the title slug (duplicate title headings in the body).

**Correct:**

```markdown
# Data Engineering 2026

## Purpose
```

**Wrong** (title must not appear inside the markers):

```markdown
```

### 2. Exclude meta sections

- Do **not** list `## Table of contents` or `## Project structure` in the TOC.
- The first TOC entry is the first real content section (e.g. `## Purpose`).

### 3. Formatting

- GitHub-style anchors: lowercase, spaces to hyphens, strip punctuation.
- Skip headings inside fenced code blocks.
- Indent nested bullets from the shallowest included heading level.

## Run the updater

**Preferred** — [cursor-config](https://github.com/basvdberg/cursor-config) script (from a consumer repo root):

```bash
python ../cursor-config/scripts/update_markdown_docs.py --toc-only
python ../cursor-config/scripts/update_markdown_docs.py --toc-only path/to/file.md
```

**Skill wrapper** (after `cursor-config/scripts/install-skills.ps1`):

```bash
python ~/.cursor/skills/markdown-toc/scripts/update_toc.py
```

Run from the consumer Git repository root.

## Agent workflow

1. Keep exactly one `#` title at the top, then `## Table of contents`, then the body.
2. **Do not hand-edit** the list between `markdown-toc:start` and `markdown-toc:end`.
3. Run `--toc-only` after heading changes.
4. Verify: open the TOC block and confirm **no** line matches the `#` title and **no** `Table of contents` / `Project structure` entries.

## Site map vs table of contents

The repository **site map** (linked folders and `.md` files) belongs only in the **Project structure** block (`markdown-project-structure` skill). Never put the site map in the TOC.

## Checklist

- [ ] TOC regenerated via script
- [ ] **No** `#` document title in the TOC
- [ ] **No** `Table of contents` or `Project structure` in the TOC
- [ ] Indents match heading depth

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
