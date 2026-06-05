# Examples

## Table of contents

<!-- markdown-toc:start -->
- [Example log entry (append to .cursor/troubleshooting-errors.md)](#example-log-entry-append-to-cursortroubleshooting-errorsmd)
- [Example review output (user: "review troubleshooting errors")](#example-review-output-user-review-troubleshooting-errors)
<!-- markdown-toc:end -->

## Example log entry (append to `.cursor/troubleshooting-errors.md`)

```markdown
### ERR-003 — docker not on PATH (SSH basnas)

| Field | Value |
|-------|-------|
| **When** | 2026-06-03T10:15:00 |
| **Context** | SSH $LOCAL_SERVER_SSH, non-interactive session |
| **Command** | `docker ps` |
| **Error** | bash: docker: command not found (127) |
| **Description** | Container Station `docker` is not on default PATH. |
| **Solution** | `source /share/.../data-solution-2026/infra/scripts/nas-remote-env.sh` then retry. |
| **Prevention** | Source `nas-remote-env.sh` once at session start before any docker/git commands. |
| **Count** | 1 |
```

If the agent runs `which docker` again without sourcing:

- Do **not** add ERR-004.
- Update **Count** to `2` on ERR-003 and apply **Solution** immediately.

## Example review output (user: "review troubleshooting errors")

```markdown
# Troubleshooting error review — data-solution-2026 (2026-06-03)

## Summary
- Total entries: 4 | Unique signatures: 3 | Repeated mistakes: 1 (ERR-003 Count=2)

## Error list

| ID | Title | Description | Solution | Count |
|----|-------|-------------|----------|-------|
| ERR-001 | compose path wrong on NAS | Deploy script run from home, not clone root | `cd` to git checkout; use `release/scripts/deploy-on-nas.sh` | 1 |
| ERR-002 | Airflow UI log 404 after reboot | Worker URL still old IP | Re-verify compose hostname settings; full reboot test | 1 |
| ERR-003 | docker not on PATH (SSH) | Non-interactive SSH PATH | Source `nas-remote-env.sh` once | 2 |

## Efficiency recommendations
1. Open NAS SSH with env script in the first command block of every infra task.
2. Treat "works once in browser" as insufficient — schedule reboot verification for infra PRs.

## Patterns to codify
- Mention `troubleshooting-error-log` + `deploy-basnas-container` in same session for NAS work.
```

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
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Pretty Color Logging
      - [Pretty Color Logging](../pretty-color-logging/SKILL.md)
    - Release Details Updater
      - [Release Details Updater](../release-details-updater/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
    - Troubleshooting Error Log
      - [Examples](examples.md)
      - [Troubleshooting error reference](reference.md)
      - [Troubleshooting error log](SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
