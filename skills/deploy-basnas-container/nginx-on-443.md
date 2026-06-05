# NGINX as HTTPS edge on port 443 (local server / QNAP)

## Table of contents

<!-- markdown-toc:start -->
- [Internal zone: *.example](#internal-zone-example)
- [Public zone: *.office.c2h.nl](#public-zone-officec2hnl)
- [Steps](#steps)
  - [1. LAN DNS](#1-lan-dns)
  - [2. Free host port 443 from QTS](#2-free-host-port-443-from-qts)
  - [3. Remap nginx-office-c2h](#3-remap-nginx-office-c2h)
  - [4. Issue internal CA certificate](#4-issue-internal-ca-certificate)
  - [5. Vhosts](#5-vhosts)
  - [6. Trust CA on Windows](#6-trust-ca-on-windows)
- [Verify](#verify)
<!-- markdown-toc:end -->

Terminate **`https://*.example/`** (internal, internal CA) and **`https://*.office.c2h.nl/`** (public, Let's Encrypt) on **nginx-office-c2h** at host **80** and **443**.

## Internal zone: `*.example`

| Item | Value |
|------|--------|
| URL | `https://<application>.<zone>/` |
| DNS | LAN only: `*.example` → `192.168.2.2` |
| TLS | **Internal CA** wildcard `*.example` (LE not available) |
| QTS | `https://admin.example/` → host QTS HTTPS `:8443` (not `:8080` — jobhunter) |

Install the CA root on every client once.

## Public zone: `*.office.c2h.nl`

Unchanged — public DNS, Let's Encrypt, `ssl/office.c2h.nl/`.

## Steps

### 1. LAN DNS

```text
*.example       A  192.168.2.2
admin.example   A  192.168.2.2
```

### 2. Free host port 443 from QTS

Move QNAP system HTTPS to **8443** (or access QTS only via `https://admin.example/`).

### 3. Remap nginx-office-c2h

```yaml
ports:
  - "80:80"
  - "443:443"
```

### 4. Issue internal CA certificate

Example with **mkcert** (dev) or **step-ca** / OpenSSL CA (production homelab):

```bash
# Example: OpenSSL — create CA once, then:
# CN=local server Internal CA, issue SAN: *.example, admin.example
```

Copy `fullchain.pem` and `privkey.pem` to NAS mount → `/etc/nginx/ssl/<zone>/` in the container.

### 5. Vhosts

- Apps: [templates/nginx-app-basnas.conf](templates/nginx-app-basnas.conf)
- QTS: [templates/nginx-admin-qts.conf](templates/nginx-admin-qts.conf)
- Public: [templates/nginx-app-public.conf](templates/nginx-app-public.conf)

```bash
docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload
```

### 6. Trust CA on Windows

Import CA root → **Trusted Root Certification Authorities** → browse `https://airflow.example/`.

## Verify

```bash
nslookup airflow.<zone>
curl -vI https://airflow.example/
```

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
      - [Fix admin hostname not resolving](dns-basnas-setup.md)
      - [Examples](examples.md)
      - [NGINX as HTTPS edge on port 443 (local server / QNAP)](nginx-on-443.md)
      - [local server deployment reference](reference.md)
      - [Deploy container service on local server](SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.example)](troubleshooting-tls.md)
      - [local server URL map](url-map.md)
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
      - [Examples](../troubleshooting-error-log/examples.md)
      - [Troubleshooting error reference](../troubleshooting-error-log/reference.md)
      - [Troubleshooting error log](../troubleshooting-error-log/SKILL.md)
- Related repositories
  - [Data Engineering 2026](https://github.com/basvdberg/data-engineering-2026) — Course and learning materials
  - [Data Engineering Design Patterns](https://github.com/basvdberg/data-engineering-design-patterns) — Design pattern catalogue
  - [Data Solution 2026](https://github.com/basvdberg/data-solution-2026) — Data solution proof of concept
<!-- markdown-project-structure:end -->
