# Runen family

This document defines Dornglut's cross-repository system boundary. Repository-local architecture remains owned by each repository.

## Repository system

```text
dornglut
├── .github
├── engineering
├── github-workflows
├── runen
├── runenwerk
├── runen-lab
├── runen-ui
├── runen-sdf
├── runen-spatial
├── runen-net
├── runen-online
├── werkstatt
├── runen-gpu
├── runen-ecs
├── runen-shader
├── runen-graph
├── runen-input
└── runen-render
```

## Organization repositories

| Repository | Role | Must not own |
|---|---|---|
| `dornglut/.github` | Inherited community-health defaults, public profile, issue and workflow templates | Product behavior, product roadmaps, validation semantics |
| `dornglut/engineering` | Organization governance, standards, cross-repository architecture, ADRs, qualifying initiatives, dated audits | Product implementation, copied live state |
| `dornglut/github-workflows` | Reusable read-only CI orchestration | Product validation semantics, source authorship, releases |

## Current product, language, and framework repositories

| Repository | Role | Current relationship |
|---|---|---|
| `dornglut/runen` | Runen programming-language specification, compiler, reference, and proving work | Independent language authority; consumers do not define Runen semantics implicitly |
| `dornglut/runenwerk` | Integration platform and reference engine | Current integration authority; downstream of adopted standalone frameworks |
| `dornglut/runen-lab` | Downstream experimental and showcase application collection | Consumes accepted public Runen-family surfaces or Runenwerk; owns no framework semantics or cross-framework integration authority |
| `dornglut/runen-ui` | Host-neutral UI framework | Standalone; adoption remains repository-owned |
| `dornglut/runen-sdf` | Signed-distance-field framework | Standalone; Runenwerk duplicate-source retirement is complete |
| `dornglut/runen-spatial` | Host-neutral spatial mechanics framework | Standalone; Runenwerk cutover remains separately owned |
| `dornglut/runen-gpu` | Backend-neutral GPU resource, execution, and device framework | Standalone semantic implementation authority; Runenwerk is a downstream integration consumer |
| `dornglut/runen-ecs` | Reusable entity-component-system framework | Standalone semantic implementation and conformance authority; Runenwerk is a downstream integration consumer |
| `dornglut/runen-shader` | Shader-source and shader-toolchain framework producing canonical shader artifacts | Standalone semantic authority; sibling of RunenGPU; concrete frontend implementation remains repository-owned |
| `dornglut/runen-render` | Reusable semantic rendering and maintained image-formation framework | Standalone semantic and conformance authority; Runenwerk consumes its accepted public contract and owns product integration |
| `dornglut/runen-graph` | Reusable graph and relationship framework over caller-owned identities | Standalone foundational framework authority; adoption remains repository-owned |
| `dornglut/runen-input` | Host/backend-neutral device-input observation and deterministic confirmed-state framework | Standalone semantic authority; Runenwerk is an exact-pinned downstream integration/product consumer |
| `dornglut/runen-net` | Host- and transport-independent realtime multiplayer networking framework | Standalone; Runenwerk is a downstream consumer, and RunenOnline does not redefine its semantics |
| `dornglut/runen-online` | Provider-neutral online-game control-plane framework | Standalone sibling of RunenNet; game/server applications may compose both through explicit integration |
| `dornglut/werkstatt` | Human-first engineering-workbench application and bounded product pilot | Application boundary; product adoption is not required by other repositories |

The durable RunenNet/RunenOnline ownership and composition boundary is defined by
[ADR 0006](../adrs/0006-separate-realtime-networking-from-online-control-plane.md).

The durable RunenShader/RunenGPU/RunenRender ownership and composition boundary is defined by
[ADR 0009](../adrs/0009-establish-runen-shader-boundary.md). RunenInput ownership and
its completed source-authority handoff direction are defined by
[ADR 0011](../adrs/0011-establish-runen-input-boundary.md).

## Dependency and extraction rule

The intended direction is:

```text
RunenSDF

RunenShader ──┐
RunenGPU ─────┼──> RunenRender
              │
              └──> other explicit consumers may use either or both

RunenECS
RunenUI
RunenInput ──> explicit consumers

RunenGraph ──> explicit consumers

RunenNet ─────┐
RunenOnline ──┼──> consumer game/server applications
              └──> Runenwerk integration when adopted

standalone frameworks
    -> Runenwerk integration

accepted public Runen-family surfaces --+
Runenwerk -------------------------------+-> Runen Lab applications
```

