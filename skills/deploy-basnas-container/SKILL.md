## Table of contents

<!-- markdown-toc:start -->
- [Dual DNS zones](#dual-dns-zones)
- [Data Solution 2026 (app deploy via CI/CD)](#data-solution-2026-app-deploy-via-cicd)
- [Non-negotiable rules](#non-negotiable-rules)
- [local server layout](#local-server-layout)
- [Workflow](#workflow)
  - [Step 6: NGINX templates](#step-6-nginx-templates)
  - [Step 7: LAN DNS](#step-7-lan-dns)
  - [Step 8: Internal CA (required for the local DNS zone)](#step-8-internal-ca-required-for-the-local-dns-zone)
- [Agent deliverables](#agent-deliverables)
  - [Step 9: Browser bookmarks (Floccus)](#step-9-browser-bookmarks-floccus)
- [Additional resources](#additional-resources)
<!-- markdown-toc:end -->

## Table of contents


---
name: deploy-basnas-container
description: >-
  Design and deploy Docker services on local server with fixed host ports, NGINX
  HTTPS termination, dual DNS (office.c2h.nl public, local DNS zone in local-server.env.example), NAS share
  mounts, and a public-exposure registry. Use when deploying containers on local server,
  QNAP, office.c2h.nl, application.<zone> internal hostnames, NGINX reverse proxy,
  or exposing services to the internet. For data-solution-2026 app/DAG/poller
  releases, use deploy-data-solution-basnas (commit and push to main)—not manual
  SSH git pull.
---

# Deploy container service on local server

The local server is a **QNAP** running **Container Station**. **NGINX runs in Docker** on the QNAP and is the HTTPS edge for all app containers.

**Connection settings:** [local-server.env.example](local-server.env.example). **Service inventory:** [basnas-inventory.yaml](basnas-inventory.yaml). **Canonical URLs:** [service-url-map.yaml](service-url-map.yaml) / [url-map.md](url-map.md).

**SSH / docker on NAS:** use plain `ssh bas@basnas 'docker …'` after one-time setup — see [basnas-ssh](../basnas-ssh/SKILL.md). Do not prefix every command with `bash -lc` + `nas-path.sh`.

## Dual DNS zones

| Zone | URL pattern | Public DNS | Use for |
|------|-------------|------------|---------|
| **office** (existing) | `https://<application>.office.c2h.nl/` | **Yes** → WAN → NGINX | `expose: public` only |
| **local zone** (default) | `https://<application>.<zone>/` | **No** — LAN/VPN only | `expose: internal` (default) |

NGINX uses separate TLS certs: `ssl/office.c2h.nl/` (Let's Encrypt) and `ssl/<zone>/` (**internal CA**, wildcard `*.example`). Never publish `*.example` on public DNS.

**QTS admin:** `https://admin.example/` (not `<short-hostname>.<zone>` — avoid duplicating the QNAP short hostname as a subdomain).

## Data Solution 2026 (app deploy via CI/CD)

**Do not** deploy `data-solution-2026` application code by SSH `git pull` or `deploy-on-nas.sh` as the default step after making changes.

| Change type | How to deploy |
|-------------|----------------|
| Code, DAGs, poller, extractor, metadata in repo | **Commit and push to `main`** → CI/CD → post-push deploys NAS ([deploy-data-solution-basnas](../deploy-data-solution-basnas/SKILL.md)) |
| `infra/` compose or `.env` on NAS | After push, `RUN_INFRA_SYNC=1` on NAS (see that skill) |
| New HTTPS vhost, port, or NGINX upstream | This skill (registry + templates below) |

Airflow/Kafka/Postgres URLs: `https://airflow.example/`, `https://kafka.example/` (inventory in [basnas-inventory.yaml](basnas-inventory.yaml)).

## Non-negotiable rules

1. **Fixed ports** — Register in `port-registry.yaml`; prefer Docker network + service name, no host publish.
2. **HTTPS via NGINX** — No TLS in app containers ([reference.md](reference.md#nginx-on-qnap-docker)).
3. **DNS by exposure** — `internal` → `https://<application>.<zone>/`; `public` → `https://<application>.office.c2h.nl/`.
4. **Public exposure** — Only `expose: public` on `office.c2h.nl`. Default `internal` + local zone only.
5. **Network share** — Bind-mount from NAS share per app.

## local server layout

```text
/docker/   # or /share/.../docker/ on QNAP
  registry/
    port-registry.yaml
    public-exposure.yaml
  services/<application>/
  nginx/
    conf.d/
    ssl/
      office.c2h.nl/    # public zone (LE)
      <zone>/           # internal zone (LOCAL_SERVER_DNS_ZONE; internal CA)
  shares/<application>/
```

## Workflow

```text
- [ ] 1. Choose <application> and container_port
- [ ] 2. Allocate host_port in port-registry.yaml (if needed)
- [ ] 3. public-exposure.yaml (expose + url https://<application>.<zone>/)
- [ ] 4. Create NAS share
- [ ] 5. docker-compose.yml
- [ ] 6. nginx vhost from templates/nginx-app-basnas.conf
- [ ] 7. LAN DNS: *.example → local server LAN IP (never on public DNS)
- [ ] 8. Verify HTTPS with trusted internal CA
- [ ] 9. Update browser bookmarks (service-url-map → Floccus repo)
```

### Step 6: NGINX templates

| Exposure | Template |
|----------|----------|
| `internal` | [templates/nginx-app-basnas.conf](templates/nginx-app-basnas.conf) |
| QTS admin | [templates/nginx-admin-qts.conf](templates/nginx-admin-qts.conf) |
| `public` | [templates/nginx-app-public.conf](templates/nginx-app-public.conf) |

Reload: `docker exec nginx-office-c2h nginx -t && docker exec nginx-office-c2h nginx -s reload`.

**Bulk deploy** all `https_basnas` services: copy [scripts/deploy-all-basnas-vhosts.sh](scripts/deploy-all-basnas-vhosts.sh) to local server, `sed -i 's/\r$//'`, run it, then `scripts/patch-bridge-upstreams.sh` if radarr/nzbget upstreams change after container recreate.

**Windows TLS name check:** use explicit SANs per hostname (not only `*.example`). After adding apps, run [scripts/reissue-basnas-cert.sh](scripts/reissue-basnas-cert.sh) on local server.

### Step 7: LAN DNS

```text
*.example  A  192.168.2.2
```

Or per-app records. **AdGuard** on QNAP (planned) can serve this zone.

### Step 8: Internal CA (required for the local DNS zone)

Let's Encrypt does **not** issue for private LAN zones. Issue a wildcard cert for your local DNS zone (see [local-server.env.example](local-server.env.example)), mount to NGINX, install the CA root on client devices once. See [nginx-on-443.md](nginx-on-443.md).

## Agent deliverables

1. Registry snippets with `url: https://<application>.<zone>/`
2. `docker-compose.yml`
3. NGINX vhost (`<application>.<zone>`)
4. LAN DNS note (`*.example` only)
5. If `public`: `office.c2h.nl` + public DNS
6. Run bookmark sync: `cursor-config/scripts/sync_browser_bookmarks.py --basnas` (see [browser-bookmarks-sync](../browser-bookmarks-sync/SKILL.md))

### Step 9: Browser bookmarks (Floccus)

After `service-url-map.yaml` has the canonical `url`, refresh the **local server** folder in [browser-bookmarks-sync](https://github.com/basvdberg/browser-bookmarks-sync):

```powershell
$cfg = Resolve-Path ..\cursor-config   # Data Engineering 2.0\cursor-config
$env:CURSOR_CONFIG_ROOT = $cfg
python "$cfg\scripts\sync_browser_bookmarks.py" --basnas --commit --push
```

Floccus on Chrome, Brave, and iPhone uses `bookmarks/merged-bookmarks.html` on branch `main`.

## Additional resources

- [basnas-inventory.yaml](basnas-inventory.yaml) · [service-url-map.yaml](service-url-map.yaml) · [browser-bookmarks-sync](../browser-bookmarks-sync/SKILL.md)
- [reference.md](reference.md) · [troubleshooting-tls.md](troubleshooting-tls.md)
- [nginx-on-443.md](nginx-on-443.md) · [dns-basnas-setup.md](dns-basnas-setup.md) · [examples.md](examples.md)

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
    - Basnas Ssh
      - [BasNAS SSH (docker and git)](../basnas-ssh/SKILL.md)
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
