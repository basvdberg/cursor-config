# NGINX as HTTPS edge on port 443 (BasNAS / QNAP)

## Table of contents

<!-- markdown-toc:start -->
- [Internal zone: *.basnas](#internal-zone-basnas)
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

Terminate **`https://*.basnas/`** (internal, internal CA) and **`https://*.office.c2h.nl/`** (public, Let's Encrypt) on **nginx-office-c2h** at host **80** and **443**.

## Internal zone: `*.basnas`

| Item | Value |
|------|--------|
| URL | `https://<application>.basnas/` |
| DNS | LAN only: `*.basnas` → `192.168.2.2` |
| TLS | **Internal CA** wildcard `*.basnas` (LE not available) |
| QTS | `https://admin.basnas/` → host QTS HTTPS `:8443` (not `:8080` — jobhunter) |

Install the CA root on every client once.

## Public zone: `*.office.c2h.nl`

Unchanged — public DNS, Let's Encrypt, `ssl/office.c2h.nl/`.

## Steps

### 1. LAN DNS

```text
*.basnas       A  192.168.2.2
admin.basnas   A  192.168.2.2
```

### 2. Free host port 443 from QTS

Move QNAP system HTTPS to **8443** (or access QTS only via `https://admin.basnas/`).

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
# CN=BasNAS Internal CA, issue SAN: *.basnas, admin.basnas
```

Copy `fullchain.pem` and `privkey.pem` to NAS mount → `/etc/nginx/ssl/basnas/` in the container.

### 5. Vhosts

- Apps: [templates/nginx-app-basnas.conf](templates/nginx-app-basnas.conf)
- QTS: [templates/nginx-admin-qts.conf](templates/nginx-admin-qts.conf)
- Public: [templates/nginx-app-public.conf](templates/nginx-app-public.conf)

```bash
docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload
```

### 6. Trust CA on Windows

Import CA root → **Trusted Root Certification Authorities** → browse `https://airflow.basnas/`.

## Verify

```bash
nslookup airflow.basnas
curl -vI https://airflow.basnas/
```

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
