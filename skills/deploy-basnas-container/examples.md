# Examples

## Table of contents

<!-- markdown-toc:start -->
- [QNAP admin (internal zone)](#qnap-admin-internal-zone)
- [Airflow + data-solution](#airflow-data-solution)
- [New Docker app](#new-docker-app)
- [Public app (rare)](#public-app-rare)
<!-- markdown-toc:end -->

## QNAP admin (internal zone)

```yaml
  admin:
    expose: internal
    url: https://admin.example/
```

Use [templates/nginx-admin-qts.conf](templates/nginx-admin-qts.conf). Do not use `https://basnas.example/` — use **admin.example**.

## Airflow + data-solution

```yaml
  airflow:
    expose: internal
    url: https://airflow.example/
    nginx_upstream: airflow-standalone:8080
```

**Application deploy (DAGs, poller, extractor):** commit and push to `main` in [data-solution-2026](https://github.com/basvdberg/data-solution-2026); CI/CD pulls to NAS automatically. See [deploy-data-solution-basnas](../deploy-data-solution-basnas/SKILL.md). Use this skill only for NGINX/upstream/registry changes on the host.

## New Docker app

```yaml
  my-app:
    expose: internal
    url: https://my-app.example/
    nginx_upstream: my-app:8080
```

Copy [templates/nginx-app-basnas.conf](templates/nginx-app-basnas.conf) → `conf.d/my-app.conf`, set `<application>` and `<container_port>`.

## Public app (rare)

```yaml
  status-dashboard:
    expose: public
    url: https://status-dashboard.office.c2h.nl/
```

Use [templates/nginx-app-public.conf](templates/nginx-app-public.conf).

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
