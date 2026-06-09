---
name: variable-naming
description: >-
  Names variables, environment keys, and config settings after the semantics of
  their value, not the component or feature that consumes them. Use when adding
  or renaming Airflow Variables, .env keys, app settings, Terraform variables,
  or when reviewing configuration for maintainability.
---

# Variable naming

## Principle

A variable should be named to show the **semantics of its value**, not its **intended use**.

When someone browses variables (Airflow Admin, `.env`, config UI), the name alone should answer: *what does this value represent?* Who reads it and why is **documentation or code**, not the variable name.

**Why:** Values change for their own reasons (new Kafka host, rotated password, new data object id). Usage-based names hide what to update and invite duplicate vars (`poller_kafka_host`, `extractor_kafka_host`) for the same endpoint.

## Core rule

| Name for | Not for |
|----------|---------|
| What the value **is** (host, port, id, mode, URL, DSN) | Which service **uses** it (poller, DAG, extractor) |
| The **dimension** being configured | The **workflow step** it enables |

Document consumers in README, implementation plan, or inline where the variable is read — not in the identifier.

## Naming patterns

### Infrastructure endpoints

Name after the **system** and **facet** of the value:

| Value | Good | Avoid |
|-------|------|-------|
| Kafka broker `kafka:9092` | `kafka_host`, `kafka_bootstrap_servers` | `poller_kafka`, `event_publish_broker` |
| Postgres DSN host | `postgres_host` | `poller_db_host`, `metadata_store_for_probe` |
| Airflow REST base URL | `airflow_api_url` | `trigger_extract_url`, `controller_airflow` |

If the hostname changes, operators should find **`kafka_host`** (or equivalent) immediately — not hunt for a poller-specific alias.

### Identifiers and resource keys

| Value | Good | Avoid |
|-------|------|-------|
| Data object id string | `data_object_id` | `poller_mapping_selector` (when value is only an id) |
| Database name | `data_solution_db` | `poller_postgres_database` |

Use a scope prefix only when the **same kind of value** legitimately differs by context (`staging_postgres_host` vs `prod_postgres_host`), not because one consumer is the poller.

### Modes, enums, and feature flags

Name the **setting** (transport, backend, log level), not the only current consumer:

| Value | Good | Avoid |
|-------|------|-------|
| `none` \| `stdout` \| `kafka` | `publish_transport`, `event_publish_transport` | `poller_publish` (encodes one consumer) |
| `postgres` \| `file` | `state_backend` | `poller_state_backend` (unless two backends exist at different keys) |

When a single component owns the setting and no sharing is planned, a short value-semantic name is still preferred over `component_action`.

### Secrets

Same rule: name the **credential or secret**, not the reader.

| Good | Avoid |
|------|-------|
| `postgres_password`, `airflow_admin_password` | `poller_db_secret`, `dag_login_password` |

## Syntax by context

Align with the surrounding ecosystem; do not invent a new style per repo.

| Context | Convention | Example |
|---------|--------------|---------|
| Environment / `.env` | `SCREAMING_SNAKE_CASE` | `KAFKA_HOST` |
| Airflow Variables | `snake_case` (value-semantic) | `kafka_host` |
| Python | `snake_case` | `kafka_bootstrap_servers` |
| Terraform | `snake_case` | `kafka_bootstrap_servers` |

For file and folder path naming, see `naming-convention-files-folders`.

## Airflow Variables vs environment

- **Shared infrastructure** (Kafka host, Postgres host): one name everywhere — env `KAFKA_HOST` and Variable `kafka_host` if both exist; same semantics.
- **Behavior toggles** (publish transport): Variable or env, named for the value domain (`publish_transport`), default documented next to the DAG or module that reads it.
- **Do not** encode DAG id, task id, or job name in the variable unless the value is literally that id and shared nowhere else.

## Agent workflow

1. **Identify the value type** — host, port, id, enum, secret, URL, path.
2. **Propose a name from the value** — strip consumer prefixes (`poller_`, `extractor_`, `dag_`) unless disambiguating two values of the same type.
3. **Check for an existing var** — reuse `kafka_host` instead of adding `poller_kafka_host`.
4. **Document usage** — one line in config readme or implementation plan: which modules read the variable; not in the name.
5. **Rename in one change** — update readers, `.env.example`, deploy docs, and Airflow UI together.

## Examples

### Kafka host (from conversation)

**Wrong:** store broker address in a name that describes poller behavior (`poller_publish` is not a hostname; `poller_kafka_endpoint` ties the host to one consumer).

**Right:**

```text
# .env
KAFKA_HOST=kafka:9092

# Airflow Variable (if used)
kafka_host = kafka:9092
```

Poller, event controller, and future consumers all read `KAFKA_HOST` / `kafka_host`. Usage is documented in the orchestration plan.

### Publish transport

**Value:** `none`, `stdout`, or `kafka` — the event **transport**, not “poller”.

**Prefer:** `publish_transport` or `event_publish_transport`.

**Document:** “Open-Meteo poller DAG reads `publish_transport` via `Variable.get`.”

### Data object selection

**Value:** `source/openmeteo/daily-temperature` — a **data object id**.

**Good:** `data_object_id` (or `poller_data_object_id` only if another `data_object_id` already exists for a different purpose in the same scope).

## Anti-patterns

- **Consumer + action:** `poller_publish`, `extractor_trigger_flag` when the value is not poller- or extractor-specific.
- **Workflow in the name:** `step2_kafka_bootstrap`, `on_change_notify_host`.
- **Duplicate endpoints:** `kafka_host` and `poller_kafka_host` with the same value.
- **Mystery abbreviations:** `k_h`, `pub_mode` without a documented value domain.

## Related skills

- `naming-convention-files-folders` — paths and filenames (kebab-case, singular)
- `create-skill` — authoring shared skills in cursor-config
