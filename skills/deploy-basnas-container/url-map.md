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
| Kafka UI | https://kafka.example/ | `kafka-ui:8080` |
| Airflow | https://airflow.example/ | `airflow-standalone:8080` |
| Jobhunter | https://jobhunter.example/ | `jobhunter-app:8080` |
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

Kafka broker `kafka:9092`, Immich Postgres/Redis/ML.

## Public (`office.c2h.nl`)

Only `expose: public` apps. See [service-url-map.yaml](service-url-map.yaml).

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
