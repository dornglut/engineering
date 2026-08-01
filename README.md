# Dornglut Engineering

This repository is the durable authority for Dornglut-wide engineering policy, cross-repository architecture, organization standards, initiatives, and decisions.

It does not own product implementation. Each product or framework repository retains authority over its code, tests, public contracts, validation semantics, releases, local architecture, roadmap, and issues.

## Authority entrypoints

- [Authority and work](governance/authority-and-work.md) — where ideas, accepted work, priorities, decisions, and evidence belong
- [Repository standard](standards/repositories.md) — repository profiles, lifecycle, root documentation, and extraction rules
- [GitHub standard](standards/github.md) — organization defaults, intake, contribution modes, Projects, and repository settings
- [Validation standard](standards/validation.md) — repository-owned validation, reusable orchestration, exact-head evidence, and security boundaries
- [Runen family](architecture/runen-family.md) — organization repositories, framework roles, and dependency direction
- [Organization ADRs](adrs/README.md) — durable organization decisions
- [Initiatives](initiatives/README.md) — optional programs that genuinely require cross-repository sequencing and closure evidence
- [Reports](reports/README.md) — dated audits and evidence that do not become policy merely by existing

Canonical validation:

```text
cargo validate
```
