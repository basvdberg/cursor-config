# Examples

## Example log entry (append to `.cursor/troubleshooting-errors.md`)

```markdown
### ERR-003 — docker not on PATH (SSH basnas)

| Field | Value |
|-------|-------|
| **When** | 2026-06-03T10:15:00 |
| **Context** | SSH bas@basnas, non-interactive session |
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