The diagram records intended dependency direction, not current package adoption.
RunenNet and RunenOnline are sibling standalone frameworks: neither depends on the
other merely to define its semantic core. A consumer may depend on both and explicitly
map their distinct identity and lifecycle domains.

RunenShader and RunenGPU are likewise sibling standalone frameworks. RunenShader owns
reusable shader-source and shader-compilation semantics and canonical shader-artifact
formation; RunenGPU owns canonical WGSL program admission and generic GPU execution.
Neither depends on the other merely to define its semantic core. RunenRender depends on
both and owns the explicit artifact-to-program-admission bridge without transferring
either framework's authority.

The Runen language repository remains its own semantic authority. A future consumer
relationship does not transfer language semantics into that consumer. RunenShader does
not acquire Runen language semantics merely because its architecture follows compatible
semantic-design principles.

Runen Lab is downstream only. A Lab application may consume an independently usable
framework directly or consume Runenwerk when it deliberately exercises canonical
engine/product integration. Framework and Runenwerk production packages do not depend
on Runen Lab, and successful Lab behavior does not itself redefine framework semantics,
support claims, or compatibility policy.

RunenSDF is the standalone authority for reusable signed-field mathematics. Current
accepted Runenwerk source contains no tracked `domain/sdf` package, workspace member,
or duplicate implementation; Runenwerk retains only product/world integration.
RunenGPU is the standalone authority for reusable GPU execution semantics after the
completed GX source-authority transfer; Runenwerk consumes the accepted standalone
framework and retains only downstream integration. RunenECS is the standalone authority
for reusable ECS semantics and conformance after its completed source-authority transfer;
Runenwerk consumes the accepted standalone framework and retains only downstream
integration. RunenShader is an active standalone framework with accepted repository-local
source/toolchain semantics, validation authority, and concrete exact-WGSL and bounded
closed-WESL composition realizations; frontend coverage and any further composition
support remain repository-owned.
RunenGraph is a standalone foundational framework authority for reusable graph and
relationship semantics over caller-owned identities. RunenGraph must not depend upward
on RunenECS, RunenUI, Runenwerk, RunenRender, or any future RunenKnowledge repository;
consumer adoption and any explicit integration remain separately owned by the consumer.
RunenInput is the standalone authority for reusable backend-neutral device-input
observation and deterministic confirmed-state semantics after its completed ADR 0008
source-authority handoff. Runenwerk consumes the accepted standalone framework and
retains only integration, backend adaptation, and product projection ownership.
RunenRender is the standalone semantic and conformance authority for reusable renderer
semantics, maintained image formation, and the explicit RunenShader-artifact to RunenGPU
program-admission bridge. Its ADR 0008 successor acceptance and RX cutover are complete.
Runenwerk migrated maintained consumers directly to one exact accepted successor
revision and deleted the transferred predecessor. Runenwerk retains product, frame,
native-host, and render-flow integration. Ordinary standalone RunenRender
evolution is no longer gated by predecessor deletion. Pre-1.0 authority transfer does
not imply a stable API promise.

Broader renderer-maturity evidence such as additional render methods, large-scene
planning or acceleration characterization, GPU-produced semantic inputs,
multi-observation/output sharing, reconstruction evolution, and performance
characterization is not an organization-level reason to keep reusable renderer semantics
owned by Runenwerk after the ownership boundary is otherwise qualified. During ADR
0008's bounded publication overlap, ordinary successor feature evolution waited
until predecessor deletion; only the handoff's permitted cutover-blocking corrections
could change the transferred boundary. After the completed cutover, further
renderer-maturity work belongs to standalone RunenRender unless a repository-local
accepted decision proves a specific item was necessary to determine the transfer
boundary itself.

A repository target does not authorize source movement. Each extraction requires:

1. boundary correction in the current owner;
2. one accepted transferred implementation;
3. standalone validation and downstream conformance;
4. real consumer migration;
5. old-source and workspace-authority deletion;
6. proof that no forwarding package, alias, include, branch dependency, submodule, or duplicate implementation remains;
7. provenance and release-policy closure.

Cross-repository sequencing belongs in owning issues, the Engineering Portfolio, and a qualifying initiative when necessary.
