---
name: create-skill
description: >-
  Creates Cursor Agent Skills in the cursor-config repository (canonical store).
  Use when authoring a new skill, asking about SKILL.md structure, or migrating
  skills from ~/.cursor/skills or consumer .cursor/skills folders.
disable-model-invocation: true
---

# Create skill (cursor-config)

All **shared** Cursor agent skills for this workspace live in the **cursor-config** Git repository — not in `~/.cursor/skills` directly and not in consumer repos under `.cursor/skills/`.

## Canonical location

| What | Path |
|------|------|
| **Author / edit** | `cursor-config/skills/<group>/<skill-name>/SKILL.md` |
| **Runtime (Cursor)** | `%USERPROFILE%\.cursor\skills\<skill-name>\` (junction → cursor-config; flat by skill name) |

Resolve `cursor-config` as:

- Folder `cursor-config/` in the **Data Engineering 2.0** workspace, or
- Clone path the user provides, or
- `$env:CURSOR_CONFIG_ROOT` when set.

**Never:**

- Create or edit skills under `~/.cursor/skills-cursor/` (Cursor-managed built-ins).
- Copy skill source into `~/.cursor/skills/` by hand (that directory is install output only).
- Add `.cursor/skills/` in consumer repos (`data-solution-2026`, etc.) unless the user explicitly wants a **repo-private** skill that must not be shared.

## Directory layout

```text
cursor-config/skills/
├── markdown/                 # category (organizational only)
│   └── markdown-toc/
│       └── SKILL.md
├── basnas/
│   └── deploy-basnas-container/
│       ├── SKILL.md
│       ├── reference.md      # optional
│       └── scripts/          # optional
└── …
```

Category folders group related skills. **Skill identity** is the leaf folder name (`markdown-toc`, `deploy-basnas-container`, …). `install-skills.ps1` discovers `SKILL.md` recursively and junctions each leaf flat into `~/.cursor/skills/<skill-name>/`.

Per-skill layout:

```text
cursor-config/skills/<group>/<skill-name>/
├── SKILL.md              # Required
├── reference.md          # Optional
├── examples.md           # Optional
└── scripts/              # Optional
```

## SKILL.md frontmatter

`SKILL.md` must follow the **Cursor skill convention** — not the content-doc layout (`## Table of contents`, `## Project structure`).

```markdown
---
name: skill-name
description: Third-person WHAT and WHEN (trigger terms for discovery).
disable-model-invocation: true
---

# Skill title

## Instructions
...
```

- **YAML frontmatter first** — file must start with `---` (no TOC or headings before it).
- **No** `markdown-toc` or `markdown-project-structure` blocks on `SKILL.md`.
- Optional supporting files (`reference.md`, `examples.md`) may use a simple `#` title and sections; they are also exempt from content-doc TOC/structure rules.

- `name`: lowercase, hyphens, max 64 chars.
- `description`: third person; include **what** it does and **when** to use it.
- Default `disable-model-invocation: true` so the skill loads when named or referenced; omit only if ambient auto-invoke is intended.

If the user supplies exact wording for the skill body, use it **verbatim** — do not paraphrase.

## Workflow

### 1. Discovery

Gather: purpose, trigger scenarios, supporting files/scripts, and whether the skill is workspace-wide (almost always → cursor-config).

### 2. Implement

1. Create `cursor-config/skills/<group>/<skill-name>/` (pick an existing category folder or add one).
2. Write `SKILL.md` (and optional `reference.md`, `examples.md`, `scripts/`).
3. Keep `SKILL.md` under ~500 lines; link one level deep for extra detail.

### 3. Install

From `cursor-config`:

```powershell
.\scripts\install-skills.ps1
```

This replaces each `%USERPROFILE%\.cursor\skills\<name>` junction with the new skill folder.

### 4. Document

- Update `cursor-config/readme.md` project-structure block (run `update_markdown_docs.py` from a consumer root if TOC/structure markers are used elsewhere).
- Mention the skill in the parent workspace `readme.md` only when it is user-facing.

### 5. Commit

Commit in **cursor-config** (user must ask before `git commit`). Consumer repos should not carry duplicate skill trees.

## Migrate stray skills

When a skill exists outside cursor-config:

| Source | Action |
|--------|--------|
| `~/.cursor/skills/<name>/` (real directory, not junction) | Move files to `cursor-config/skills/<group>/<name>/`, delete the old folder, run `install-skills.ps1` |
| `<consumer>/.cursor/skills/<name>/` | Move to `cursor-config/skills/<group>/<name>/`, delete consumer copy, run `install-skills.ps1` |
| `.cursor/rules/*.mdc` or `.cursor/commands/*.md` | Follow Cursor **migrate-to-skills** into **cursor-config/skills/** (not consumer `.cursor/skills/`) |

Preserve skill body content character-for-character when migrating.

## Quality checklist

- [ ] Stored under `cursor-config/skills/`
- [ ] `SKILL.md` starts with YAML frontmatter (no TOC/structure blocks)
- [ ] `install-skills.ps1` run after add/rename
- [ ] Description includes WHAT + WHEN, third person
- [ ] No Windows backslash paths in skill text
- [ ] No duplicate copy in consumer `.cursor/skills/`

## Related

- Built-in Cursor authoring reference: `~/.cursor/skills-cursor/create-skill/` (read only; do not edit).
- Workspace install: `cursor-config/scripts/install-cursor.ps1`
