# BasNAS deployment reference

## Table of contents

<!-- markdown-toc:start -->
- [Platform](#platform)
  - [NGINX on QNAP Docker](#nginx-on-qnap-docker)
- [Dual-zone architecture](#dual-zone-architecture)
- [DNS](#dns)
  - [Public DNS (c2h.nl / office)](#public-dns-c2hnl-office)
  - [LAN DNS](#lan-dns)
- [TLS](#tls)
- [public-exposure.yaml](#public-exposureyaml)
- [Hostname notes](#hostname-notes)
- [Port fixation, shares, deploy](#port-fixation-shares-deploy)
<!-- markdown-toc:end -->

## Platform

| Item | Value |
|------|--------|
| Device | QNAP (BasNAS) |
| HTTPS edge | **nginx-office-c2h** → host **80/443** (target) |
| Internal URLs | `https://<app>.basnas/` |
| Public URLs | `https://<app>.office.c2h.nl/` |

### NGINX on QNAP Docker

Prefer `proxy_pass http://<container_name>:<container_port>` on a shared Docker network. Reload: `docker exec nginx-office-c2h nginx -s reload`.

## Dual-zone architecture

```text
office.c2h.nl  ──► public DNS ──► WAN ──► NGINX :443  (LE cert)
<app>.basnas   ──► LAN DNS only ──► NGINX :443       (internal CA *.basnas)
```

Never publish `*.basnas` on public DNS.

## DNS

### Public DNS (c2h.nl / office)

| Record | Action |
|--------|--------|
| `*.office.c2h.nl` | Keep for `expose: public` |
| `*.basnas` / `<app>.basnas` | **Do not add** |

### LAN DNS

```text
*.basnas  A  <basnas-lan-ip>   # e.g. 192.168.2.2
```

VPN: push the same resolver or split DNS.

## TLS

| Zone | Certificate |
|------|-------------|
| `office.c2h.nl` | Let's Encrypt (existing) |
| `*.basnas` | Internal CA wildcard — trust root on clients |

```text
nginx/ssl/office.c2h.nl/
nginx/ssl/basnas/
```

## public-exposure.yaml

| `expose` | URL | Public DNS |
|----------|-----|------------|
| `internal` | `https://<app>.basnas/` | No |
| `public` | `https://<app>.office.c2h.nl/` | Yes |

Templates: `nginx-app-basnas.conf`, `nginx-app-public.conf`, `nginx-admin-qts.conf`.

## Hostname notes

| Name | Use |
|------|-----|
| `basnas` (short) | QNAP mDNS/LAN hostname — not the HTTPS app zone |
| `admin.basnas` | QTS via NGINX |
| `airflow.basnas` | Airflow UI |

## Port fixation, shares, deploy

See main [SKILL.md](SKILL.md). Update [basnas-inventory.yaml](basnas-inventory.yaml) after each deploy.

## Project structure

<!-- markdown-project-structure:start -->
- [cursor-config](../../readme.md)
  - Githooks
  - Skills
    - Browser Bookmarks Sync
      - [Browser bookmarks sync](../browser-bookmarks-sync/SKILL.md)
    - Create Design Pattern
      - [Create design pattern](../create-design-pattern/SKILL.md)
      - [{Title}](../create-design-pattern/TEMPLATE.md)
    - Deploy Basnas Container
      - Templates
      - [Fix `admin.basnas` not resolving](dns-basnas-setup.md)
      - [Examples](examples.md)
      - [NGINX as HTTPS edge on port 443 (BasNAS / QNAP)](nginx-on-443.md)
      - [BasNAS deployment reference](reference.md)
      - [Deploy container service on BasNAS](SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.basnas)](troubleshooting-tls.md)
      - [BasNAS URL map](url-map.md)
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
