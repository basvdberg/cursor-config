# BasNAS URL map

## Table of contents

<!-- markdown-toc:start -->
- [HTTPS via NGINX (*.basnas) — LAN / VPN only](#https-via-nginx-basnas-lan-vpn-only)
- [Docker only (no browser URL)](#docker-only-no-browser-url)
- [Public (office.c2h.nl)](#public-officec2hnl)
<!-- markdown-toc:end -->

NGINX: **nginx-office-c2h** → target host **80/443** ([nginx-on-443.md](nginx-on-443.md)). LAN DNS: `*.basnas` → **192.168.2.2**.

## HTTPS via NGINX (`*.basnas`) — LAN / VPN only

| Service | URL | NGINX upstream |
|---------|-----|----------------|
| **QNAP QTS** | https://admin.basnas/ | QNAP host HTTPS `:8443` |
| Kafka UI | https://kafka.basnas/ | `kafka-ui:8080` |
| Airflow | https://airflow.basnas/ | `airflow-standalone:8080` |
| Jobhunter | https://jobhunter.basnas/ | `jobhunter-app:8080` |
| Immich | https://immich.basnas/ | `immich_server:2283` |
| Plex | https://plex.basnas/ | `plex:32400` (planned) |
| qBittorrent | https://qbittorrent.basnas/ | `qbittorrent-1:8080` |
| Radarr | https://radarr.basnas/ | `radarr-3:7878` |
| NZBGet | https://nzbget.basnas/ | `nzbget-2:6789` |
| Homebridge | https://homebridge.basnas/ | `homebridge-2:8581` |
| AdGuard | https://adguard.basnas/ | planned |

**Open-Meteo / data jobs:** https://airflow.basnas/ (DAGs).

**TLS:** internal CA for `*.basnas` — install root on each device.

## Docker only (no browser URL)

Kafka broker `kafka:9092`, Immich Postgres/Redis/ML.

## Public (`office.c2h.nl`)

Only `expose: public` apps. See [service-url-map.yaml](service-url-map.yaml).

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
