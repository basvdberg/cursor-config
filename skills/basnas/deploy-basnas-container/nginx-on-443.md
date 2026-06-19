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
| QTS | `https://admin.example/` → host QTS HTTPS `:8443` (not host `:8080`) |

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
