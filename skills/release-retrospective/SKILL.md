## Table of contents

<!-- markdown-toc:start -->
- [Purpose](#purpose)
- [Artifact layout](#artifact-layout)
- [When to run](#when-to-run)
- [Workflow](#workflow)
- [Chat transcript scan](#chat-transcript-scan)
- [Retrospective output](#retrospective-output)
- [Lessons and categories](#lessons-and-categories)
- [Promotion rules](#promotion-rules)
- [Prompts](#prompts)
<!-- markdown-toc:end -->

---
name: release-retrospective
description: >-
  Drafts per-release sprint retrospectives from ERR entries, incidents, and
  validation results; proposes action items and codification into skills, rules,
  and checklists. Use after a release deploy, when validation fails, or when the
  user asks to run a release retrospective.
---

# Release retrospective

Per-release sprint retrospective (Scrum-style). Agent drafts; user approves promotions and action items.

## Purpose

Close the learning loop: tactical ERR log → significant INC postmortems → per-release retro → permanent guardrails.

## Artifact layout

| Artifact | Path | Role |
|----------|------|------|
| Release notes | `release/YYYY/MM/DD/<version>/notes.md` | Operator-facing changes ([Keep a Changelog](https://keepachangelog.com/)) |
| Release details | `release/YYYY/MM/DD/<version>/readme.md` | Internal audit (metadata, prompts) |
| Retrospective | `release/YYYY/MM/DD/<version>/retrospective.md` | Process review for this release |
| Incidents | `doc/operation/incident/inc-NNN-*.md` | Blameless postmortems |
| Categories | `doc/operation/issue-category.md` | Taxonomy and heat map |
| ERR log | `.cursor/troubleshooting-errors.md` | Session-level failures |

Template: `release/retrospective-template.md`.

## When to run

- After push/deploy and validation attempt (pass or fail)
- When release notes validation checklist has unchecked items
- When user says: "run release retrospective for v…"
- After three or more distinct ERR entries in a release period

## Workflow

1. Read `release/VERSION` or the version the user named.
2. Gather inputs:
   - `release/YYYY/MM/DD/<version>/notes.md` (validation section)
   - `release/YYYY/MM/DD/<version>/readme.md`
   - `.cursor/troubleshooting-errors.md` (entries since previous retro or same date range)
   - `doc/operation/incident/readme.md` and any INC files linked to this release
   - `doc/operation/issue-category.md`
   - Agent transcripts (see [Chat transcript scan](#chat-transcript-scan)) when user supplies a chat ID or retro gaps are likely
3. If transcript or user report reveals failures not in ERR/INC: log ERR first, promote INC when significant, then draft retro.
4. Draft or update `release/YYYY/MM/DD/<version>/retrospective.md` from the template.
5. Update category heat map in `doc/operation/issue-category.md` if patterns are clear.
6. Link retrospective from:
   - `notes.md` → **Related artifacts**
   - `readme.md` → **Linked files**
7. Run [Lessons and categories](#lessons-and-categories) when user asks to enrich lessons or generalize.
8. Present **Promotions** checklist to the user. Do **not** edit skills, rules, or templates until the user approves items.

## Chat transcript scan

Failures fixed only in Cursor chat are invisible to git and an empty ERR log. Scan transcripts when:

- User passes a chat UUID (e.g. `a672de17-cc52-409f-b6a6-b3326360ae3e`)
- User asks why an issue is missing from the retro
- Release validation is unchecked but user reported runtime errors
- Docs-only release but Airflow/deploy issues are plausible

**Transcript location** (workspace project):

```text
%USERPROFILE%\.cursor\projects\<workspace-slug>\agent-transcripts\<chat-uuid>\<chat-uuid>.jsonl
```

**Lookup steps:**

1. If user gives a UUID: search `agent-transcripts` for that string (folder name or file content). Folder name may differ from UI link ID — grep error text (`ModuleNotFoundError`, `dag_run_guard`, etc.) if UUID not found.
2. Read matching `.jsonl`; extract symptom, root cause, fix commands, release version if mentioned.
3. Backfill `.cursor/troubleshooting-errors.md` (ERR-NNN) and `doc/operation/incident/` (INC-NNN) before updating retro.
4. Link source chat in INC and retro **Related artifacts** using `[title](chat-uuid)` (transcript folder UUID).

**Do not** treat “no ERR entries” as “no incidents” without transcript scan when the user references a chat or validation failed.

## Retrospective output

Sections (see template):

- Release context (version, commit, validation outcome)
- What went well / What did not go well
- Incidents table (INC-NNN links)
- Patterns by category (from `issue-category.md`)
- Root causes (generalized, not one-off typos)
- Metrics (ERR count, repeats with Count > 1, incidents, validation)
- Action items (skill / rule / checklist / runbook / lessons-learned)
- Promotions (approval gate checkboxes)

## Lessons and categories

After drafting the retro (or when user says “enrich lessons learned” / “generalize into categories”):

1. Read `doc/operation/issue-category.md` and all INC files linked from the retro.
2. Update **Generalized lessons by category** and **Heat map** in `issue-category.md` if patterns changed.
3. Add or extend narrative sections in `lessons-learned-part2.md` for mature themes (not one-line duplicates of INC text).
4. Add **Lessons promoted** table to `retrospective.md` mapping category → theme → lessons-learned anchor.
5. Cross-cutting themes that span categories go in `issue-category.md` **Cross-cutting themes** table.

**Do not** duplicate every INC into lessons-learned — synthesize patterns (e.g. “two deploy paths”, “chat is not inventory”).

## Promotion rules

| Action type | Destination |
|-------------|-------------|
| Agent behavior | `cursor-config/skills/` or `cursor-config/rules/` |
| Validation step | `release/release-notes-template.md` |
| Infra procedure | `infra/readme.md` |
| Narrative theme | `lessons-learned-part2.md` + `doc/operation/issue-category.md` generalized lessons |
| Cross-project principle | `data-engineering-design-patterns` |

Only implement promotions the user explicitly checks or requests.

## Prompts

| User says | Agent does |
|-----------|------------|
| Run release retrospective for v2026.06.05.6 | Full workflow for that version |
| Why is issue X not in the retro? `<chat-uuid>` | Transcript scan → backfill ERR/INC → update retro |
| Review issue categories | Update heat map from last 3 retrospectives |
| Apply retro action items from v… | Implement only approved items |

## Related skills

- [troubleshooting-error-log](../troubleshooting-error-log/SKILL.md)
- [release-details-updater](../release-details-updater/SKILL.md)
- `deploy-data-solution-basnas` — post-deploy validation and retro trigger
