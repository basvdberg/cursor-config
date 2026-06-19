---
name: deploy-data-solution-basnas
description: >-
  Deploy data-solution-2026 to BasNAS via CI/CD: commit and push to main; GitHub
  Actions tests and release; post-push hook deploys to NAS after green CI. Use when
  deploying app code, DAGs, poller, extractor, metadata, or docs to BasNAS—not for
  first-time NGINX/Docker host setup (use deploy-basnas-container).
disable-model-invocation: true
---

# Deploy Data Solution 2026 to BasNAS (CI/CD)

**Default for agents:** deploy application changes by **committing and pushing to `main`**. Do **not** SSH to BasNAS to run `git pull` or `deploy-on-nas.sh` for routine releases unless CI/CD failed or the user explicitly asks for a manual deploy.

Repo: [data-solution-2026](https://github.com/basvdberg/data-solution-2026). Full workflow: [CI/CD design](https://github.com/basvdberg/data-solution-2026/blob/main/doc/design/cicd/ci-cd.md).

## Deploy path (normal)

```text
edit → commit → push origin main
  → GitHub Actions: ntfy, tests, GitHub release
  → pre-push hook (this machine, cursor-config/githooks): wait for CI green
  → SSH: bash ~/apps/data-solution-2026/release/scripts/deploy-on-nas.sh
  → ntfy: deploy success or failure
```

What lands on NAS after deploy:

- Latest `main` at `~/apps/data-solution-2026`
- Airflow picks up DAGs from mounted `code/airflow/dags/` (no separate DAG copy)
- Poller/extractor code from mounted `/opt/data-solution` in the Airflow container

## Agent checklist

When the user wants changes on BasNAS (or you finished implementation they will run in production):

1. **Finish the change** in `data-solution-2026/` (code, `infra/`, docs).
2. **Commit and push** to `origin main` yourself—do not ask the user to deploy, commit, or push unless they explicitly want to do that step.
3. **Do not** run NAS deploy commands yourself unless troubleshooting or CI/CD failed.
4. **Do not** end with “deploy manually” or “SSH and git pull”—CI/CD and the post-push hook handle routine releases.
5. Tell the user only to watch **ntfy** topic `data-solution-2026-deploy` (or GitHub Actions) for CI and deploy status.
6. **Do not commit** when the user only asked a question with no deploy intent; **do commit** when they want something on BasNAS or you completed a feature they are shipping.
7. **After deploy** (when validation is in scope): read `.cursor/troubleshooting-errors.md`; on validation failure log ERR and promote to `doc/operation/incident/` if significant; draft `release/YYYY/MM/DD/<version>/retrospective.md` per `release-retrospective` skill and present promotion checklist for user approval.

Skip release bump for docs-only commits when appropriate:

```powershell
$env:SKIP_RELEASE = "1"
git commit -m "chore: docs only"
```

## One-time setup (developer machine)

Verify deploy hook once from the **data-solution-2026** repo root (uses `cursor-config/githooks/pre-push`, not `.git/hooks/post-push`):

```powershell
powershell -ExecutionPolicy Bypass -File .\release\scripts\install-post-push-hook.ps1
```

Requires:

- `gh auth login` (CI status polling)
- `ssh bas@basnas` working from this machine (`ssh bas@basnas 'docker -v'` — see **basnas-ssh** skill)
- ntfy subscription: `https://ntfy.sh/data-solution-2026-deploy`

Hook config: `release/scripts/post-push-hook.ps1` (NAS SSH command).

## When infra compose files change

Pre-commit updates `release/deploy-config.json` (`sync_infra: true`) when meaningful runtime files under `infra/` change since the last release tag (compose, `.env.example`, deploy scripts — not readme-only).

`deploy-on-nas.sh` reads that flag after `git pull` and runs `deploy-infra-on-nas.sh` automatically. **No extra SSH step for routine releases.**

Force infra sync (override or when config is stale):

```bash
RUN_INFRA_SYNC=1 bash ~/apps/data-solution-2026/release/scripts/deploy-on-nas.sh
```

First-time stack setup (`.env`, Postgres app user, Airflow variables) is **not** part of CI/CD—see [implementation plan prerequisites](https://github.com/basvdberg/data-solution-2026/blob/main/doc/implementation-plan.md#prerequisites).

## Manual / emergency deploy

Use only when CI/CD or the post-push hook is broken:

```bash
ssh bas@basnas 'bash ~/apps/data-solution-2026/release/scripts/deploy-on-nas.sh'
```

Rollback: checkout a previous tag on NAS ([CI/CD rollback](https://github.com/basvdberg/data-solution-2026/blob/main/doc/design/cicd/ci-cd.md#rollback)).

## Related skills

- [basnas-ssh](../basnas-ssh/SKILL.md) — plain SSH docker/git on QNAP (install via `cursor-config/scripts/install-cursor.ps1`)
- [deploy-basnas-container](../deploy-basnas-container/SKILL.md) — NGINX, TLS, new containers, port registry (host/infrastructure, not app git deploy)
- [troubleshooting-error-log](../../operations/troubleshooting-error-log/SKILL.md) — ERR log during deploy/validation failures
- [release-retrospective](../../operations/release-retrospective/SKILL.md) — per-release retrospective after validation
