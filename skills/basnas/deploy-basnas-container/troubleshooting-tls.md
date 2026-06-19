# Troubleshooting “Your connection is not private” (*.example)

## Table of contents

<!-- markdown-toc:start -->
- [Common causes](#common-causes)
- [Fix order](#fix-order)
  - [1. LAN DNS only](#1-lan-dns-only)
  - [2. NGINX on 443](#2-nginx-on-443)
  - [3. Internal CA for *.example](#3-internal-ca-for-example)
  - [4. Vhost + reload](#4-vhost-reload)
  - [5. Re-issue cert (Windows SEC_E_WRONG_PRINCIPAL)](#5-re-issue-cert-windows-sec_e_wrong_principal)
- [Verify](#verify)
<!-- markdown-toc:end -->

Browser TLS errors are **not** SSH-related. They mean the **HTTPS certificate** does not match or is not trusted for `https://<app>.<zone>/`.

**Preferred setup:** [nginx-on-443.md](nginx-on-443.md).

## Common causes

1. **DNS** — `*.example` missing on LAN, or an old public record points elsewhere.
2. **Wrong port** — QTS on host `:443` instead of **nginx-office-c2h** (NGINX should own 80/443).

3. **admin.example hangs** — Do not proxy to host `:8080`. QTS is **`https://192.168.2.2:8443`** from inside the NGINX container (`proxy_ssl_verify off`). Run `scripts/fix-admin-basnas-upstream.sh`.
4. **No vhost** — no `server_name app.basnas` in NGINX.
5. **Untrusted cert** — internal CA root not installed on your PC ([install-windows-basnas-ca.ps1](scripts/install-windows-basnas-ca.ps1)).
6. **Windows name mismatch** — Schannel rejects wildcard-only `*.example` for `airflow.<zone>` etc. Re-issue with explicit SANs: [reissue-basnas-cert.sh](scripts/reissue-basnas-cert.sh).

## Fix order

### 1. LAN DNS only

```text
*.example     A    192.168.2.2
admin.example A    192.168.2.2
```

Do **not** add `*.example` on your public DNS provider.

`nslookup airflow.<zone>` → **192.168.2.2**.

### 2. NGINX on 443

Free QTS from port 443; map container **80:80** and **443:443**. See [nginx-on-443.md](nginx-on-443.md).

### 3. Internal CA for `*.example`

Issue wildcard cert; mount:

```text
/etc/nginx/ssl/<zone>/fullchain.pem
/etc/nginx/ssl/<zone>/privkey.pem
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

### 5. Re-issue cert (Windows `SEC_E_WRONG_PRINCIPAL`)

If browsers or `curl` fail with *target principal name is incorrect* but `-k` works, the leaf cert likely has only `*.example`. On local server:

```bash
sed -i 's/\r$//' reissue-basnas-cert.sh && ./reissue-basnas-cert.sh
```

## Verify

```bash
nslookup admin.example
curl -vI https://admin.example/
```
