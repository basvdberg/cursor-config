# Troubleshooting error reference

## Table of contents

<!-- markdown-toc:start -->
- [SSH / remote shell](#ssh-remote-shell)
- [Docker / containers](#docker-containers)
- [Scripts and paths](#scripts-and-paths)
- [Git / CI / deploy](#git-ci-deploy)
- [Agent efficiency anti-patterns](#agent-efficiency-anti-patterns)
- [Linking to project docs](#linking-to-project-docs)
<!-- markdown-toc:end -->

Catalog of frequent signatures. Match log entries to these; extend the catalog when a new class appears twice.

## SSH / remote shell

| Signature | Description | Solution | Prevention |
|-----------|-------------|----------|------------|
| `docker: command not found` (SSH) | Non-interactive `sshd` uses `/bin/sh` + minimal `PATH`; `~/.profile` not loaded | `setup-nas-ssh-env.sh` + set `bas` shell to `nas-login-sh` in `/etc/passwd` (see **basnas-ssh** skill) | Plain `ssh bas@basnas 'docker …'` after one-time setup; no per-command `bash -lc` |
| `git: command not found` (SSH QNAP) | QGit not on default PATH / libcharset | `setup-nas-ssh-env.sh` git wrapper + same login shell fix | Same as docker |
| Wrong host shell | Commands for bash run in PowerShell SSH or vice versa | Use host-appropriate syntax; open correct shell | Read terminal metadata (`cwd`, shell) before commands |
| Interactive-only setup | Fix works in manual SSH but not agent SSH | Put exports in script sourced by automation, not only `.bashrc` interactive | Prefer `nas-remote-env.sh` over ad hoc `export` |

## Docker / containers

| Signature | Description | Solution | Prevention |
|-----------|-------------|----------|------------|
| `docker` without env on NAS | Agent rediscovers path via `find`/`which` each failure | One-time PATH fix; log `Count` if repeated | Never repeat lookup in same session |
| Random admin password after restart | Compose regenerates creds on recreate | Pin password in compose/env; document in infra | Require reboot test in infra changes |
| UI/log URL errors after reboot | Hostname, published ports, or worker URLs drift | Pin `hostname`, network, `AIRFLOW__CORE__HOSTNAME_CALLABLE`, fixed ports | Verify `down` → reboot → browse cycle |
| Compose file not found | Wrong directory on remote | `cd` to known deploy root; verify with `ls` | Read deploy docs/skills for layout first |

## Scripts and paths

| Signature | Description | Solution | Prevention |
|-----------|-------------|----------|------------|
| `No such file or directory` (script) | Path assumed from docs or wrong OS separators | Use repo-relative path; `test -f` before run | Glob or read file tree before invoking |
| `cannot execute: required file not found` | Windows CRLF on shell script | `dos2unix` or fix `.gitattributes` | Check `file` / `git attributes` for `*.sh` |
| Permission denied (script) | Missing `chmod +x` on NAS | `chmod +x` once; log it | Check `-x` before first run |

## Git / CI / deploy

| Signature | Description | Solution | Prevention |
|-----------|-------------|----------|------------|
| `gh: command not found` | GitHub CLI not installed on current machine | Use `git` API or install `gh`; or run from machine that has it | Check tool availability before PR/release ops |
| Hook / script path (Windows) | PowerShell vs bash hook location | Use documented hook from `release/scripts/` | Match OS in getting-started |

## Agent efficiency anti-patterns

Log these explicitly when observed:

| Anti-pattern | Prevention |
|--------------|------------|
| Same `which`/`find` after PATH fix | Increment `Count`; apply logged **Solution** |
| Fix UI symptom without reboot test | Add **Prevention**: full stop → reboot → verify |
| Infra change without documented decision | Log + suggest architecture note before apply |

## Linking to project docs

When errors relate to a known project lesson, cross-reference in **Description** (e.g. `lessons-learned-part2.md` § Remote SSH) — do not duplicate long prose in the log.

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
