## Table of contents

<!-- markdown-toc:start -->
- [Goal](#goal)
- [Rules — current repository (expanded)](#rules-current-repository-expanded)
- [Rules — related GitHub repositories (not expanded)](#rules-related-github-repositories-not-expanded)
  - [Short description (required)](#short-description-required)
  - [Private repositories (excluded)](#private-repositories-excluded)
- [Example](#example)
- [Run the updater](#run-the-updater)
- [Checklist](#checklist)
<!-- markdown-toc:end -->

## Table of contents


---
name: markdown-project-structure
description: >-
  Generates a project structure block: full nested site map for the current repo only,
  plus related public repositories discovered from incoming/outgoing markdown references.
  Each related repo gets a GitHub link and short description; private repos are omitted
  from the Related repositories section. Use for project structure blocks or updates on commit.
---

# Markdown project structure

## Goal

The **Project structure** block has two **top-level** parts (sibling bullets, same depth):

1. **This repository (expanded)** — one top-level bullet for the repo root, then nested folders and in-repo Markdown files.
2. **Related repositories** — a separate **top-level** section (not nested under the repo root). One line per **public** related repo with a **short description**; **do not** expand other repositories.

## Rules — current repository (expanded)

- **Root** — `- [Document title](relative/path/to/readme.md)` from the readme `#` title.
- **Folders** — plain bullet with a section label (e.g. `Definitions`, `Design patterns`).
- **Markdown files** — `- [Title from # heading](relative/path.md)`; paths relative to the file containing the block.
- **Omit** — `prompts.md`, subfolder `readme.md`, `scripts/`, excluded/tooling dirs.
- **Design-patterns layout** — curated map when a top-level `design-patterns/` folder exists.

## Rules — related GitHub repositories (not expanded)

The updater **discovers** related repos automatically:

| Direction | Detection |
|-----------|-----------|
| **Outgoing** | `https://github.com/{owner}/{repo}` in any `.md` file in **this** repository (except `prompts.md`) |
| **Incoming** | Sibling Git repositories under the same parent folder (workspace) whose `.md` files link to **this** repo on GitHub |

- Use the `origin` remote to determine **owner** and **current repo slug**.
- **Related repositories** is its own top-level bullet; place it after the expanded repo tree (both at top level).
- **Never** use relative paths like `../other-repo/` for cross-repo links (they break on GitHub).
- **Always exclude** `cursor-config` from related repositories (tooling repo, not a content sibling).
- **Always exclude private repositories** from the Related repositories section (no line, no link). Document private repos elsewhere (e.g. a Repositories table in the readme).
- **Do not** add folder trees or file lists for related repositories.

### Short description (required)

Every **public** related repo line ends with ` — ` and a **very short** phrase (about 4–12 words): role or scope, not a full readme.

- Format: `  - [Display name](https://github.com/owner/repo) — short description`

Configure descriptions in **`project-structure-external.json`** → `"descriptions": { "repo-slug": "..." }`. The updater also ships defaults for known workspace repos.

### Private repositories (excluded)

Repositories marked **private** on GitHub (or unknown visibility) are **omitted** from Related repositories entirely.

- Configure slugs to exclude in `"private": ["browser-bookmarks-sync"]` or per-entry `"private": true` in `repositories`.
- Known private repo in this workspace: **browser-bookmarks-sync**.

Optional **`project-structure-external.json`** for labels, descriptions, private slugs to exclude, and public URL overrides (discovery still drives which public repos appear):

```json
{
  "section": "Related repositories",
  "private": ["browser-bookmarks-sync"],
  "labels": {
    "data-engineering-2026": "Data Engineering 2026"
  },
  "descriptions": {
    "data-engineering-2026": "Course and learning materials",
    "data-engineering-design-patterns": "Design pattern catalogue",
    "data-solution-2026": "Data solution proof of concept"
  },
  "repositories": [
    {
      "label": "Data Engineering Design Patterns",
      "url": "https://github.com/basvdberg/data-engineering-design-patterns",
      "description": "Design pattern catalogue"
    }
  ]
}
```

Repos in `repositories` are included only if they are also found by link discovery, except you can use the file to supply labels, descriptions, and URLs for discovered slugs.

## Example

```markdown
- [Data Solution 2026](readme.md)
  - Docs
    - [Markdown automation](docs/markdown-automation.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
```

## Run the updater

```bash
python ../cursor-config/scripts/update_markdown_docs.py --structure-only
python ~/.cursor/skills/markdown-project-structure/scripts/update_structure.py
```

Install skills from [cursor-config](https://github.com/basvdberg/cursor-config) with `scripts/install-skills.ps1`.

## Checklist

- [ ] Only the **current** repo is expanded in the site map
- [ ] `Related repositories` is a **top-level** section (sibling of the repo root, not nested under it)
- [ ] Every **public** related repo has a **short description** after ` — `
- [ ] **Private** repos are **not** listed under Related repositories
- [ ] Public related repos use a **flat GitHub link** plus description
- [ ] Related set matches incoming/outgoing `github.com` references in markdown
- [ ] No `../sibling-repo/` cross-repo paths
- [ ] `markdown-project-structure` markers updated

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
      - [Markdown project structure](SKILL.md)
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
