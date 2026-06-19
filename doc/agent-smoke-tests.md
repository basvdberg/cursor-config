# Agent smoke tests

## Table of contents

<!-- markdown-toc:start -->
- [How to score](#how-to-score)
- [Test prompts](#test-prompts)
- [Results log](#results-log)
- [After a failed test](#after-a-failed-test)
<!-- markdown-toc:end -->

Quarterly (or per release retro) manual checks that rules and skills produce expected agent behavior. Run each prompt in **Agent mode** with the **Data Engineering 2.0** multi-root workspace open and `cursor-config` included.

## How to score

| Result | Meaning |
|--------|---------|
| **Pass** | Agent follows expected skill/rule without wrong shortcuts |
| **Partial** | Correct outcome but unnecessary steps or missed skill read |
| **Fail** | Wrong procedure (e.g. SSH git pull for routine deploy) |

Log results in the table below. Link failures to ERR entries or retro action items.

## Test prompts

| # | Prompt | Expected skill / rule | Pass criteria |
|---|--------|----------------------|---------------|
| 1 | Deploy my DAG change to BasNAS | `deploy-data-solution-basnas` | Commits and pushes to `main`; does not SSH `git pull` for routine deploy |
| 2 | Fix the markdown TOC in this readme | `markdown-toc-no-title` / `markdown-toc` | TOC has no h1, no self-ref, no `## Project structure` |
| 3 | SSH docker fails on basnas | `basnas-ssh` | Uses plain `ssh bas@basnas 'docker …'`; in data-solution-2026 reads ERR log first |
| 4 | Create a new skill for bookmark icons | `create-skill` | Authors under `cursor-config/skills/`, not `~/.cursor/skills/` directly |
| 5 | Add a link to the browser-bookmarks-sync repo in this doc | `no-private-git-repo-links` | Repo name only; no clickable private GitHub URL |

## Results log

| Date | Tester | 1 | 2 | 3 | 4 | 5 | Notes |
|------|--------|---|---|---|---|---|-------|
| _YYYY-MM-DD_ | | | | | | | Initial baseline after rules/skills audit |

## After a failed test

1. Log ERR in the relevant repo if troubleshooting was involved.
2. Propose rule or skill update in release retro (promotion gate applies).
3. Re-run `python scripts/audit_cursor_config.py` if links or frontmatter were wrong.

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../readme.md)
  - Doc
    - [Agent smoke tests](agent-smoke-tests.md)
    - [Cursor rules & skills dashboard](cursor-dashboard.md)
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
