---
name: basnas-ssh
description: >-
  Run docker and git on BasNAS over non-interactive SSH. Use when ssh bas@basnas,
  NAS troubleshooting, docker ps/exec on QNAP, docker or git command not found over SSH,
  or QNAP PATH/sshd setup.
---

# BasNAS SSH (docker and git)

**Default for agents:** use plain SSH — no `bash -lc`, no per-command `nas-path.sh` prefix.

```powershell
ssh bas@basnas 'docker ps'
ssh bas@basnas 'docker exec nginx-office-c2h nginx -t'
ssh bas@basnas 'git --version'
```

Connection alias: `bas@basnas` or `$LOCAL_SERVER_SSH` from [local-server.env.example](../deploy-basnas-container/local-server.env.example).

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
- [deploy-data-solution-basnas](https://github.com/basvdberg/cursor-config/blob/main/skills/deploy-data-solution-basnas/SKILL.md) — CI/CD app deploy (if installed under `~/.cursor/skills/`)
- [troubleshooting-error-log](../troubleshooting-error-log/SKILL.md) — ERR log
