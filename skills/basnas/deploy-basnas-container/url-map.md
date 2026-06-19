# local server URL map

## Table of contents

<!-- markdown-toc:start -->
- [HTTPS via NGINX (*.example) — LAN / VPN only](#https-via-nginx-example-lan-vpn-only)
- [Docker only (no browser URL)](#docker-only-no-browser-url)
- [Public (office.c2h.nl)](#public-officec2hnl)
<!-- markdown-toc:end -->

Human-readable summary. **Canonical URLs:** [service-url-map.yaml](service-url-map.yaml) and [local-server.env.example](local-server.env.example).

NGINX: **nginx-office-c2h** → target host **80/443** ([nginx-on-443.md](nginx-on-443.md)). LAN DNS: `*.<zone>` → `${LOCAL_SERVER_LAN_IP}`.

## HTTPS via NGINX (`*.example`) — LAN / VPN only

| Service | URL | NGINX upstream |
|---------|-----|----------------|
| **QNAP QTS** | https://admin.example/ | QNAP host HTTPS `:8443` |
| Airflow | https://airflow.example/ | `airflow-standalone:8080` |
| Immich | https://immich.example/ | `immich_server:2283` |
| Plex | https://plex.example/ | `plex:32400` (planned) |
| qBittorrent | https://qbittorrent.example/ | `qbittorrent-1:8080` |
| Radarr | https://radarr.example/ | `radarr-3:7878` |
| NZBGet | https://nzbget.example/ | `nzbget-2:6789` |
| Homebridge | https://homebridge.example/ | `homebridge-2:8581` |
| AdGuard | https://adguard.example/ | planned |

**Open-Meteo / data jobs:** https://airflow.example/ (DAGs).

**TLS:** internal CA for `*.example` — install root on each device.

## Docker only (no browser URL)

Immich Postgres/Redis/ML.

## Public (`office.c2h.nl`)

Only `expose: public` apps. See [service-url-map.yaml](service-url-map.yaml).
