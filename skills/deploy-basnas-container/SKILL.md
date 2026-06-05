## Table of contents

<!-- markdown-toc:start -->
- [Dual DNS zones](#dual-dns-zones)
- [Non-negotiable rules](#non-negotiable-rules)
- [BasNAS layout](#basnas-layout)
- [Workflow](#workflow)
  - [Step 6: NGINX templates](#step-6-nginx-templates)
  - [Step 7: LAN DNS](#step-7-lan-dns)
  - [Step 8: Internal CA (required for .basnas)](#step-8-internal-ca-required-for-basnas)
- [Agent deliverables](#agent-deliverables)
  - [Step 9: Browser bookmarks (Floccus)](#step-9-browser-bookmarks-floccus)
- [Additional resources](#additional-resources)
<!-- markdown-toc:end -->

---
name: deploy-basnas-container
description: >-
  Design and deploy Docker services on BasNAS with fixed host ports, NGINX
  HTTPS termination, dual DNS (office.c2h.nl public, basnas internal), NAS share
  mounts, and a public-exposure registry. Use when deploying containers on BasNAS,
  QNAP, office.c2h.nl, application.basnas internal hostnames, NGINX reverse proxy,
  or exposing services to the internet. For data-solution-2026 app/DAG/poller
  releases, use deploy-data-solution-basnas (commit and push to main)—not manual
  SSH git pull.
---

# Deploy container service on BasNAS

BasNAS is a **QNAP** running **Container Station**. **NGINX runs in Docker** on the QNAP and is the HTTPS edge for all app containers.

**Service inventory:** [basnas-inventory.yaml](basnas-inventory.yaml). **URL map:** [service-url-map.yaml](service-url-map.yaml) / [url-map.md](url-map.md).

## Dual DNS zones

| Zone | URL pattern | Public DNS | Use for |
|------|-------------|------------|---------|
| **office** (existing) | `https://<application>.office.c2h.nl/` | **Yes** → WAN → NGINX | `expose: public` only |
| **basnas** (default) | `https://<application>.basnas/` | **No** — LAN/VPN only | `expose: internal` (default) |

NGINX uses separate TLS certs: `ssl/office.c2h.nl/` (Let's Encrypt) and `ssl/basnas/` (**internal CA**, wildcard `*.basnas`). Never publish `*.basnas` on public DNS.

**QTS admin:** `https://admin.basnas/` (not `basnas.basnas` — conflicts with QNAP short hostname `basnas`).

## Data Solution 2026 (app deploy via CI/CD)

**Do not** deploy `data-solution-2026` application code by SSH `git pull` or `deploy-on-nas.sh` as the default step after making changes.

| Change type | How to deploy |
|-------------|----------------|
| Code, DAGs, poller, extractor, metadata in repo | **Commit and push to `main`** → CI/CD → post-push deploys NAS ([deploy-data-solution-basnas](../deploy-data-solution-basnas/SKILL.md)) |
| `infra/` compose or `.env` on NAS | After push, `RUN_INFRA_SYNC=1` on NAS (see that skill) |
| New HTTPS vhost, port, or NGINX upstream | This skill (registry + templates below) |

Airflow/Kafka/Postgres URLs: `https://airflow.basnas/`, `https://kafka.basnas/` (inventory in [basnas-inventory.yaml](basnas-inventory.yaml)).

## Non-negotiable rules

1. **Fixed ports** — Register in `port-registry.yaml`; prefer Docker network + service name, no host publish.
2. **HTTPS via NGINX** — No TLS in app containers ([reference.md](reference.md#nginx-on-qnap-docker)).
3. **DNS by exposure** — `internal` → `https://<application>.basnas/`; `public` → `https://<application>.office.c2h.nl/`.
4. **Public exposure** — Only `expose: public` on `office.c2h.nl`. Default `internal` + `.basnas` only.
5. **Network share** — Bind-mount from NAS share per app.

## BasNAS layout

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
      basnas/           # internal zone (internal CA, *.basnas)
  shares/<application>/
```

## Workflow

```text
- [ ] 1. Choose <application> and container_port
- [ ] 2. Allocate host_port in port-registry.yaml (if needed)
- [ ] 3. public-exposure.yaml (expose + url https://<application>.basnas/)
- [ ] 4. Create NAS share
- [ ] 5. docker-compose.yml
- [ ] 6. nginx vhost from templates/nginx-app-basnas.conf
- [ ] 7. LAN DNS: *.basnas → BasNAS LAN IP (never on public DNS)
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

**Bulk deploy** all `https_basnas` services: copy [scripts/deploy-all-basnas-vhosts.sh](scripts/deploy-all-basnas-vhosts.sh) to BasNAS, `sed -i 's/\r$//'`, run it, then `scripts/patch-bridge-upstreams.sh` if radarr/nzbget upstreams change after container recreate.

**Windows TLS name check:** use explicit SANs per hostname (not only `*.basnas`). After adding apps, run [scripts/reissue-basnas-cert.sh](scripts/reissue-basnas-cert.sh) on BasNAS.

### Step 7: LAN DNS

```text
*.basnas  A  192.168.2.2
```

Or per-app records. **AdGuard** on QNAP (planned) can serve this zone.

### Step 8: Internal CA (required for `.basnas`)

Let's Encrypt does **not** issue for `.basnas`. Issue wildcard `*.basnas`, mount to NGINX, install CA root on client devices once. See [nginx-on-443.md](nginx-on-443.md).

## Agent deliverables

1. Registry snippets with `url: https://<application>.basnas/`
2. `docker-compose.yml`
3. NGINX vhost (`<application>.basnas`)
4. LAN DNS note (`*.basnas` only)
5. If `public`: `office.c2h.nl` + public DNS
6. Run bookmark sync: `cursor-config/scripts/sync_browser_bookmarks.py --basnas` (see [browser-bookmarks-sync](../browser-bookmarks-sync/SKILL.md))

### Step 9: Browser bookmarks (Floccus)

After `service-url-map.yaml` has the canonical `url`, refresh the **BasNAS** folder in [browser-bookmarks-sync](https://github.com/basvdberg/browser-bookmarks-sync):

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
  - [Deploy Data Solution 2026 to BasNAS (CI/CD)](../deploy-data-solution-basnas/SKILL.md)
<!-- markdown-project-structure:end -->
