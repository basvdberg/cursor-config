# Cursor rules & skills dashboard

Generated: 2026-06-19. Re-run: `python scripts/generate_cursor_dashboard.py` from cursor-config.

## Inventory matrix

Counts of `.mdc` rules and `SKILL.md` skills. **Merged (effective custom)** = cursor-config plus non-junction entries under `%USERPROFILE%\.cursor\skills` and `rules` (if any).

| Location | Rules | Skills | Notes |
|----------|------:|-------:|-------|
| workspace / cursor-config | 4 | 15 | — |
| workspace / browser-bookmarks-sync | 0 | 0 | — |
| workspace / data-solution-2026 | 0 | 0 | .cursor/troubleshooting-errors.md (ERR log artifact, not a rule) |
| workspace / data-engineering-2026 | 0 | 0 | — |
| workspace / data-engineering-design-patterns | 0 | 0 | — |
| workspace / adl-feedback | 0 | 0 | — |
| **cursor-config** (canonical) | **4** | **15** | Shared rules + skills source of truth |
| user home `~/.cursor/skills` | — | 14 junctions + 0 real | All 14 installed skills are junctions → cursor-config |
| user home `~/.cursor/skills-cursor` | — | 18 | Cursor-managed built-ins (not merged) |
| user home `~/.cursor/rules` | 0 | — | directory absent |
| **Merged effective custom** | **4** | **15** | cursor-config + non-symlink user-home skills/rules |
| **Total available to agent** | **4** | **33** | custom + Cursor built-in skills |

### Symlink policy

- `install-cursor.ps1` junctions `~/.cursor/skills/<name>` → `cursor-config/skills/<group>/<name>/` (flat by skill name).
- Rules are **not** junctioned; they load when `cursor-config` is in the workspace.
- Non-junction user-home skills: **0** (should be migrated into cursor-config per `create-skill`).

## Scoring legend

Score 1–10 for **compactness + effectiveness** (higher is better).

| Factor | Effect |
|--------|--------|
| Missing frontmatter or description | −2 to −3 |
| Ambiguous or short description (weak WHEN triggers) | −1 |
| Skill >250 lines (verbose) or >500 lines | −0.5 to −3 |
| Rule >50 lines | −1 (prefer skill) |
| TOC before YAML frontmatter | −1 |
| Broken relative links | −2 |

Audit: `python scripts/audit_cursor_config.py` (cursor-config skills/rules).

## Rules (cursor-config)

### markdown & documentation

| Rule | Score | Lines | Summary | Issues |
|------|------:|------:|---------|--------|
| [markdown-folder-kebab-case](rules/markdown/markdown-folder-kebab-case.mdc) | 10.0 | 41 | Enforce kebab-case naming for markdown files and folders | — |
| [markdown-toc-no-title](rules/markdown/markdown-toc-no-title.mdc) | 8.0 | 52 | TOC generation rules for markdown files | short description; weak WHEN triggers; rule >50 lines; consider a skill |

### operations & release

| Rule | Score | Lines | Summary | Issues |
|------|------:|------:|---------|--------|
| [issue-inventory](rules/operations/issue-inventory.mdc) | 10.0 | 35 | Issue inventory — ERR log, incident promotion, per-release retrospectives (data-solution-2026) | — |

### security & policy

| Rule | Score | Lines | Summary | Issues |
|------|------:|------:|---------|--------|
| [no-private-git-repo-links](rules/security/no-private-git-repo-links.mdc) | 10.0 | 40 | Do not link to private Git repositories in docs or agent output | — |

## Skills

### markdown & documentation

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [markdown-project-structure](skills/markdown/markdown-project-structure/SKILL.md) | cursor-config | 10.0 | 122 | Generates a project structure block: full nested site map for the current repo only, plus related public repositories di… | — |
| [markdown-toc](skills/markdown/markdown-toc/SKILL.md) | cursor-config | 10.0 | 90 | Generates and refreshes Markdown table-of-contents blocks from ##–###### headings only. Never includes the document # ti… | — |
| [review-markdown-structure](skills/markdown/review-markdown-structure/SKILL.md) | cursor-config | 10.0 | 156 | Reviews and authors Markdown for spelling, kebab-case naming, heading hierarchy, orphan paragraphs, required TOC/project… | — |

