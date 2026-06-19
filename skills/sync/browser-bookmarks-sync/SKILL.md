---
name: browser-bookmarks-sync
description: >-
  Merge Chrome and Brave bookmarks, inject local server service URLs from service-url-map.yaml,
  and commit to the private browser-bookmarks-sync repo for Floccus (desktop + iPhone).
  Use when syncing bookmarks, deploying local server containers, or updating Floccus Git targets.
disable-model-invocation: true
---

# Browser bookmarks sync

**Floccus target repo:** browser-bookmarks-sync (private; workspace folder `browser-bookmarks-sync/`).  
**Config:** [browser-bookmarks-sync.json](../../../browser-bookmarks-sync.json) at cursor-config root.  
**local server URLs source:** [service-url-map.yaml](../../basnas/deploy-basnas-container/service-url-map.yaml).

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

**User menu:** double-click `browser-bookmarks-sync/manage-bookmarks.cmd` — see [manage-bookmarks.md](../../../../browser-bookmarks-sync/docs/manage-bookmarks.md).

Clone the bookmarks repo if missing (sibling of `cursor-config` in this workspace):

```powershell
cd "..\.."   # Data Engineering 2.0 root (from cursor-config)
git clone <browser-bookmarks-sync private remote>
```

## Commands

From **cursor-config** (or with `CURSOR_CONFIG_ROOT` set):

```powershell
$cfg = Resolve-Path .
$env:CURSOR_CONFIG_ROOT = $cfg
python "$cfg\scripts\sync_browser_bookmarks.py"              # merge + local server
python "$cfg\scripts\sync_browser_bookmarks.py" --basnas       # local server folder only
python "$cfg\scripts\sync_browser_bookmarks.py" --merge      # Chrome + Brave only
python "$cfg\scripts\sync_browser_bookmarks.py" --commit --push
```

Wrapper:

```powershell
.\scripts\sync-browser-bookmarks.ps1 --basnas --commit --push
```

## local server folder in HTML

The script maintains a **local server** folder between HTML markers:

```html
<!-- cursor-config:basnas:start -->
...
<!-- cursor-config:basnas:end -->
```

Only that block is overwritten from `service-url-map.yaml`. Personal folders (including legacy **local server**) are left unchanged unless you run a full `--merge`, which rebuilds the file from browser profiles.

**Favicons:** Floccus does not sync `ICON` in HTML. After `--basnas`, run `sync_browser_bookmarks.py --apply-favicons` with Chrome/Brave closed (or menu **11** in `manage-bookmarks.cmd`). Icons are 32×32 PNGs in `bookmarks/basnas-icons/`, injected into each browser’s `Favicons` SQLite DB.

## With local server deploy

When [deploy-basnas-container](../../basnas/deploy-basnas-container/SKILL.md) adds or changes a service URL:

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

Setup details: [floccus-setup.md](../../../../browser-bookmarks-sync/docs/floccus-setup.md).

## Agent checklist

- [ ] `service-url-map.yaml` reflects new `https://<app>.basnas/` URL
- [ ] `sync_browser_bookmarks.py --basnas` (or full sync if user asked to merge browsers)
- [ ] `--apply-favicons` after local server URL changes (browsers must be closed)
- [ ] Commit/push only when user wants bookmarks repo updated
- [ ] Remind user to Floccus sync if push was skipped
