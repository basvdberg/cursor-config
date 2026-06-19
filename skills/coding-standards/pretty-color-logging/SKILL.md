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
