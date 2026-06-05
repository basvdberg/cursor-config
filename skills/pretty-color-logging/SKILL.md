## Table of contents

<!-- markdown-toc:start -->
- [Goal](#goal)
- [Apply This Pattern](#apply-this-pattern)
- [Best Practices](#best-practices)
- [Reference Implementation](#reference-implementation)
- [Validation Checklist](#validation-checklist)
<!-- markdown-toc:end -->

## Table of contents


---
name: pretty-color-logging
description: Standardize Python CLI logging with readable, colorized, structured output. Use when adding or improving logs for scripts, extractors, pollers, workers, and batch jobs that print to terminal.
disable-model-invocation: true
---

# Pretty Color Logging

## Goal

Produce consistent, human-friendly logs where timestamp, level, logger name, and message are easy to scan.

## Apply This Pattern

1. Add a shared logging setup module (do not duplicate formatter logic per CLI).
2. Use a single `configure_logging(verbose=...)` entrypoint called from each CLI `main()`.
3. Render logs in this order:
   - timestamp (with milliseconds)
   - level (fixed width)
   - logger name
   - message
4. Use ANSI colors when attached to a TTY; automatically fall back to plain text when output is redirected.
5. Prefer `log.info(...)`/`log.warning(...)` over `print(...)` for operational status lines.

## Best Practices

- Keep the formatter dependency-light (prefer stdlib `logging` unless the repo already uses a structured logging stack).
- Set log level via `--verbose` (DEBUG when true, INFO otherwise).
- Configure exactly one root handler to avoid duplicate lines.
- Include exception and stack info in formatter output.
- Keep messages concise and include key identifiers (`mapping_id`, marker, path, row count).
- Use parameterized logging (`log.info("rows=%d", rows)`) rather than f-strings.

## Reference Implementation

Use this formatter behavior:

```python
timestamp = "YYYY-MM-DD HH:MM:SS.mmm"
line = f"{timestamp} | {level:<8} | {logger_name} | {message}"
```

Color guidance:
- timestamp: gray/dim
- INFO: green
- WARNING: yellow
- ERROR: red
- CRITICAL: magenta
- message: neutral light color

## Validation Checklist

- [ ] CLI output remains readable when piped to a file (no broken escape clutter in non-TTY mode).
- [ ] `--verbose` increases detail without changing message semantics.
- [ ] No duplicate log lines.
- [ ] Extractor/poller status uses logs instead of prints.

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
      - [Fix admin hostname not resolving](../deploy-basnas-container/dns-basnas-setup.md)
      - [Examples](../deploy-basnas-container/examples.md)
      - [NGINX as HTTPS edge on port 443 (local server / QNAP)](../deploy-basnas-container/nginx-on-443.md)
      - [local server deployment reference](../deploy-basnas-container/reference.md)
      - [Deploy container service on local server](../deploy-basnas-container/SKILL.md)
      - [Troubleshooting “Your connection is not private” (*.example)](../deploy-basnas-container/troubleshooting-tls.md)
      - [local server URL map](../deploy-basnas-container/url-map.md)
    - Markdown Project Structure
      - [Markdown project structure](../markdown-project-structure/SKILL.md)
    - Markdown Toc
      - [Markdown table of contents](../markdown-toc/SKILL.md)
    - Naming Convention Files Folders
      - [Naming convention for files and folders](../naming-convention-files-folders/SKILL.md)
    - Pretty Color Logging
      - [Pretty Color Logging](SKILL.md)
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
