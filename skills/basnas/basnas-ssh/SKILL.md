---
name: basnas-ssh
description: >-
  Run docker and git on BasNAS over non-interactive SSH. Use when ssh bas@basnas,
  NAS troubleshooting, docker ps/exec on QNAP, docker or git command not found over SSH,
  quoting or pipe errors over SSH from Windows, or QNAP PATH/sshd setup.
disable-model-invocation: true
---

# BasNAS SSH (docker and git)

**Default for agents:** use plain SSH — no `bash -lc`, no per-command `nas-path.sh` prefix.

```powershell
ssh bas@basnas 'docker ps'
ssh bas@basnas 'docker exec nginx-office-c2h nginx -t'
ssh bas@basnas 'git --version'
```

Connection alias: `bas@basnas` or `$LOCAL_SERVER_SSH` from [local-server.env.example](../deploy-basnas-container/local-server.env.example).

## Quoting and pipes (Windows → SSH)

**Default:** no remote pipes. Run a broad command on the NAS and filter in the agent or locally.

```powershell
ssh bas@basnas 'docker ps --format "{{.Names}}"'
```

Nested quotes across PowerShell → SSH → remote Bash break easily. A failed pattern:

```powershell
# BAD — | in grep pattern becomes shell pipes; bash runs postgres/airflow as commands
ssh bas@basnas 'docker ps --format "{{.Names}}\t{{.Image}}" | grep -E "kafka|postgres|airflow"'
```

Symptom: `bash: postgres: command not found` / `bash: airflow: command not found` — **quoting**, not missing packages.

**If you must grep on the NAS**, single-quote the regex on the remote side:

```powershell
ssh bas@basnas "docker ps --format '{{.Names}}' | grep -E 'kafka|postgres|airflow'"
```

**Prefer Docker filters** over remote `grep`:

```powershell
ssh bas@basnas 'docker ps --format "{{.Names}}\t{{.Image}}" --filter name=kafka --filter name=airflow'
```

(`--filter name=` is substring match; repeat flags for multiple names.)

**Copy-paste — list data-stack containers by name:**

```powershell
ssh bas@basnas 'docker ps --format "{{.Names}}\t{{.Image}}"'
```

Then match `airflow`, `kafka`, `postgres` in the output (container may be named `basnas_postgress`).

## Skill maintenance (not automatic)

Agents improvise SSH quoting, pipes, paths, and env vars every session. Cursor does **not** update this skill from failures by itself.

After deploy or NAS troubleshooting in a release period:

1. Review terminal output and agent transcripts for `ssh bas@basnas` — failed commands, retries, and what finally worked.
2. Log new signatures in `.cursor/troubleshooting-errors.md` (see **troubleshooting-error-log**).
3. At [release retrospective](../../operations/release-retrospective/SKILL.md), add **Promotions** to extend this skill (quoting examples, `$LOCAL_SERVER_SSH`, container names, copy-paste blocks).

Narrative: [lessons-learned-part2 — Local server interaction](https://github.com/basvdberg/data-solution-2026/blob/main/lessons-learned-part2.md#local-server-interaction-learn-from-ssh-commands).

## Forbidden anti-pattern

Do **not** document or default to:

```bash
bash -lc '. /share/homes/bas/.local/bin/nas-path.sh && docker ...'
```

That was a session workaround before the NAS login shell was fixed. Deploy scripts already source [nas-remote-env.sh](https://github.com/basvdberg/data-solution-2026/blob/main/infra/scripts/nas-remote-env.sh).

## One-time NAS setup (QNAP)

Run on the NAS after `git pull` (or from repo path):

```bash
bash ~/apps/data-solution-2026/infra/scripts/setup-nas-ssh-env.sh
```

Then set the login shell (persistent across reboot; verified on BasNAS):

```bash
ssh bas@basnas
sudo cp -p /etc/passwd /etc/passwd.bak.nas-path
sudo sed -i 's#:/bin/sh$#:/share/homes/bas/.local/bin/nas-login-sh#' /etc/passwd
grep '^bas:' /etc/passwd
```

`sudo` asks for the **QTS administrator password** (web UI admin), **not** the `bas` SSH password. QNAP Control Panel → Privilege → Users has **no** custom-shell field.

When `infra/scripts/enable-nas-login-shell.sh` exists in the repo, prefer that script over manual `sed`.

**Verify from Windows:**

```powershell
ssh bas@basnas 'docker -v'
ssh bas@basnas 'command -v docker'   # ~/.local/bin/docker
ssh bas@basnas 'echo PATH=$PATH'     # includes .local/bin and container-station/bin
```

## QNAP quirks (do not rediscover)

| Topic | Fact |
|-------|------|
| Running sshd | `/usr/sbin/sshd -f /etc/config/ssh/sshd_config` — **not** `/etc/ssh/sshd_config` |
| `PermitUserEnvironment` | Manual append to `/etc/config/ssh/sshd_config` is **wiped on reboot**; prefer `nas-login-sh` |
| `ssh admin@basnas` | Usually **Permission denied** — admin SSH is disabled; use QTS web UI + SSH as `bas` |
| `sudo` as `bas` | Prompts for **QTS admin password** |
| SSH restart | Do not run `setsid /etc/init.d/login.sh restart` without **sudo** (segfault risk) |
| Interactive vs one-shot | `ssh bas@basnas` loads `~/.profile`; `ssh bas@basnas 'cmd'` uses login shell from `/etc/passwd` |

## If `docker: command not found`

1. Read [ERR-001](https://github.com/basvdberg/data-solution-2026/blob/main/.cursor/troubleshooting-errors.md) in the workspace.
2. Run `setup-nas-ssh-env.sh` then `enable-nas-login-shell.sh` (or confirm `grep '^bas:' /etc/passwd` ends with `nas-login-sh`).
3. Do **not** run repeated `which docker` / `find` loops in the same session.

## Deploy and troubleshooting

```bash
ssh bas@basnas 'bash ~/apps/data-solution-2026/release/scripts/deploy-on-nas.sh'
```

`deploy-on-nas.sh` sources `nas-remote-env.sh` internally.

## Related skills

- [deploy-basnas-container](../deploy-basnas-container/SKILL.md) — NGINX, TLS, new containers
- [deploy-data-solution-basnas](../deploy-data-solution-basnas/SKILL.md) — CI/CD app deploy (commit and push to `main`)
- [troubleshooting-error-log](../../operations/troubleshooting-error-log/SKILL.md) — ERR log
