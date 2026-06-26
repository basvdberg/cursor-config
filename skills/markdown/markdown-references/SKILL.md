---
name: markdown-references
description: >-
  Authors a ## References section listing sources used to build a document
  (standards, RFCs, books, normative upstream patterns), in bibliographic form
  with an optional usage note. Use when adding or editing references, Used
  references, citations, or bibliography blocks in markdown documentation.
---

# Markdown references

## Goal

A **References** section lists **sources that informed the document** — not sibling patterns, implementation guides, or downstream consumers of the ideas.

Cross-link related patterns in the body (Purpose, Recommendations) when the relationship matters. Put only **normative inputs** and **external standards** in References.

**Direction rule:** If pattern A defines metrics and pattern B implements them, B may cite A as a reference; A does not cite B.

## Placement

- Section title: `## References` (not "Used references").
- Place after the last body section, before `## Project structure`.
- Regenerate TOC after adding or editing (`markdown-toc` skill).

## Entry format

Use **bibliographic notation** first; add a short usage note after an em dash.

```markdown
## References

- Author, A. A., & Author, B. B. (Year). *Title*. Publisher. https://… — How this source was used.

- Organisation. (Year). *Standard or specification* (version). https://… — How this source was used.
```

### Source types (prefer in this order)

| Type | Format |
|------|--------|
| **RFC / IETF** | Author(s). (Year). *RFC ####: Title*. Internet Engineering Task Force. URL |
| **Standard / spec** | Organisation. (Year). *Title* (version). URL |
| **Book** | Author, A. (Year). *Title*. Publisher. ISBN |
| **Web documentation** | Organisation. (Year or n.d.). *Page title*. URL |
| **Normative design pattern** | Data Engineering Design Patterns. (Year). *Pattern title* [Design pattern]. URL — only when this document directly implements or extends that pattern's definitions |

### Usage note

- One sentence: which definitions, dimensions, or vocabulary came from the source.
- Start with an em dash (`—`), not a second sentence in the citation line.
- Do not repeat the full definition from the body.

## Include

- Standards and specifications (ODCS, ITIL, ISO, W3C, etc.).
- RFCs and formal internet standards.
- Books and papers that shaped terminology.
- An upstream pattern in the same catalogue when this document **implements** its definitions (one direction only).

## Exclude

- Sibling patterns that **apply** or **extend** this document's ideas.
- Implementation folders (`implementation/`), tool-choice docs, or PoC repos unless they were the primary source for definitions.
- The project's own output (e.g. do not cite a LinkedIn post as a source for the pattern it describes).

## Examples

**Quality-of-service pattern** (defines metrics; cites external sources only):

```markdown
## References

- Nichols, K., Blake, S., Baker, F., & Black, D. (1998). *RFC 2475: An Architecture for Differentiated Services*. Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc2475 — Adapted delivery-quality dimensions (throughput, latency, availability, reliability) for data objects.

- Bitol. (2024). *Open Data Contract Standard v3.1.0: Service level agreement*. Linux Foundation. https://bitol-io.github.io/open-data-contract-standard/v3.1.0/service-level-agreement/ — `slaProperties` vocabulary for freshness, availability, and service-level dimensions.
```

**Refresh contract pattern** (implements QoS; cites QoS + external standards):

```markdown
## References

- Data Engineering Design Patterns. (2026). *Data object quality of service* [Design pattern]. https://github.com/basvdberg/data-engineering-design-patterns/blob/main/design-patterns/data-engineering/data-object-quality-of-service.md — Defines `Frequency`, `Latency`, availability, and service-level metrics the contract must meet.

- Bitol. (2024). *Open Data Contract Standard v3.1.0: Service level agreement*. Linux Foundation. https://bitol-io.github.io/open-data-contract-standard/v3.1.0/service-level-agreement/ — `ConsumerPromise` maps to `slaProperties` (`latency`, `frequency`, `timeOfAvailability`).
```

## Workflow

1. List every definition or vocabulary term borrowed from outside the document.
2. Find the authoritative source (RFC, standard, book) — not a blog summary unless no standard exists.
3. Write bibliographic line + usage note for each source.
4. Remove sibling patterns unless this document normatively implements them.
5. Regenerate TOC; run `review_markdown.py` on the file.

## Related skills

`markdown-toc`, `review-markdown-structure`, `create-design-pattern`
