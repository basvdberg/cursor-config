# local server deployment reference

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
| Device | QNAP (local server) |
| HTTPS edge | **nginx-office-c2h** → host **80/443** (target) |
| Internal URLs | `https://<app>.<zone>/` |
| Public URLs | `https://<app>.office.c2h.nl/` |

### NGINX on QNAP Docker

Prefer `proxy_pass http://<container_name>:<container_port>` on a shared Docker network. Reload: `docker exec nginx-office-c2h nginx -s reload`.

## Dual-zone architecture

```text
office.c2h.nl  ──► public DNS ──► WAN ──► NGINX :443  (LE cert)
<app>.<zone>   ──► LAN DNS only ──► NGINX :443       (internal CA *.example)
```

Never publish `*.example` on public DNS.

## DNS

### Public DNS (c2h.nl / office)

| Record | Action |
|--------|--------|
| `*.office.c2h.nl` | Keep for `expose: public` |
| `*.example` / `<app>.<zone>` | **Do not add** |

### LAN DNS

```text
*.example  A  ${LOCAL_SERVER_LAN_IP}   # e.g. 192.168.2.2
```

VPN: push the same resolver or split DNS.

## TLS

| Zone | Certificate |
|------|-------------|
| `office.c2h.nl` | Let's Encrypt (existing) |
| `*.example` | Internal CA wildcard — trust root on clients |

```text
nginx/ssl/office.c2h.nl/
nginx/ssl/<zone>/
```

## public-exposure.yaml

| `expose` | URL | Public DNS |
|----------|-----|------------|
| `internal` | `https://<app>.<zone>/` | No |
| `public` | `https://<app>.office.c2h.nl/` | Yes |

Templates: `nginx-app-basnas.conf`, `nginx-app-public.conf`, `nginx-admin-qts.conf`.

## Hostname notes

| Name | Use |
|------|-----|
| `<zone>` (short hostname) | QNAP mDNS/LAN hostname — not the HTTPS app zone |
| `admin.example` | QTS via NGINX |
| `airflow.<zone>` | Airflow UI |

## Port fixation, shares, deploy

See main [SKILL.md](SKILL.md). Update [basnas-inventory.yaml](basnas-inventory.yaml) after each deploy.
