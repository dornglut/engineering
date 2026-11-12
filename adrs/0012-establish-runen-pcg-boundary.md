# ADR 0012: Establish RunenPCG as standalone procedural-generation framework authority

- Status: accepted
- Date: 2026-11-12
- Owner: Dornglut organization
- Scope: Runen-family procedural-generation ownership and dependency boundary

## Context

Runenwerk has a domain-owned procedural cave-topology generator. Chimera Signal
requires reproducible Site generation but independently owns Site grammar and
physical realization. Neither application nor a Bevy or Runenwerk plugin is an
appropriate owner for reusable generation algorithms.

[RunenGraph](0010-establish-runen-graph-boundary.md) owns graph relationship
semantics, not the purpose or policy of generating a graph. Sharing graph-shaped
outputs does not transfer application source or establish a common runtime.

## Decision

Establish `dornglut/runen-pcg` as the standalone Runen-family Rust framework
authority for reusable, engine-independent procedural-generation algorithms and
their capability-specific contracts.

RunenPCG may own explicit generation inputs, deterministic algorithm versions,
bounded computation, candidate structure, verifiable results, and typed failures
when justified by accepted repository-local work.

It does **not** own:

- RunenGraph identities, relationships, or general graph analysis;
- RunenSpatial addressing or RunenSDF field mathematics;
- application-authored recipes, source provenance, candidate admission, gameplay
  meaning, or accepted world products;
- 3D spatial realization, collision, network authority, execution scheduling,
  persistence, or Bevy/Runenwerk plugin lifecycle.

RunenPCG may consume peer frameworks only for specific proven capabilities.
RunenPCG must not depend on Runenwerk, Chimera Signal, Runen Lab, or their engine
runtimes. Applications may consume RunenPCG through ordinary Rust APIs; optional
engine adapters remain downstream.

The initial RunenPCG repository bootstrap has no generation API. This decision
does not prescribe one generator trait, graph representation, algorithm, crate
split, compatibility format, or universal PCG system.

## Alternatives considered

### Keep all generation inside Runenwerk or Chimera

Rejected as the general ownership target. Independently reusable algorithms
would become tied to consumer lifecycles or be duplicated. Existing domain
implementations remain in place until a separately accepted transfer.

### Extend RunenGraph with procedural generation

Rejected. Graph structure and analysis have distinct invariants from algorithm
selection, generation budgets, randomization, and result qualification.

### Make a Bevy or Runenwerk plugin the framework

Rejected. Plugins may integrate a generator into an engine but should not make
the algorithm dependent on an application's runtime.

### Require generic ports-and-adapters infrastructure first

Rejected. Narrow pure Rust functions and concrete types are sufficient until
multiple real integrations justify adapter contracts.

## Consequences

- RunenPCG owns independently accepted generation behavior and conformance.
- RunenGraph and other peer libraries retain their separate semantic authorities.
- Runenwerk and Chimera retain their existing domain sources and product admission.
- Seed replay, versioning, resource limits, and consumer compatibility must be
  proved for each accepted generation capability, not implied by this ADR.
- Future source movement follows [ADR 0008](0008-adopt-bounded-source-authority-handoffs.md).
  Duplicate implementations must not survive an accepted handoff.

## Affected repositories

- `dornglut/engineering`: cross-repository architecture.
- `dornglut/runen-pcg`: standalone repository-local generation authority.
- `dornglut/runen-graph`, `dornglut/runen-spatial`, and `dornglut/runen-sdf`:
  independent peer authorities, unchanged.
- `dornglut/runenwerk` and `dornglut/chimera-signal`: potential consumers,
  without automatic adoption or source changes.

## Adoption or migration

Accept this ADR and reconcile the Runen-family map. Complete RunenPCG bootstrap
through its protected repository workflow. Introduce generator behavior only in
separately accepted RunenPCG work. Source transfer and consumer adoption require
independent owning issues, compatibility evidence, and validation. There is no
source migration in this decision.

## Supersedes

None.

## Superseded by

None.
