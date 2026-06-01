# Troubleshooting “Your connection is not private” (*.basnas)

## Table of contents

<!-- markdown-toc:start -->
- [Common causes](#common-causes)
- [Fix order](#fix-order)
  - [1. LAN DNS only](#1-lan-dns-only)
  - [2. NGINX on 443](#2-nginx-on-443)
  - [3. Internal CA for *.basnas](#3-internal-ca-for-basnas)
  - [4. Vhost + reload](#4-vhost-reload)
- [Verify](#verify)
<!-- markdown-toc:end -->

Browser TLS errors are **not** SSH-related. They mean the **HTTPS certificate** does not match or is not trusted for `https://<app>.basnas/`.

**Preferred setup:** [nginx-on-443.md](nginx-on-443.md).

## Common causes

1. **DNS** — `*.basnas` missing on LAN, or an old public record points elsewhere.
2. **Wrong port** — QTS on host `:443` instead of **nginx-office-c2h** (NGINX should own 80/443).

3. **admin.basnas hangs** — Upstream was `:8080` (jobhunter). QTS is **`https://192.168.2.2:8443`** from inside the NGINX container (`proxy_ssl_verify off`). Run `scripts/fix-admin-basnas-upstream.sh`.
4. **No vhost** — no `server_name app.basnas` in NGINX.
5. **Untrusted cert** — internal CA root not installed on your PC, or cert lacks `*.basnas` SAN.

## Fix order

### 1. LAN DNS only

```text
*.basnas     A    192.168.2.2
admin.basnas A    192.168.2.2
```

Do **not** add `*.basnas` on your public DNS provider.

`nslookup airflow.basnas` → **192.168.2.2**.

### 2. NGINX on 443

Free QTS from port 443; map container **80:80** and **443:443**. See [nginx-on-443.md](nginx-on-443.md).

### 3. Internal CA for `*.basnas`

Issue wildcard cert; mount:

```text
/etc/nginx/ssl/basnas/fullchain.pem
/etc/nginx/ssl/basnas/privkey.pem
```

Install the **CA root** on Windows (Trusted Root Certification Authorities):

```powershell
.\scripts\install-windows-basnas-ca.ps1
```

Or copy `basnas-ca.crt` from `/share/.../nginx-office-c2h/certs/basnas-ca.crt` and run `certutil -addstore -user Root basnas-ca.crt`. Restart the browser after install.

Let's Encrypt cannot issue for `.basnas`. `curl` on Windows may still report revocation errors for private CAs; use `curl.exe --ssl-no-revoke` or trust via the browser (Edge/Chrome use the Windows store).

### 4. Vhost + reload

```bash
docker exec nginx-office-c2h nginx -t
docker exec nginx-office-c2h nginx -s reload
```

## Verify

```bash
nslookup admin.basnas
curl -vI https://admin.basnas/
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
