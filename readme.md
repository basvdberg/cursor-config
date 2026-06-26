# cursor-config

## Table of contents

<!-- markdown-toc:start -->
- [Layout](#layout)
- [One-time setup](#one-time-setup)
  - [1. Clone beside your projects](#1-clone-beside-your-projects)
  - [2. Install Cursor skills](#2-install-cursor-skills)
  - [3. Enable Git hooks in each consumer repo](#3-enable-git-hooks-in-each-consumer-repo)
- [Manual commands](#manual-commands)
- [Environment](#environment)
- [Related repositories](#related-repositories)
<!-- markdown-toc:end -->

Versioned Cursor automation for the Data Engineering workspace: agent rules, skills, Markdown TOC/structure updaters, `prompts.md` generation, and Git pre/post-commit hooks.

Repository: [github.com/basvdberg/cursor-config](https://github.com/basvdberg/cursor-config) (push this folder after clone).

## Layout

| Path | Purpose |
|------|---------|
| `rules/` | Shared Cursor rules (`.mdc`) in category folders (`markdown/`, `operations/`, `security/`, …); single copy only—no per-repo `.cursor/rules` |
| `scripts/` | Python tools and install scripts (`install-cursor.ps1`, `update_markdown_docs.py`, …) |
| `githooks/` | Shared `pre-commit` and `post-commit` hooks for consumer repos |
| `skills/` | Cursor agent skills in category folders (`markdown/`, `basnas/`, `operations/`, …); `install-skills.ps1` junctions leaf folders flat into `~/.cursor/skills/` |
| `browser-bookmarks-sync.json` | Paths to Chrome/Brave profiles and the Floccus Git repo |

Consumer repositories keep repo-specific files only, for example `project-structure-external.json` and `project-structure-descriptions.json` at their own roots.

## One-time setup

### 1. Clone beside your projects

```text
Data Engineering 2.0/
  cursor-config/
  browser-bookmarks-sync/   # private Floccus target (in workspace)
  data-solution-2026/
  data-engineering-2026/
  data-engineering-design-patterns/
```

### 2. Install Cursor skills

From this repository:

```powershell
.\scripts\install-cursor.ps1
```

Links each skill under `%USERPROFILE%\.cursor\skills\` to `skills/` in this repo.

**Rules** stay in `cursor-config/rules/` only. Do not add `.cursor/rules` in consumer repositories. Open the parent workspace (or add the `cursor-config` folder to your Cursor workspace) so agents resolve shared rules from this path.

Re-run after adding a new skill.

### 3. Enable Git hooks in each consumer repo

From the consumer repository root:

```powershell
..\cursor-config\scripts\setup-githooks.ps1 .
```

Or add `.cursor-config.json`:

```json
{
  "cursorConfig": "../cursor-config",
  "preCommit": "standard"
}
```

Use `"preCommit": "strict"` for naming and marker validation (default for `data-engineering-design-patterns`).

## Manual commands

Run from a **consumer** Git root:

```powershell
$cfg = Resolve-Path ..\cursor-config
python "$cfg\scripts\update_markdown_docs.py" --root (Get-Location)
python "$cfg\scripts\update_markdown_docs.py" --toc-only
python "$cfg\scripts\update_prompts.py"   # root prompts.md, or release/details/<version>/ when release/VERSION exists
python "$cfg\scripts\review_markdown.py" .
python "$cfg\scripts\review_markdown.py" . --check-private-urls
```

Audit **cursor-config** itself (rules, skills, private-repo links):

```powershell
python scripts\audit_cursor_config.py   # from cursor-config root
```

Browser bookmarks (Chrome + Brave → Floccus via Git):

```powershell
$env:CURSOR_CONFIG_ROOT = $cfg
python "$cfg\scripts\sync_browser_bookmarks.py" --basnas --commit --push
```

Skill wrappers (after `install-skills.ps1`):

```powershell
python $env:USERPROFILE\.cursor\skills\markdown-toc\scripts\update_toc.py
```

## Environment

| Variable | Purpose |
|----------|---------|
| `CURSOR_CONFIG_ROOT` | Absolute path to this repo when it is not a sibling of the consumer |

Git config `cursor.configPath` is set automatically by `setup-githooks`.

## Related repositories

- [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
- [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
- [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
- [Browser bookmarks sync](skills/sync/browser-bookmarks-sync/SKILL.md) (private; Floccus)

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](readme.md)
  - Doc
    - [Agent smoke tests](doc/agent-smoke-tests.md)
    - [Cursor rules & skills dashboard](doc/cursor-dashboard.md)
  - Githooks
  - Rules
    - Coding Standards
    - Markdown
    - Operations
    - Security
  - Skills
    - Authoring
      - Create Design Pattern
        - [Create design pattern](skills/authoring/create-design-pattern/SKILL.md)
        - [{Title}](skills/authoring/create-design-pattern/TEMPLATE.md)
      - Create Skill
        - [Create skill (cursor-config)](skills/authoring/create-skill/SKILL.md)
      - Create Use Case
        - [Create use case](skills/authoring/create-use-case/SKILL.md)
    - Basnas
      - Basnas Ssh
        - [BasNAS SSH (docker and git)](skills/basnas/basnas-ssh/SKILL.md)
      - Deploy Basnas Container
        - Templates
        - [Fix admin hostname not resolving](skills/basnas/deploy-basnas-container/dns-basnas-setup.md)
        - [Examples](skills/basnas/deploy-basnas-container/examples.md)
        - [NGINX as HTTPS edge on port 443 (local server / QNAP)](skills/basnas/deploy-basnas-container/nginx-on-443.md)
        - [local server deployment reference](skills/basnas/deploy-basnas-container/reference.md)
        - [Deploy container service on local server](skills/basnas/deploy-basnas-container/SKILL.md)
        - [Troubleshooting “Your connection is not private” (*.example)](skills/basnas/deploy-basnas-container/troubleshooting-tls.md)
        - [local server URL map](skills/basnas/deploy-basnas-container/url-map.md)
      - Deploy Data Solution Basnas
        - [Deploy Data Solution 2026 to BasNAS (CI/CD)](skills/basnas/deploy-data-solution-basnas/SKILL.md)
    - Coding Standards
      - Naming Convention Files Folders
        - [Naming convention for files and folders](skills/coding-standards/naming-convention-files-folders/SKILL.md)
      - Pretty Color Logging
        - [Pretty Color Logging](skills/coding-standards/pretty-color-logging/SKILL.md)
      - Variable Naming
        - [Variable naming](skills/coding-standards/variable-naming/SKILL.md)
    - Markdown
      - Markdown Project Structure
        - [Markdown project structure](skills/markdown/markdown-project-structure/SKILL.md)
      - Markdown References
        - [Markdown references](skills/markdown/markdown-references/SKILL.md)
      - Markdown Toc
        - [Markdown table of contents](skills/markdown/markdown-toc/SKILL.md)
      - Review Markdown Structure
        - [Review Markdown structure](skills/markdown/review-markdown-structure/SKILL.md)
    - Operations
      - Release Details Updater
        - [Release Details Updater](skills/operations/release-details-updater/SKILL.md)
      - Release Retrospective
        - [Release retrospective](skills/operations/release-retrospective/SKILL.md)
      - Troubleshooting Error Log
        - [Examples](skills/operations/troubleshooting-error-log/examples.md)
        - [Troubleshooting error reference](skills/operations/troubleshooting-error-log/reference.md)
        - [Troubleshooting error log](skills/operations/troubleshooting-error-log/SKILL.md)
    - Sync
      - Browser Bookmarks Sync
        - [Browser bookmarks sync](skills/sync/browser-bookmarks-sync/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
