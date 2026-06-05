## Table of contents

<!-- markdown-toc:start -->
- [Log location](#log-location)
- [When to log](#when-to-log)
- [Entry format](#entry-format)
- [Agent rules during troubleshooting](#agent-rules-during-troubleshooting)
- [Review workflow](#review-workflow)
- [Bootstrap](#bootstrap)
- [Additional resources](#additional-resources)
<!-- markdown-toc:end -->

## Table of contents


---
name: troubleshooting-error-log
description: >-
  Records shell, SSH, Docker, and script failures during agent troubleshooting
  with short descriptions and solutions; deduplicates repeat errors; produces
  review summaries. Use when commands fail, debugging infra, SSH to NAS/QNAP,
  docker not found, missing scripts, permission errors, or when the user asks
  to review troubleshooting errors or improve agent efficiency.
---

# Troubleshooting error log

Keep a durable, reviewable record of every failure encountered while fixing a problem — not only the final fix.

## Log location

Use the **workspace root** log file:

```text
.cursor/troubleshooting-errors.md
```

- Create `.cursor/` if missing.
- If the user names a different path, use that path for the rest of the session.
- One file per project; do not scatter entries across chat only.

## When to log

Append an entry **immediately** after any of these:

| Trigger | Examples |
|---------|----------|
| Non-zero exit | `docker compose up` failed, `git pull` rejected |
| Command not found | `docker`, `git`, `gh`, script path wrong |
| Permission denied | cannot write mount, SSH key, sudo |
| Wrong environment | tool works locally but not over SSH; Windows vs Linux path |
| Missing file | script, `.env`, compose file, DAG path assumed but absent |
| Transient infra | UI errors after reboot; port/hostname mismatch |
| Repeated workaround | same `which` / `find` / PATH fix run twice in one session |

**Before retrying:** read the log. If the same error signature exists, apply the documented **Solution** — do not rediscover it.

## Entry format

Append under `## Session: <YYYY-MM-DD>` (create the heading if needed). Newest entries at the **bottom** of that section.

```markdown
### ERR-<NNN> — <short title>

| Field | Value |
|-------|-------|
| **When** | <ISO-8601 local or UTC> |
| **Context** | e.g. SSH local server, PowerShell local, CI |
| **Command** | exact command or script invoked |
| **Error** | stderr / exit code / one-line symptom |
| **Description** | What went wrong in plain language (1–2 sentences) |
| **Solution** | What fixed it or what to do next time (actionable) |
| **Prevention** | How the agent should avoid this next time |
| **Count** | 1 (increment if same signature recurs; do not add duplicate rows) |

```

**Error signature** (for dedup): normalize `Command` + core message (strip timestamps, PIDs, random ports).

**Numbering:** `ERR-001`, `ERR-002`, … monotonic within the file.

## Agent rules during troubleshooting

1. **Log first, then fix** — one line in chat is not enough; write the table row.
2. **Persist environment fixes once** — after first `command not found` for a recurring tool (e.g. `docker` on NAS SSH), source env or export `PATH` for the **rest of the session**; log `Prevention` accordingly.
3. **Verify before run** — `test -f`, `test -x`, or `Get-Command` / `where.exe` for scripts and CLIs you depend on; log a single entry if missing instead of trial-and-error loops.
4. **No silent repeats** — if `Count` > 1, stop and apply **Solution**; tell the user the agent repeated a known mistake.
5. **End of task** — if three or more distinct errors occurred, offer a one-paragraph session summary and point to the log path.

## Review workflow

When the user asks to **review errors**, **list failures**, or **improve agent efficiency**:

1. Read `.cursor/troubleshooting-errors.md` (or the path they gave).
2. Output a **Review summary** in this shape:

```markdown
# Troubleshooting error review — <project or date>

## Summary
- Total entries: N | Unique signatures: M | Repeated mistakes: K (Count > 1)

## Error list

| ID | Title | Description | Solution | Count |
|----|-------|-------------|----------|-------|
| ERR-001 | … | … | … | 1 |

## Efficiency recommendations
1. … (concrete agent behavior change)
2. …

## Patterns to codify
- Skill/rule/script changes worth making permanent
```

3. Propose **Prevention** updates for top repeated errors (skills, `nas-remote-env.sh`, compose pins, etc.) only when grounded in the log.

## Bootstrap

If the log file does not exist, create it with:

```markdown
# Troubleshooting errors

Agent-maintained log of failures during debugging. Do not edit by hand unless correcting facts.

## Session: <today>
```

## Additional resources

- Common signatures and NAS/SSH patterns: [reference.md](reference.md)
- Example review output: [examples.md](examples.md)

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
