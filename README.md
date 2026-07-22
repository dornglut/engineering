# Dornglut Engineering

This repository is the durable authority for Dornglut-wide engineering policy, cross-repository architecture, and organization-level decisions.

It does not own product implementation. Each product repository retains authority over its code, tests, public API, validation semantics, releases, and local roadmap.

## Structure

- [governance](governance/) — authority, repository lifecycle, and decision policy
- [architecture](architecture/) — cross-repository system boundaries
- [adrs](adrs/) — accepted organization-level decisions
- [initiatives](initiatives/) — cross-repository outcomes with bounded ownership
- [portfolio](portfolio/) — relationship between durable documents and live GitHub Projects
- [reports](reports/) — dated evidence and reviews that do not become permanent policy
- [templates](templates/) — starting points for decisions and initiatives

Canonical validation:

```text
python scripts/validate.py
```
