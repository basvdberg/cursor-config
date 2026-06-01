# cursor-config

## Table of contents

<!-- markdown-toc:start -->
- [Layout](#layout)
- [One-time setup](#one-time-setup)
  - [1. Clone beside your projects](#1-clone-beside-your-projects)
  - [2. Install skills for Cursor](#2-install-skills-for-cursor)
  - [3. Enable Git hooks in each consumer repo](#3-enable-git-hooks-in-each-consumer-repo)
- [Manual commands](#manual-commands)
- [Environment](#environment)
- [Related repositories](#related-repositories)
<!-- markdown-toc:end -->

Versioned Cursor automation for the Data Engineering workspace: Markdown TOC/structure updaters, `prompts.md` generation, Git pre-commit hooks, and agent skills.

Repository: [github.com/basvdberg/cursor-config](https://github.com/basvdberg/cursor-config) (push this folder after clone).

## Layout

| Path | Purpose |
|------|---------|
| `scripts/` | Python tools (`update_markdown_docs.py`, `update_prompts.py`, `pre_commit.py`, `review_markdown.py`) |
| `githooks/` | Shared `pre-commit` hook used by consumer repos |
| `skills/` | Cursor agent skills (`markdown-toc`, `markdown-project-structure`, `review-markdown-structure`, `deploy-basnas-container`, `browser-bookmarks-sync`, …) |
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

### 2. Install skills for Cursor

```powershell
.\scripts\install-skills.ps1
```

Links each skill under `%USERPROFILE%\.cursor\skills\` to this repository.

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
python "$cfg\scripts\update_prompts.py"
python "$cfg\scripts\review_markdown.py" .
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
- [Browser bookmarks sync](https://github.com/basvdberg/browser-bookmarks-sync) (private; Floccus)

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](readme.md)
  - Githooks
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](skills/browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](skills/create-design-pattern/SKILL.md)
      - [{Title}](skills/create-design-pattern/TEMPLATE.md)
    - Deploy Basnas Container
      - Templates
      - [Fix `admin.basnas` not resolving](skills/deploy-basnas-container/dns-basnas-setup.md)
      - [Examples](skills/deploy-basnas-container/examples.md)
      - [NGINX as HTTPS edge on port 443 (BasNAS / QNAP)](skills/deploy-basnas-container/nginx-on-443.md)
      - [BasNAS deployment reference](skills/deploy-basnas-container/reference.md)
      - [Deploy container service on BasNAS](skills/deploy-basnas-container/SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.basnas)](skills/deploy-basnas-container/troubleshooting-tls.md)
      - [BasNAS URL map](skills/deploy-basnas-container/url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](skills/markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](skills/markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](skills/naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](skills/review-markdown-structure/SKILL.md)
- Related repositories
  - [Browser bookmarks sync](https://github.com/basvdberg/browser-bookmarks-sync)
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
