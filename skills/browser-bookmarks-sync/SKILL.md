## Table of contents

<!-- markdown-toc:start -->
- [Layout](#layout)
- [Commands](#commands)
- [BasNAS folder in HTML](#basnas-folder-in-html)
- [With BasNAS deploy](#with-basnas-deploy)
- [Floccus](#floccus)
- [Agent checklist](#agent-checklist)
<!-- markdown-toc:end -->

---
name: browser-bookmarks-sync
description: >-
  Merge Chrome and Brave bookmarks, inject BasNAS service URLs from service-url-map.yaml,
  and commit to the private browser-bookmarks-sync repo for Floccus (desktop + iPhone).
  Use when syncing bookmarks, deploying BasNAS containers, or updating Floccus Git targets.
---

# Browser bookmarks sync

**Floccus target repo:** [browser-bookmarks-sync](https://github.com/basvdberg/browser-bookmarks-sync) (private).  
**Config:** [browser-bookmarks-sync.json](../../browser-bookmarks-sync.json) at cursor-config root.  
**BasNAS URLs source:** [service-url-map.yaml](../deploy-basnas-container/service-url-map.yaml).

## Layout

```text
Data Engineering 2.0/
  cursor-config/
    browser-bookmarks-sync.json
    scripts/sync_browser_bookmarks.py
  browser-bookmarks-sync/
    manage-bookmarks.cmd          # interactive menu (user-facing)
    scripts/bookmark_utils.py     # stats, list, duplicates
    bookmarks/merged-bookmarks.html
```

**User menu:** double-click `browser-bookmarks-sync/manage-bookmarks.cmd` — see [manage-bookmarks.md](https://github.com/basvdberg/browser-bookmarks-sync/blob/main/docs/manage-bookmarks.md).

Clone the bookmarks repo if missing (sibling of `cursor-config` in this workspace):

```powershell
cd "..\.."   # Data Engineering 2.0 root (from cursor-config)
git clone https://github.com/basvdberg/browser-bookmarks-sync.git
```

## Commands

From **cursor-config** (or with `CURSOR_CONFIG_ROOT` set):

```powershell
$cfg = Resolve-Path .
$env:CURSOR_CONFIG_ROOT = $cfg
python "$cfg\scripts\sync_browser_bookmarks.py"              # merge + BasNAS
python "$cfg\scripts\sync_browser_bookmarks.py" --basnas       # BasNAS folder only
python "$cfg\scripts\sync_browser_bookmarks.py" --merge      # Chrome + Brave only
python "$cfg\scripts\sync_browser_bookmarks.py" --commit --push
```

Wrapper:

```powershell
.\scripts\sync-browser-bookmarks.ps1 --basnas --commit --push
```

## BasNAS folder in HTML

The script maintains a **BasNAS** folder between HTML markers:

```html
<!-- cursor-config:basnas:start -->
...
<!-- cursor-config:basnas:end -->
```

Only that block is overwritten from `service-url-map.yaml`. Personal folders (including legacy **Basnas**) are left unchanged unless you run a full `--merge`, which rebuilds the file from browser profiles.

## With BasNAS deploy

When [deploy-basnas-container](../deploy-basnas-container/SKILL.md) adds or changes a service URL:

1. Update `service-url-map.yaml` (and deploy registries).
2. Run `sync_browser_bookmarks.py --basnas --commit --push`.
3. Floccus pulls on each device (or sync manually once).

## Floccus

| Setting | Value |
|---------|--------|
| Git server | `https://github.com` |
| Repository | `basvdberg/browser-bookmarks-sync` |
| Branch | `main` |
| Bookmark file | `bookmarks/merged-bookmarks.html` |

Setup details: [floccus-setup.md](https://github.com/basvdberg/browser-bookmarks-sync/blob/main/docs/floccus-setup.md).

## Agent checklist

- [ ] `service-url-map.yaml` reflects new `https://<app>.basnas/` URL
- [ ] `sync_browser_bookmarks.py --basnas` (or full sync if user asked to merge browsers)
- [ ] Commit/push only when user wants bookmarks repo updated
- [ ] Remind user to Floccus sync if push was skipped

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](SKILL.md)
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Deploy Basnas Container
      - Templates
      - [Fix `admin.basnas` not resolving](../deploy-basnas-container/dns-basnas-setup.md)
      - [Examples](../deploy-basnas-container/examples.md)
      - [NGINX as HTTPS edge on port 443 (BasNAS / QNAP)](../deploy-basnas-container/nginx-on-443.md)
      - [BasNAS deployment reference](../deploy-basnas-container/reference.md)
      - [Deploy container service on BasNAS](../deploy-basnas-container/SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.basnas)](../deploy-basnas-container/troubleshooting-tls.md)
      - [BasNAS URL map](../deploy-basnas-container/url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Review Markdown Structure
      - [Review Markdown structure](../review-markdown-structure/SKILL.md)
- Related repositories
  - [Browser bookmarks sync](https://github.com/basvdberg/browser-bookmarks-sync)
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026)
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns)
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026)
<!-- markdown-project-structure:end -->
