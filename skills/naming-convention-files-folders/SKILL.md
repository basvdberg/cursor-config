## Table of contents

<!-- markdown-toc:start -->
- [Goal](#goal)
- [GitHub baseline (most common)](#github-baseline-most-common)
- [Your rules (apply on every new name)](#your-rules-apply-on-every-new-name)
- [Decision checklist](#decision-checklist)
- [Examples](#examples)
- [Layer and technical exceptions](#layer-and-technical-exceptions)
- [Agent workflow](#agent-workflow)
- [Related skills](#related-skills)
<!-- markdown-toc:end -->

## Table of contents


---
name: naming-convention-files-folders
description: >-
  Names files and folders using common GitHub conventions plus singular, short,
  non-conjugated names. Use when creating or renaming paths, reviewing folder
  structure, scaffolding repos, or when the user asks about naming conventions.
---

# Naming convention for files and folders

## Goal

Choose names that match what most open-source GitHub repositories use, and stay easy to read in URLs, terminals, and cross-platform paths.

## GitHub baseline (most common)

| Item | Convention |
|------|------------|
| **Folders** | Lowercase **kebab-case**: `design-patterns`, `event-bus`, `src` |
| **Files** | Lowercase **kebab-case** stem + extension: `data-extractor.md`, `docker-compose.yml` |
| **Pattern** | `[a-z0-9]+(-[a-z0-9]+)*` — hyphens between words, no spaces or underscores |
| **Repo root** | Often `readme.md` (lowercase) or `README.md` (GitHub renders both) |
| **Well-known roots** | Short fixed names: `.github`, `docs`, `scripts`, `tests`, `src` |

Avoid `CamelCase`, `snake_case`, and `PascalCase` for generic GitHub paths unless a **project rule** explicitly requires them (document the exception in that repo).

## Your rules (apply on every new name)

Use these in addition to the GitHub baseline:

1. **Use singular over plural.**  
   Prefer `doc`, `script`, `mapping`, `extractor` — not `docs`, `scripts`, `mappings`, `extractors`.  
   Exception: established ecosystem names (`docs`, `.github`) where singular would confuse readers.

2. **Prefer short names.**  
   Drop filler (`data`, `file`, `folder`) when context is obvious.  
   `config` not `configuration-settings`; `poll` not `data-object-poller` unless the longer form is required for clarity.

3. **Do not use conjugations.**  
   Names are **nouns or stable labels**, not verbs in progressive, past, or gerund form.  
   - Good: `extract`, `poll`, `load`, `schema`, `mapping`  
   - Avoid: `extracting`, `polled`, `loads`, `loading`, `configured`

Combine with kebab-case: `change-detector`, `event-bus`, `landing-path` — not `detecting-changes` or `events-bus`.

## Decision checklist

Before creating a path, verify:

- [ ] Lowercase kebab-case (unless repo documents another rule)
- [ ] Singular noun where a choice exists
- [ ] As short as clarity allows
- [ ] No `-ing`, `-ed`, or verb phrases as the core token
- [ ] No spaces, dots inside the name (except extension), or mixed case
- [ ] Name still meaningful without the parent folder (e.g. `poll` inside `implementation/` may need `data-object-poll` for disambiguation)

## Examples

| Avoid | Prefer | Why |
|-------|--------|-----|
| `Extractors/` | `extractor/` | Singular; kebab-case |
| `processing-pipeline/` | `pipeline/` or `process/` | No conjugation; shorter |
| `loaded-events/` | `event/` or `load-event/` | No past tense |
| `configuring-sources.json` | `source-config.json` | Noun phrase, not gerund |
| `dataObjectMappings/` | `data-object-mapping/` | GitHub kebab-case |
| `KNMI_Daggegevens/` | `knmi/daggegevens` or project-specific acronym rule | Default is kebab |

## Layer and technical exceptions

Keep industry-standard tokens even if they break “short singular” slightly:

- Numeric layer prefixes: `000_Source`, `100_Landing_Area` (when the repo already uses them)
- Acronyms in data paths: `KNMI`, `OData` — only when they are proper names, not invented verbs
- Schema or tool-mandated names: follow the external spec; do not rename for style alone

**Do not rename JSON schema property names** (e.g. keep `dataObjectMappings` in DSA JSON). Only filesystem folders and non-schema file paths follow this skill.

When a repo uses a **documented override**, follow that repo’s `Conventions` or `.cursor-config.json`.

## Agent workflow

1. Read existing siblings in the target directory; match the dominant pattern.
2. Propose a name using singular, short, non-conjugated kebab-case.
3. If renaming, update imports, links, and config paths in the same change.
4. In Data Engineering workspaces, run `review-markdown-structure` or pre-commit after markdown path changes.

## Related skills

- `review-markdown-structure` — validates kebab-case for markdown repos (with per-repo overrides)
- `create-design-pattern` — design pattern *files* use kebab-case stems; titles are sentence case

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
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](SKILL.md)
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
