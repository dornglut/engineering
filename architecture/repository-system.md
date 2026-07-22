# Repository system

```text
dornglut
├── .github
├── engineering
├── github-workflows
├── runenwerk
├── runen-ui
├── runen-sdf
├── runen-gpu       planned
├── runen-render    planned
└── runen-ecs       planned
```

## Organizational repositories

`dornglut/.github` owns inherited community-health files, issue forms, pull-request guidance, and the public organization profile.

`dornglut/engineering` owns cross-repository policy, architecture, initiatives, and ADRs.

`dornglut/github-workflows` owns reusable CI orchestration. It calls repository-owned validation commands and does not own product validation semantics.

## Product repositories

Product and framework repositories own implementation, tests, public contracts, local decisions, local issues, release policy, and compatibility.

The stable operating rule is:

> Centralize policy, planning structure, shared architecture, and automation; localize code ownership, validation semantics, releases, and implementation decisions.
