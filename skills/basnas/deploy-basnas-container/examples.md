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
