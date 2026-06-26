---
name: create-design-pattern
description: >-
  Creates compact, technology-agnostic design pattern markdown in
  data-engineering-design-patterns/design-patterns/. Use when adding or
  rewriting a pattern in Data Engineering Design Patterns.
---

# Create design pattern

## Target

- Repo: `data-engineering-design-patterns/`
- Path: `design-patterns/{data-engineering|generic}/{kebab-case}.md`
- Title: `#` sentence case; filename kebab-case
- Naming rule: never include the words `design pattern` in the pattern name, title, or filename.

## Style

- **Short and simple** — shortest correct text; one idea per sentence; cut filler and repetition.
- **Positive scope only** — describe what the pattern *is* and *does*. Do not state what it does *not* do. 
- **Generic** — no vendors, products, or solution-specific names in examples.
- **Declarative** — entities and constraints (*what*), not build steps (*how*).
- **Compact** — short sections; do not repeat the summary in every component.
- **Entities** — `` `EntityName` `` on first mention per component.
- **Examples** — at most two neutral bullets per component, only when they clarify.
- **Define once** — define each term in Components (or Dimensions); examples apply those names in prose and tables only. Do not add `Notes` glossaries or `**Term** is …` bullets that restate definitions. Use existing column names (`Frequency`, `Latency`); add example-only columns (`Ready at`) when the value is scenario-specific, not a new dimension.
- **Use-case prose** — follow `create-use-case` skill. One short lead-in per scenario, then the contract JSON. Prose states constraints, dependencies, and choices the JSON does not show. Do not echo field values or enums already in the example (`refreshScope`, `mode`, `schedule`, and similar). Explain *why* a value was chosen only when the reason is not visible in the contract (e.g. no change data capture → `full`).
- **Cross-links** — only to other patterns when the relationship matters (one line).

No `implementation/` content in pattern files.

## Apply generic patterns

When creating or modifying any design pattern, always apply the generic patterns in `design-patterns/generic/` as guiding principles:

- `simplicity.md` — choose the simpler correct design; keep the system boundary small; remove non-essential parts.
- `separate-what-and-how.md` — keep the declarative specification separate from the imperative implementation; one specification, many implementations.
- `functional-decomposition.md` — decompose by responsibility; generalize repeated behavior; express variation in configuration.
- `prefer-simple-decomposition.md` — compatibility entry point for the two patterns above.

These shape both the pattern's content (the design it describes) and its structure (favor the fewest, clearest components). Cross-link to a generic pattern only when the relationship matters.

## Rewrites

When the user edits a pattern file and asks for a rewrite or review:

- Treat their wording, entity names, section structure, and concepts as intentional — **keep** them unless they ask to change them.
- Improve spelling, structure, TOC/structure blocks, and brevity **around** their concepts; do not “restore” an older version of ideas they replaced.

## Sections

| Sections | Guidance |
|---------|----------|
| Purpose | Problem + pattern intent (≤2 short paragraphs). |
| Benefits | 3–5 one-line bullets. |
| Summary | One paragraph; core idea only. |
| Components | 4–8 `###` subsections; 1–2 sentences each. Optional numbered flow as last subsection (≤5 steps). |
| Use cases | Optional; numbered scenarios per `create-use-case` skill. Each use case = distinct viewpoint; full set covers the domain. |
| Rules | Optional; 3–6 short `###` rules stating required behavior (not out-of-scope disclaimers). Omit for catalog-only patterns. |
| References | Optional; sources that informed definitions (`markdown-references` skill). Place before Project structure. |

Skip: Definitions, Assumptions, Processes unless essential.

## Workflow

1. Draft from [TEMPLATE.md](TEMPLATE.md).
2. Regenerate (repo root):

```bash
python ../cursor-config/scripts/update_markdown_docs.py --toc-only design-patterns/{stem}.md
python ../cursor-config/scripts/update_markdown_docs.py --structure-only
python ../cursor-config/scripts/review_markdown.py design-patterns/{stem}.md
```

3. Fix review **errors**; do not hand-edit TOC/structure markers.
4. Fix review **warnings** for redundant example glossaries (`Notes` blocks or `**Term** is …` bullets that repeat Component definitions).
5. After editing use cases, apply `create-use-case` (coverage map, numbered viewpoints, lead-in review).

## Related skills

`create-use-case`, `markdown-toc`, `markdown-project-structure`, `review-markdown-structure`, `markdown-references`
