# Runen family

This document defines Dornglut's cross-repository system boundary. Repository-local architecture remains owned by each repository.

## Repository system

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

## Organization repositories

| Repository | Role | Must not own |
|---|---|---|
| `dornglut/.github` | Inherited community-health defaults, public profile, issue and workflow templates | Product behavior, product roadmaps, validation semantics |
| `dornglut/engineering` | Organization governance, standards, cross-repository architecture, ADRs, qualifying initiatives, dated audits | Product implementation, copied live state |
| `dornglut/github-workflows` | Reusable read-only CI orchestration | Product validation semantics, source authorship, releases |

## Current product and framework repositories

| Repository | Role | Current relationship |
|---|---|---|
| `dornglut/runenwerk` | Integration platform and reference engine | Current integration authority |
| `dornglut/runen-ui` | Host-neutral UI framework | Standalone; adoption remains repository-owned |
| `dornglut/runen-sdf` | Signed-distance-field framework | Standalone; Runenwerk duplicate-source retirement remains the consumer cutover gate |

## Planned repositories

| Repository | Intended role | Dependency direction |
|---|---|---|
| `dornglut/runen-gpu` | GPU resource, execution, and device abstraction | Lower-level dependency |
| `dornglut/runen-render` | Rendering framework built on RunenGPU | Depends on RunenGPU |
| `dornglut/runen-ecs` | Standalone ECS framework | Independent extraction after higher-priority boundaries stabilize |

## Dependency and extraction rule

The intended direction is:

```text
RunenSDF
RunenGPU
    -> RunenRender

RunenECS
RunenUI

standalone frameworks
    -> Runenwerk integration
```

The diagram records intended dependency direction, not current package adoption.

A planned repository name does not authorize source movement. Each extraction requires:

1. boundary correction in the current owner;
2. one accepted transferred implementation;
3. standalone validation and downstream conformance;
4. real consumer migration;
5. old-source and workspace-authority deletion;
6. proof that no forwarding package, alias, include, branch dependency, submodule, or duplicate implementation remains;
7. provenance and release-policy closure.

Cross-repository sequencing belongs in owning issues, the Engineering Portfolio, and a qualifying initiative when necessary.
