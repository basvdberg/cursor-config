---
name: create-use-case
description: >-
  Authors numbered, domain-covering use cases that explore a subject through
  concrete real-world scenarios and feed functional requirements. Use when
  adding or rewriting use cases in design patterns, specs, or documentation,
  or when the user asks for use case coverage, scenarios, or requirements from
  examples.
---

# Create use case

## Purpose

The purpose of a use case is to describe and explore the domain by giving concrete examples of all possibilities. This means that each use case should preferably define a completely different viewpoint. The total set of all use cases should cover the domain. A use case should be simple and practical and describe real-world scenarios. Use cases are a source for defining the functional requirements. They do this by describing all possible scenarios.

## When to apply

- Adding or rewriting a `## Use cases` section in a design pattern or spec.
- Checking whether existing scenarios cover the domain.
- Deriving functional requirements from documented examples.
- Reviewing use-case prose for redundancy or missing viewpoints.

Apply [Simplicity](https://github.com/basvdberg/data-engineering-design-patterns/blob/main/design-patterns/generic/simplicity.md): shortest correct text; remove sentences that add no information beyond the example.

## Domain coverage

Before writing, list the domain dimensions (entities, triggers, modes, scopes, constraints) from the parent document's Components or equivalent section.

| Rule | Guidance |
|------|----------|
| **Distinct viewpoint** | Each use case explores a different combination of dimensions — not a minor variation of the previous one. |
| **Full coverage** | Together, all use cases should exercise every important dimension at least once. |
| **No gaps** | If a dimension has enumerated values (`full` / `partition` / `subset`, `direct` / `snapshot`, …), at least one use case should show each value that matters in practice. |
| **Real-world** | Name concrete situations operators and consumers recognize (late arrival, upstream out of sync, combined triggers). |
| **Requirements source** | Each scenario should be specific enough that a reader can infer what the system must do without a separate requirements list repeating the same facts. |

When two use cases would overlap, merge them or split so each owns a clearly different viewpoint.

## Structure

```markdown
## Use cases

{Optional diagram when relationships help — keep one per section.}

### 1. {Short title — primary viewpoint}

{Lead-in prose — see below.}

{Concrete example — JSON contract, table, or code block.}

### 2. {Short title — different viewpoint}
...
```

- **Number** use cases (`### 1.`, `### 2.`, …).
- **Title** — names the viewpoint (trigger type, dependency shape, failure mode), not only the object id.
- **One primary example** per use case unless the scenario inherently involves multiple objects (e.g. a chain).

Regenerate TOC after renumbering:

```bash
python ../cursor-config/scripts/update_markdown_docs.py --toc-only path/to/file.md
```

## Lead-in prose

One short paragraph before each example. State what the example does **not** already show.

| Include | Omit |
|---------|------|
| Trigger or dependency context | Field values already in the example (`refreshScope`, `mode`, `schedule`, …) |
| Access path or consumer constraint | Component definitions repeated from earlier sections |
| Scope rationale when not visible in the example (e.g. no change data capture → full dataset) | Filler that narrates the obvious |
| Agreed time windows and calendar rules | Duplicate labels from the JSON keys |

**Parallel scenarios** — when use case 2 follows the same shape as use case 1 (e.g. same object family), keep the same lead-in elements in the same order: trigger → access mode → data scope rationale → extract or processing window.

## Workflow

1. **Inventory** — list dimensions and values from Components (or domain model).
2. **Coverage map** — draft a small matrix: use case number × dimensions each scenario will demonstrate. Resolve gaps before writing prose.
3. **Draft** — write numbered use cases; one viewpoint each; lead-in + concrete example.
4. **Review coverage** — every row in the matrix filled? Any duplicate viewpoints to merge or differentiate?
5. **Review prose** — remove sentences that only restate the example; keep non-obvious constraints and rationales.
6. **Derive requirements** — optionally list functional requirements implied by the set (only where not already captured elsewhere).

## Checklist

- [ ] Each use case has a clearly different viewpoint.
- [ ] The full set covers the domain dimensions that matter in practice.
- [ ] Scenarios are simple, practical, and real-world.
- [ ] Use cases are numbered; TOC updated.
- [ ] Lead-in prose adds information the example does not carry.
- [ ] No redundant restatement of example field values.
- [ ] Parallel use cases share the same lead-in structure where applicable.

## Related skills

- `create-design-pattern` — pattern files with `## Use cases` sections.
- `markdown-toc` — TOC after renumbering.
- `review-markdown-structure` — define-once and use-case prose rules in design patterns.
