# ADR 0010: Establish RunenGraph as standalone graph-framework authority

- Status: accepted
- Date: 2026-09-23
- Owner: Dornglut organization
- Scope: Runen-family graph and relationship framework boundary

## Context

Dornglut has no standalone authority for reusable graph and relationship semantics
over identities owned by a caller. Existing graph-shaped systems in Runenwerk or
other repositories have their own product or domain boundaries; their existence does
not establish a shared RunenGraph contract. Treating one of those systems as an
implicit source would transfer authority without an accepted boundary decision.

The Runen family also needs a clear dependency direction for a foundational framework.
RunenGraph must remain usable by explicit consumers without acquiring dependencies on
the consumers whose identities, lifecycle, or integration policy it may represent.

## Decision

Dornglut establishes `dornglut/runen-graph` as a standalone foundational Runen-family
Rust framework authority for reusable graph and relationship semantics over
caller-owned identities.

RunenGraph is greenfield. This decision does not transfer source authority from
Runenwerk's `domain/graph`, and it does not authorize copying, migrating, or deleting
that source. Existing graph-shaped systems are not automatically RunenGraph consumers.

RunenGraph has the following cross-repository boundary:

- explicit consumers may depend on RunenGraph;
- RunenGraph must not depend upward on RunenECS, RunenUI, Runenwerk, RunenRender, or
  any future RunenKnowledge repository;
- no dependency from those repositories to RunenGraph is pre-authorized by this ADR;
- adoption by a consumer requires separate consumer-owned work and acceptance.

This ADR establishes only repository authority, high-level role, and dependency
direction. It does not define graph semantics, public API, identity representation,
storage, algorithms, backend selection, conformance, implementation, or a roadmap.

## Consequences

- RunenGraph owns its future repository-local graph and relationship contract rather
  than inheriting one from Runenwerk or a consumer.
- Consumers must make their identity and integration correspondence explicit when
  they adopt RunenGraph.
- RunenECS, RunenUI, Runenwerk, RunenRender, and future RunenKnowledge remain free to
  evolve under their own authorities until separate adoption work is accepted.
- The RunenGraph repository can be bootstrapped and validated independently before
  any graph behavior or consumer integration is implemented.

## Alternatives considered

### Extract Runenwerk graph source into RunenGraph

Rejected. RunenGraph is greenfield, and source-authority transfer requires a separate
bounded extraction decision, implementation acceptance, consumer migration, and
duplicate-source closure. None of those are authorized here.

### Make RunenGraph a Runenwerk or RunenECS subsystem

Rejected. A reusable relationship framework has a distinct authority boundary from
an integration product or entity-component-system framework. An upward dependency
would couple the foundational authority to a consumer's identity and lifecycle model.

### Pre-authorize all likely Runen-family consumers

Rejected. Consumer adoption is repository-owned work and must establish its own
correspondence, validation, and integration boundary.

## Affected repositories

- `dornglut/engineering`
- `dornglut/runen-graph`
- `dornglut/runenwerk` as historical graph-shaped context only; no source change
- RunenECS, RunenUI, RunenRender, and future RunenKnowledge only as prohibited or
  separately owned dependency directions; no implementation change

## Adoption or migration

1. Accept this ADR and reconcile `architecture/runen-family.md`.
2. Bootstrap `dornglut/runen-graph` as the standalone repository authority through
   its own issue, pull request, and exact-head validation.
3. Define RunenGraph semantics only through separately accepted RunenGraph-owned work.
4. Adopt RunenGraph from any consumer only through separately accepted consumer work.

No source transfer, consumer migration, graph implementation, backend selection, or
dependency addition is authorized by this ADR.

## Supersedes

None.

## Superseded by

None.
