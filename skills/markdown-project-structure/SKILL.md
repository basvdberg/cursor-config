---
name: markdown-project-structure
description: >-
  Generates a project structure block: full nested site map for the current repo only,
  plus flat GitHub links to repositories discovered from incoming/outgoing markdown
  references. Use for project structure blocks or automatic updates on commit.
---

# Markdown project structure

## Goal

The **Project structure** block has two **top-level** parts (sibling bullets, same depth):

1. **This repository (expanded)** — one top-level bullet for the repo root, then nested folders and in-repo Markdown files.
2. **Related repositories** — a separate **top-level** section (not nested under the repo root). Flat GitHub links only; **do not** expand other repositories.

## Rules — current repository (expanded)

- **Root** — `- [Document title](relative/path/to/readme.md)` from the readme `#` title.
- **Folders** — plain bullet with a section label (e.g. `Definitions`, `Design patterns`).
- **Markdown files** — `- [Title from # heading](relative/path.md)`; paths relative to the file containing the block.
- **Omit** — `prompts.md`, subfolder `readme.md`, `scripts/`, excluded/tooling dirs.
- **Design-patterns layout** — curated map when a top-level `design-patterns/` folder exists.

## Rules — related GitHub repositories (not expanded)

The updater **discovers** related repos automatically:

| Direction | Detection |
|-----------|-----------|
| **Outgoing** | `https://github.com/{owner}/{repo}` in any `.md` file in **this** repository (except `prompts.md`) |
| **Incoming** | Sibling Git repositories under the same parent folder (workspace) whose `.md` files link to **this** repo on GitHub |

- Use the `origin` remote to determine **owner** and **current repo slug**.
- **Related repositories** is its own top-level bullet; each repo is one nested link: `  - [Display name](https://github.com/owner/repo)`.
- Place **Related repositories** after the expanded repo tree (both at top level).
- **Never** use relative paths like `../other-repo/` for cross-repo links (they break on GitHub).
- **Do not** add folder trees or file lists for related repositories.

Optional **`project-structure-external.json`** for display-name overrides only (discovery still drives which repos appear):

```json
{
  "section": "Related repositories",
  "labels": {
    "data-engineering-2026": "Data Engineering 2026"
  },
  "repositories": [
    {
      "label": "Data Engineering Design Patterns",
      "url": "https://github.com/basvdberg/data-engineering-design-patterns"
    }
  ]
}
```

Repos in `repositories` are included only if they are also found by link discovery, except you can use the file to supply labels/URLs for discovered slugs.

## Example

```markdown
- [Data Solution 2026](readme.md)
  - Docs
    - [Markdown automation](docs/markdown-automation.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
```

## Run the updater

```bash
python ../cursor-config/scripts/update_markdown_docs.py --structure-only
python ~/.cursor/skills/markdown-project-structure/scripts/update_structure.py
```

Install skills from [cursor-config](https://github.com/basvdberg/cursor-config) with `scripts/install-skills.ps1`.

## Checklist

- [ ] Only the **current** repo is expanded in the site map
- [ ] `Related repositories` is a **top-level** section (sibling of the repo root, not nested under it)
- [ ] Related repos are **flat GitHub links** under that section
- [ ] Related set matches incoming/outgoing `github.com` references in markdown
- [ ] No `../sibling-repo/` cross-repo paths
- [ ] `markdown-project-structure` markers updated
