---
name: release-details-updater
description: Maintain release/YYYY/MM/DD/<version>/ metadata and prompts per release. Use when creating releases, updating release notes, or when the user asks to keep release details synchronized on each commit.
disable-model-invocation: true
---

# Release Details Updater

## Purpose

Keep `release/YYYY/MM/DD/<version>/` complete and consistent with `release/VERSION`, release notes, and commit history.

## Required outputs per release

For each release version folder (`release/YYYY/MM/DD/<version>/`):

| File | Required | When created |
|------|----------|--------------|
| `notes.md` | Yes | Minimal stub at open release; fill before publish |
| `readme.md` | No | `update-release-details.ps1` on first refresh |
| `prompts.md` | No | `update_prompts.py` when transcript sessions exist |
| `retrospective.md` | No | [release-retrospective](../release-retrospective/SKILL.md) on demand |

Also maintain:

- `release/readme.md` release index table.
- Cross-links in `notes.md` → **Related artifacts** (readme, retrospective, incidents).

## Workflow

1. Read `release/VERSION`.
2. Ensure `release/YYYY/MM/DD/<version>/` exists.
3. Update `readme.md` with:
   - start and end development date/time
   - release commit/tag info
   - sequential summary of changes
4. Update `prompts.md` with all prompts used in that release.
5. Ensure `readme.md` **Linked files** includes retrospective and incident register.
6. Keep `release/readme.md` index in sync with ordered release history.
7. After validation, run or offer [release-retrospective](../release-retrospective/SKILL.md) for that version.

## Commit-time automation

Shared Git hooks from [cursor-config](https://github.com/basvdberg/cursor-config) (`core.hooksPath`):

**Pre-commit** (`pre_commit.py`):

- `ensure-open-release.ps1` — ensures minimal `notes.md` for the open `release/VERSION` (on `main`, unless `SKIP_RELEASE=1` or only metadata files are staged)
- `new-release.ps1` — only when `NEW_RELEASE=1` (force next version)
- `update_prompts.py` — writes `prompts.md` when sessions exist (header-only stubs are overwritten)
- `update-release-details.ps1` — bootstraps missing `readme.md`

**Post-commit** (`post_commit.py` + `release/scripts/post-commit-hook.ps1`):

- `update_prompts.py` — refreshes prompts after the commit lands
- `update-release-details.ps1 -Refresh` — updates README metadata (development end, branch, release commit)

Post-commit changes are staged automatically for the next commit.

## Push-time automation

After push to `main`, `wait-and-trigger-pull.ps1` (started by `post-push-hook.ps1`):

- Waits for CI success on the pushed commit
- `publish-release.ps1` — tag/GitHub Release only when `notes.md` is publish-ready; then `close-release.ps1` opens the next version
- Triggers NAS deploy