### authoring & templates

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [create-design-pattern](skills/authoring/create-design-pattern/SKILL.md) | cursor-config | 10.0 | 65 | Creates compact, technology-agnostic design pattern markdown in data-engineering-design-patterns/design-patterns/. Use w… | — |
| [create-skill](skills/authoring/create-skill/SKILL.md) | cursor-config | 9.0 | 142 | Creates Cursor Agent Skills in the cursor-config repository (canonical store). Use when authoring a new skill, asking ab… | TOC before frontmatter (move YAML to line 1) |

### BasNAS & deployment

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [basnas-ssh](skills/basnas/basnas-ssh/SKILL.md) | cursor-config | 10.0 | 141 | Run docker and git on BasNAS over non-interactive SSH. Use when ssh bas@basnas, NAS troubleshooting, docker ps/exec on Q… | — |
| [deploy-basnas-container](skills/basnas/deploy-basnas-container/SKILL.md) | cursor-config | 10.0 | 134 | Design and deploy Docker services on local server with fixed host ports, NGINX HTTPS termination, dual DNS (office.c2h.n… | — |
| [deploy-data-solution-basnas](skills/basnas/deploy-data-solution-basnas/SKILL.md) | cursor-config | 10.0 | 97 | Deploy data-solution-2026 to BasNAS via CI/CD: commit and push to main; GitHub Actions tests and release; post-push hook… | — |

### operations & release

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [release-details-updater](skills/operations/release-details-updater/SKILL.md) | cursor-config | 10.0 | 66 | Maintain release/YYYY/MM/DD/<version>/ metadata and prompts per release. Use when creating releases, updating release no… | — |
| [release-retrospective](skills/operations/release-retrospective/SKILL.md) | cursor-config | 10.0 | 153 | Drafts per-release sprint retrospectives from ERR entries, incidents, and validation results; proposes action items and … | — |
| [troubleshooting-error-log](skills/operations/troubleshooting-error-log/SKILL.md) | cursor-config | 10.0 | 149 | Records shell, SSH, Docker, and script failures during agent troubleshooting with short descriptions and solutions; dedu… | — |

### bookmarks & sync

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [browser-bookmarks-sync](skills/sync/browser-bookmarks-sync/SKILL.md) | cursor-config | 10.0 | 96 | Merge Chrome and Brave bookmarks, inject local server service URLs from service-url-map.yaml, and commit to the private … | — |

### coding standards

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| [naming-convention-files-folders](skills/coding-standards/naming-convention-files-folders/SKILL.md) | cursor-config | 10.0 | 99 | Names files and folders using common GitHub conventions plus singular, short, non-conjugated names. Use when creating or… | — |
| [pretty-color-logging](skills/coding-standards/pretty-color-logging/SKILL.md) | cursor-config | 10.0 | 56 | Standardize Python CLI logging with readable, colorized, structured output. Use when adding or improving logs for script… | — |
| [variable-naming](skills/coding-standards/variable-naming/SKILL.md) | cursor-config | 10.0 | 140 | Names variables, environment keys, and config settings after the semantics of their value, not the component or feature … | — |

### authoring & migration (Cursor built-in)

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| `create-hook` (`~/.cursor/skills-cursor/create-hook/`) | skills-cursor | 9.5 | 239 | Create Cursor hooks. Use when you want to create a hook, write hooks.json, add hook scripts, or automate behavior around… | — |
| `create-rule` (`~/.cursor/skills-cursor/create-rule/`) | skills-cursor | 10.0 | 164 | Create Cursor rules for persistent AI guidance. Use when you want to create a rule, add coding standards, set up project… | — |
| `create-skill` (`~/.cursor/skills-cursor/create-skill/`) | skills-cursor | 6.0 | 504 | Create Cursor Agent Skills. Use when authoring a new skill or asking about SKILL.md structure. | WARN: 504 lines (>500); 504 lines (>500 guideline); overlaps cursor-config `create-skill` (different scope) |
| `create-subagent` (`~/.cursor/skills-cursor/create-subagent/`) | skills-cursor | 9.5 | 225 | Create custom subagents for specialized AI tasks. Use when you want to create a new type of subagent, set up task-specif… | — |
| `migrate-to-skills` (`~/.cursor/skills-cursor/migrate-to-skills/`) | skills-cursor | 10.0 | 134 | Convert 'Applied intelligently' Cursor rules (.cursor/rules/*.mdc) and slash commands (.cursor/commands/*.md) to Agent S… | — |

### code review (Cursor built-in)

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| `review` (`~/.cursor/skills-cursor/review/`) | skills-cursor | 10.0 | 16 | Review code changes with the Bugbot or Security Review subagent. | — |
| `review-bugbot` (`~/.cursor/skills-cursor/review-bugbot/`) | skills-cursor | 9.0 | 67 | Review code changes with Bugbot subagent. | short description; weak WHEN triggers |
| `review-security` (`~/.cursor/skills-cursor/review-security/`) | skills-cursor | 10.0 | 52 | Review code changes with Security Review subagent. | — |

### automation & workflow (Cursor built-in)

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| `automate` (`~/.cursor/skills-cursor/automate/`) | skills-cursor | 7.5 | 377 | Use this skill to create Cursor Automations. | short description; weak WHEN triggers; 377 lines (verbose) |
| `babysit` (`~/.cursor/skills-cursor/babysit/`) | skills-cursor | 10.0 | 14 | Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI in a loop. | — |
| `loop` (`~/.cursor/skills-cursor/loop/`) | skills-cursor | 10.0 | 73 | Run a prompt or skill in this session on a recurring or variable interval (e.g. /loop 5m /foo). | — |
| `shell` (`~/.cursor/skills-cursor/shell/`) | skills-cursor | 10.0 | 24 | Runs the rest of a /shell request as a literal shell command. Use only when the user explicitly invokes /shell and wants… | — |
| `split-to-prs` (`~/.cursor/skills-cursor/split-to-prs/`) | skills-cursor | 10.0 | 49 | Split current work into small reviewable PRs. Use when the user asks to split a chat, set of changes, branch, or PR. | — |

### canvas & SDK (Cursor built-in)

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| `canvas` (`~/.cursor/skills-cursor/canvas/`) | skills-cursor | 8.0 | 108 | A Cursor Canvas is a live React app that the user can open beside the chat. You MUST use a canvas when the agent produce… | broken link: `/Users/<user>/.cursor/projects/<workspace>/canvases/billing-review.canvas.tsx` |
| `sdk` (`~/.cursor/skills-cursor/sdk/`) | skills-cursor | 8.5 | 380 | Guide users building apps, scripts, CI pipelines, or automations on top of the Cursor SDK - TypeScript (`@cursor/sdk`) o… | 380 lines (verbose) |

### IDE & CLI config (Cursor built-in)

| Skill | Source | Score | Lines | Summary | Issues |
|-------|--------|------:|------:|---------|--------|
| `statusline` (`~/.cursor/skills-cursor/statusline/`) | skills-cursor | 10.0 | 196 | Configure a custom status line in the CLI. Use when the user mentions status line, statusline, statusLine, CLI status ba… | — |
| `update-cli-config` (`~/.cursor/skills-cursor/update-cli-config/`) | skills-cursor | 10.0 | 87 | View and modify Cursor CLI configuration settings in ~/.cursor/cli-config.json. Use when the user wants to change CLI se… | — |
| `update-cursor-settings` (`~/.cursor/skills-cursor/update-cursor-settings/`) | skills-cursor | 10.0 | 122 | Modify Cursor/VSCode user settings in settings.json. Use when you want to change editor settings, preferences, configura… | — |

## Cross-cutting findings

### Duplicate / overlapping names

| Name | Locations | Recommendation |
|------|-----------|----------------|
| `create-skill` | cursor-config (workspace canonical) + skills-cursor (generic Cursor template) | Use cursor-config skill for shared workspace skills; built-in for global Cursor authoring. |
| `review` vs `review-bugbot` / `review-security` | skills-cursor | `review` is a router; prefer specific review skills when intent is known. |

### Policy alignment

- Consumer repos have **no** `.cursor/rules` or `.cursor/skills` — aligned with cursor-config readme.
- `data-solution-2026/.cursor/troubleshooting-errors.md` is an ERR log artifact referenced by `issue-inventory` rule, not a Cursor rule file.
- `issue-inventory` glob `data-solution-2026/**` requires multi-root workspace with cursor-config present.

### Skills with TOC before frontmatter

Several cursor-config skills place the generated TOC above YAML frontmatter (valid for docs, non-standard for skill discovery). Consider moving frontmatter to line 1 per `create-skill` template.

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../readme.md)
  - Doc
    - [Agent smoke tests](agent-smoke-tests.md)
    - [Cursor rules & skills dashboard](cursor-dashboard.md)
  - Githooks
  - Rules
    - Coding Standards
    - Markdown
    - Operations
    - Security
  - Skills
    - Authoring
      - Create Design Pattern
        - [Create design pattern](../skills/authoring/create-design-pattern/SKILL.md)
        - [{Title}](../skills/authoring/create-design-pattern/TEMPLATE.md)
      - Create Skill
        - [Create skill (cursor-config)](../skills/authoring/create-skill/SKILL.md)
      - Create Use Case
        - [Create use case](../skills/authoring/create-use-case/SKILL.md)
    - Basnas
      - Basnas Ssh
        - [BasNAS SSH (docker and git)](../skills/basnas/basnas-ssh/SKILL.md)
      - Deploy Basnas Container
        - Templates
        - [Fix admin hostname not resolving](../skills/basnas/deploy-basnas-container/dns-basnas-setup.md)
        - [Examples](../skills/basnas/deploy-basnas-container/examples.md)
        - [NGINX as HTTPS edge on port 443 (local server / QNAP)](../skills/basnas/deploy-basnas-container/nginx-on-443.md)
        - [local server deployment reference](../skills/basnas/deploy-basnas-container/reference.md)
        - [Deploy container service on local server](../skills/basnas/deploy-basnas-container/SKILL.md)
        - [Troubleshooting “Your connection is not private” (*.example)](../skills/basnas/deploy-basnas-container/troubleshooting-tls.md)
        - [local server URL map](../skills/basnas/deploy-basnas-container/url-map.md)
      - Deploy Data Solution Basnas
        - [Deploy Data Solution 2026 to BasNAS (CI/CD)](../skills/basnas/deploy-data-solution-basnas/SKILL.md)
    - Coding Standards
      - Naming Convention Files Folders
        - [Naming convention for files and folders](../skills/coding-standards/naming-convention-files-folders/SKILL.md)
      - Pretty Color Logging
        - [Pretty Color Logging](../skills/coding-standards/pretty-color-logging/SKILL.md)
      - Variable Naming
        - [Variable naming](../skills/coding-standards/variable-naming/SKILL.md)
    - Markdown
      - Markdown Project Structure
        - [Markdown project structure](../skills/markdown/markdown-project-structure/SKILL.md)
      - Markdown References
        - [Markdown references](../skills/markdown/markdown-references/SKILL.md)
      - Markdown Toc
        - [Markdown table of contents](../skills/markdown/markdown-toc/SKILL.md)
      - Review Markdown Structure
        - [Review Markdown structure](../skills/markdown/review-markdown-structure/SKILL.md)
    - Operations
      - Release Details Updater
        - [Release Details Updater](../skills/operations/release-details-updater/SKILL.md)
      - Release Retrospective
        - [Release retrospective](../skills/operations/release-retrospective/SKILL.md)
      - Troubleshooting Error Log
        - [Examples](../skills/operations/troubleshooting-error-log/examples.md)
        - [Troubleshooting error reference](../skills/operations/troubleshooting-error-log/reference.md)
        - [Troubleshooting error log](../skills/operations/troubleshooting-error-log/SKILL.md)
    - Sync
      - Browser Bookmarks Sync
        - [Browser bookmarks sync](../skills/sync/browser-bookmarks-sync/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
