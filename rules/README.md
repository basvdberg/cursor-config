# Cursor rules (cursor-config)

## Table of contents

<!-- markdown-toc:start -->
- [Activation](#activation)
- [Rule vs skill policy](#rule-vs-skill-policy)
- [Frontmatter](#frontmatter)
  - [Multi-root workspace](#multi-root-workspace)
- [Rule index](#rule-index)
- [Enforcement](#enforcement)
- [Related](#related)
<!-- markdown-toc:end -->

Shared agent rules for the Data Engineering workspace. **Author and edit here only** — do not add `.cursor/rules/` in consumer repositories.

## Activation

| Mechanism | Rules | Skills |
|-----------|-------|--------|
| **Install** | None — rules are not junctioned | `install-cursor.ps1` → `~/.cursor/skills/` |
| **Runtime** | Cursor loads when `cursor-config` is in the workspace | Always available via junctions |
| **Recommended workspace** | [Data Engineering 2.0.code-workspace](../../Data%20Engineering%202.0.code-workspace) (parent folder) | Same |

If you open a single consumer repo without `cursor-config`, skills still work but **rules do not**.

## Rule vs skill policy

| Use a **rule** (`.mdc`) when | Use a **skill** (`SKILL.md`) when |
|------------------------------|-----------------------------------|
| Constraint is short (under ~50 lines) | Workflow has multiple steps or checklists |
| Should apply always or when certain files are open | Needs scripts, templates, or reference files |
| One concern (naming, TOC shape, no private links) | Domain procedures (deploy, SSH, retro, markdown updater) |

Skills carry detail; rules point agents to skills when needed. Example: `markdown-folder-kebab-case` rule + `naming-convention-files-folders` skill.

Author new shared skills per [create-skill](../skills/authoring/create-skill/SKILL.md). Migrate stray `.cursor/rules/*.mdc` from consumer repos into this folder or into skills.

## Frontmatter

```yaml
---
description: Brief description (shown in rule picker)
globs: **/*.md          # optional — file-scoped activation
alwaysApply: false      # true = every session in this workspace
---
```

### Multi-root workspace

- `alwaysApply: true` — applies across all workspace folders when `cursor-config` is included.
- `globs: **/*.md` — matches markdown in every workspace root.
- `globs: data-solution-2026/**` — matches paths prefixed with the **workspace folder name** (works in `.code-workspace`; breaks if that repo is opened alone or renamed).

## Rule index

| Rule | `alwaysApply` | `globs` | Purpose |
|------|---------------|---------|---------|
| [no-private-git-repo-links](no-private-git-repo-links.mdc) | yes | — | No clickable URLs to private Git repos |
| [markdown-folder-kebab-case](markdown-folder-kebab-case.mdc) | no | `**/*.{md,mdc}` | kebab-case for new/renamed markdown paths |
| [markdown-toc-no-title](markdown-toc-no-title.mdc) | no | `**/*.md` | TOC excludes h1, self-ref, Project structure |
| [issue-inventory](issue-inventory.mdc) | no | `data-solution-2026/**` | ERR log, INC promotion, release retro index |

## Enforcement

| Check | Tool |
|-------|------|
| kebab-case paths | `pre_commit.py` (strict), `review_markdown.py` |
| TOC / structure markers | `pre_commit.py`, `update_markdown_docs.py` |
| Private repo links in docs | `audit_cursor_config.py` |
| Skill frontmatter, broken links | `audit_cursor_config.py` |

Run audit from this repo:

```powershell
python scripts/audit_cursor_config.py
```

## Related

- [cursor-config readme](../readme.md) — install skills and Git hooks
- [agent smoke tests](../doc/agent-smoke-tests.md) — quarterly agent behavior checks

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../readme.md)
  - Doc
    - [Agent smoke tests](../doc/agent-smoke-tests.md)
    - [Cursor rules & skills dashboard](../doc/cursor-dashboard.md)
  - Githooks
  - Rules
  - Skills
    - Authoring
      - Create Design Pattern
        - [Create design pattern](../skills/authoring/create-design-pattern/SKILL.md)
        - [{Title}](../skills/authoring/create-design-pattern/TEMPLATE.md)
      - Create Skill
        - [Create skill (cursor-config)](../skills/authoring/create-skill/SKILL.md)
    - Basnas
      - Basnas Ssh
        - [BasNAS SSH (docker and git)](../skills/basnas/basnas-ssh/SKILL.md)
      - Deploy Basnas Container
        - Templates
        - [Fix admin hostname not resolving](../skills/basnas/deploy-basnas-container/dns-basnas-setup.md)
        - [Examples](../skills/basnas/deploy-basnas-container/examples.md)
        - [NGINX as HTTPS edge on port 443 (local server / QNAP)](../skills/basnas/deploy-basnas-container/nginx-on-443.md)
        - [local server deployment reference](../skills/basnas/deploy-basnas-container/reference.md)
        - [Deploy container service on local server](../skills/basnas/deploy-basnas-container/SKILL.md)
        - [Troubleshooting “Your connection is not private” (*.example)](../skills/basnas/deploy-basnas-container/troubleshooting-tls.md)
        - [local server URL map](../skills/basnas/deploy-basnas-container/url-map.md)
      - Deploy Data Solution Basnas
        - [Deploy Data Solution 2026 to BasNAS (CI/CD)](../skills/basnas/deploy-data-solution-basnas/SKILL.md)
    - Coding Standards
      - Naming Convention Files Folders
        - [Naming convention for files and folders](../skills/coding-standards/naming-convention-files-folders/SKILL.md)
      - Pretty Color Logging
        - [Pretty Color Logging](../skills/coding-standards/pretty-color-logging/SKILL.md)
      - Variable Naming
        - [Variable naming](../skills/coding-standards/variable-naming/SKILL.md)
    - Markdown
      - Markdown Project Structure
        - [Markdown project structure](../skills/markdown/markdown-project-structure/SKILL.md)
      - Markdown Toc
        - [Markdown table of contents](../skills/markdown/markdown-toc/SKILL.md)
      - Review Markdown Structure
        - [Review Markdown structure](../skills/markdown/review-markdown-structure/SKILL.md)
    - Operations
      - Release Details Updater
        - [Release Details Updater](../skills/operations/release-details-updater/SKILL.md)
      - Release Retrospective
        - [Release retrospective](../skills/operations/release-retrospective/SKILL.md)
      - Troubleshooting Error Log
        - [Examples](../skills/operations/troubleshooting-error-log/examples.md)
        - [Troubleshooting error reference](../skills/operations/troubleshooting-error-log/reference.md)
        - [Troubleshooting error log](../skills/operations/troubleshooting-error-log/SKILL.md)
    - Sync
      - Browser Bookmarks Sync
        - [Browser bookmarks sync](../skills/sync/browser-bookmarks-sync/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
