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
├── runen-spatial
├── runen-net
├── runen-online
├── werkstatt
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
| `dornglut/runenwerk` | Integration platform and reference engine | Current integration authority; downstream of adopted standalone frameworks |
| `dornglut/runen-ui` | Host-neutral UI framework | Standalone; adoption remains repository-owned |
| `dornglut/runen-sdf` | Signed-distance-field framework | Standalone; Runenwerk duplicate-source retirement is complete |
| `dornglut/runen-spatial` | Host-neutral spatial mechanics framework | Standalone; Runenwerk cutover remains separately owned |
| `dornglut/runen-net` | Host- and transport-independent realtime multiplayer networking framework | Standalone; Runenwerk is a downstream consumer, and RunenOnline does not redefine its semantics |
| `dornglut/runen-online` | Provider-neutral online-game control-plane framework | Standalone sibling of RunenNet; game/server applications may compose both through explicit integration |
| `dornglut/werkstatt` | Human-first engineering-workbench application and bounded product pilot | Application boundary; product adoption is not required by other repositories |

The durable RunenNet/RunenOnline ownership and composition boundary is defined by
[ADR 0006](../adrs/0006-separate-realtime-networking-from-online-control-plane.md).

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

RunenNet ─────┐
RunenOnline ──┼──> consumer game/server applications
              └──> Runenwerk integration when adopted

standalone frameworks
    -> Runenwerk integration
```

The diagram records intended dependency direction, not current package adoption.
RunenNet and RunenOnline are sibling standalone frameworks: neither depends on the
other merely to define its semantic core. A consumer may depend on both and explicitly
map their distinct identity and lifecycle domains.

RunenSDF is the standalone authority for reusable signed-field mathematics. Current
accepted Runenwerk source contains no tracked `domain/sdf` package, workspace member,
or duplicate implementation; Runenwerk retains only product/world integration.
RunenGPU, RunenRender, and RunenECS remain planned standalone repositories, not
implemented external frameworks.

A planned repository name does not authorize source movement. Each extraction requires:

1. boundary correction in the current owner;
2. one accepted transferred implementation;
3. standalone validation and downstream conformance;
4. real consumer migration;
5. old-source and workspace-authority deletion;
6. proof that no forwarding package, alias, include, branch dependency, submodule, or duplicate implementation remains;
7. provenance and release-policy closure.

Cross-repository sequencing belongs in owning issues, the Engineering Portfolio, and a qualifying initiative when necessary.
