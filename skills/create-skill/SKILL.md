## Table of contents

<!-- markdown-toc:start -->
- [Canonical location](#canonical-location)
- [Directory layout](#directory-layout)
- [SKILL.md frontmatter](#skillmd-frontmatter)
- [Workflow](#workflow)
  - [1. Discovery](#1-discovery)
  - [2. Implement](#2-implement)
  - [3. Install](#3-install)
  - [4. Document](#4-document)
  - [5. Commit](#5-commit)
- [Migrate stray skills](#migrate-stray-skills)
- [Quality checklist](#quality-checklist)
- [Related](#related)
<!-- markdown-toc:end -->

## Table of contents


---
name: create-skill
description: >-
  Creates Cursor Agent Skills in the cursor-config repository (canonical store).
  Use when authoring a new skill, asking about SKILL.md structure, or migrating
  skills from ~/.cursor/skills or consumer .cursor/skills folders.
disable-model-invocation: true
---

# Create skill (cursor-config)

All **shared** Cursor agent skills for this workspace live in the **cursor-config** Git repository — not in `~/.cursor/skills` directly and not in consumer repos under `.cursor/skills/`.

## Canonical location

| What | Path |
|------|------|
| **Author / edit** | `cursor-config/skills/<skill-name>/SKILL.md` |
| **Runtime (Cursor)** | `%USERPROFILE%\.cursor\skills\<skill-name>\` (junction → cursor-config) |

Resolve `cursor-config` as:

- Folder `cursor-config/` in the **Data Engineering 2.0** workspace, or
- Clone path the user provides, or
- `$env:CURSOR_CONFIG_ROOT` when set.

**Never:**

- Create or edit skills under `~/.cursor/skills-cursor/` (Cursor-managed built-ins).
- Copy skill source into `~/.cursor/skills/` by hand (that directory is install output only).
- Add `.cursor/skills/` in consumer repos (`data-solution-2026`, etc.) unless the user explicitly wants a **repo-private** skill that must not be shared.

## Directory layout

```text
cursor-config/skills/<skill-name>/
├── SKILL.md              # Required
├── reference.md          # Optional
├── examples.md           # Optional
└── scripts/              # Optional
```

## SKILL.md frontmatter

```markdown
---
name: skill-name
description: Third-person WHAT and WHEN (trigger terms for discovery).
disable-model-invocation: true
---
```

- `name`: lowercase, hyphens, max 64 chars.
- `description`: third person; include **what** it does and **when** to use it.
- Default `disable-model-invocation: true` so the skill loads when named or referenced; omit only if ambient auto-invoke is intended.

If the user supplies exact wording for the skill body, use it **verbatim** — do not paraphrase.

## Workflow

### 1. Discovery

Gather: purpose, trigger scenarios, supporting files/scripts, and whether the skill is workspace-wide (almost always → cursor-config).

### 2. Implement

1. Create `cursor-config/skills/<skill-name>/`.
2. Write `SKILL.md` (and optional `reference.md`, `examples.md`, `scripts/`).
3. Keep `SKILL.md` under ~500 lines; link one level deep for extra detail.

### 3. Install

From `cursor-config`:

```powershell
.\scripts\install-skills.ps1
```

This replaces each `%USERPROFILE%\.cursor\skills\<name>` junction with the new skill folder.

### 4. Document

- Update `cursor-config/readme.md` project-structure block (run `update_markdown_docs.py` from a consumer root if TOC/structure markers are used elsewhere).
- Mention the skill in the parent workspace `readme.md` only when it is user-facing.

### 5. Commit

Commit in **cursor-config** (user must ask before `git commit`). Consumer repos should not carry duplicate skill trees.

## Migrate stray skills

When a skill exists outside cursor-config:

| Source | Action |
|--------|--------|
| `~/.cursor/skills/<name>/` (real directory, not junction) | Move files to `cursor-config/skills/<name>/`, delete the old folder, run `install-skills.ps1` |
| `<consumer>/.cursor/skills/<name>/` | Move to `cursor-config/skills/<name>/`, delete consumer copy, run `install-skills.ps1` |
| `.cursor/rules/*.mdc` or `.cursor/commands/*.md` | Follow Cursor **migrate-to-skills** into **cursor-config/skills/** (not consumer `.cursor/skills/`) |

Preserve skill body content character-for-character when migrating.

## Quality checklist

- [ ] Stored under `cursor-config/skills/`
- [ ] `install-skills.ps1` run after add/rename
- [ ] Description includes WHAT + WHEN, third person
- [ ] No Windows backslash paths in skill text
- [ ] No duplicate copy in consumer `.cursor/skills/`

## Related

- Built-in Cursor authoring reference: `~/.cursor/skills-cursor/create-skill/` (read only; do not edit).
- Workspace install: `cursor-config/scripts/install-cursor.ps1`

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Rules
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](../browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Create Skill
      - [Create skill (cursor-config)](SKILL.md)
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
