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
| `bash: <word>: command not found` after `\|` in SSH | `grep -E "a\|b\|c"` lost quotes; `\|` became shell pipes on NAS | Single-quote regex on remote: `grep -E 'a\|b\|c'`; or avoid remote pipe — `docker ps --format` + filter locally | **basnas-ssh** quoting section; promote at release retro |

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
