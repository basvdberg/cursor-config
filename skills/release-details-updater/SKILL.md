---
name: release-details-updater
description: Maintain release/details metadata and prompts per release version. Use when creating releases, updating release notes, or when the user asks to keep release details synchronized on each commit.
disable-model-invocation: true
---

# Release Details Updater

## Purpose

Keep `release/details/` complete and consistent with `release/VERSION`, release notes, and commit history.

## Required outputs per release

For each release version, ensure:

- `release/details/<version>/README.md`
- `release/details/<version>/prompts.md`

Also maintain:

- `release/details/README.md` with a sequential release overview.

## Workflow

1. Read `release/VERSION`.
2. Ensure `release/details/<version>/` exists.
3. Update `<version>/README.md` with:
   - start and end development date/time
   - release commit/tag info
   - sequential summary of changes
4. Update `<version>/prompts.md` with all prompts used in that release.
5. Keep `release/details/README.md` in sync with ordered release history.

## Commit-time automation

Shared Git hooks from [cursor-config](https://github.com/basvdberg/cursor-config) (`core.hooksPath`):

**Pre-commit** (`pre_commit.py`):

- `new-release.ps1` — bumps `release/VERSION` and scaffolds notes/details for the next release (on `main`, unless `SKIP_RELEASE=1` or only metadata files are staged)
- `update_prompts.py` — writes `release/details/<version>/prompts.md`
- `update-release-details.ps1` — bootstraps missing `README.md` and the details index

**Post-commit** (`post_commit.py` + `release/scripts/post-commit-hook.ps1`):

- `update_prompts.py` — refreshes prompts after the commit lands
- `update-release-details.ps1 -Refresh` — updates README metadata (development end, branch, release commit)

Post-commit changes are staged automatically for the next commit.

## Push-time automation

After push to `main`, `wait-and-trigger-pull.ps1` (started by `post-push-hook.ps1`):

- Waits for CI success on the pushed commit
- `publish-release.ps1` — creates/pushes annotated tag and GitHub Release from `release/notes/<version>.md`
- Triggers NAS deploy
