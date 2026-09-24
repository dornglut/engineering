# RunenInput standalone authority cutover

- Status: active
- Owner: Dornglut organization
- Opened: 2026-09-24
- Closed:
- Owning issue: [engineering#82](https://github.com/dornglut/engineering/issues/82)
- Decision authority: [ADR 0011](../adrs/0011-establish-runen-input-boundary.md), [ADR 0008](../adrs/0008-adopt-bounded-source-authority-handoffs.md)

## Outcome

Move reusable backend-neutral device-input observation and deterministic confirmed-state
semantic source authority from Runenwerk into standalone `dornglut/runen-input`, then
cut Runenwerk over to one immutable accepted successor revision and delete the
predecessor reusable implementation without mirrors, forwarding compatibility, moving
dependencies, or duplicate writable authority.

This initiative owns only cross-repository sequencing, rollback/reversal, the ADR 0008
authority handoff, and final coordination closure. Repository-local issues retain
implementation, validation, public-contract, repository-profile, release,
consumer-migration, adapter, and deletion authority.

## Rationale

The accepted Runenwerk I3 decision proves that the reusable input boundary now satisfies
the organization initiative criteria for extraction: the outcome spans Runenwerk and
the standalone RunenInput repository, requires multiple repository-local phases, has an
order-sensitive semantic authority switch, and needs explicit rollback and final
duplicate-authority closure. No repository-local issue can truthfully own both
successor acceptance and predecessor cutover.

## Affected repositories

- `dornglut/engineering` owns this initiative, ADR 0011, family membership, and the
  organization-level ADR 0008 handoff policy.
- `dornglut/runenwerk` owns the predecessor source boundary before the switch,
  pre-transfer correction/census, backend and product integration, downstream consumer
  migration, predecessor deletion, and Runenwerk-side closure.
- `dornglut/runen-input` owns successor repository bootstrap, transferred reusable
  input implementation/public contract, standalone conformance and validation,
  provenance, release policy, and successor acceptance.
- `dornglut/runen-ui` remains a neighboring downstream semantic owner. No RunenUI
  source transfer or adoption change is part of this initiative.

## Dependency graph

```text
accepted Runenwerk I3 extraction decision
    ↓
accepted Engineering ADR 0011 + active RunenInput initiative
    ↓
Runenwerk pre-transfer source-boundary correction + exact transfer census
    ↓
runen-input repository bootstrap/profile reconciliation
    ↓
runen-input repository-local successor transfer authority
    ↓
unmerged standalone successor candidate
    ↓
exact-head standalone validation and successor acceptance
    ↓
accepted runen-input revision becomes sole semantic source authority
    ↓
Runenwerk predecessor neutral-input implementation freezes
    ↓
Runenwerk exact-pin consumer migration + predecessor deletion
    ↓
final no-mirror/no-forwarder/no-moving-dependency proof
    ↓
RunenInput planned → current family reconciliation
    ↓
initiative closure
```

## Acceptance evidence

[runenwerk#771](https://github.com/dornglut/runenwerk/issues/771) owns the completed I3
source/consumer census and the `EXTRACTION_DESIGN_JUSTIFIED` decision.
[runenwerk#774](https://github.com/dornglut/runenwerk/issues/774) owns the completed
pre-transfer source-boundary correction, [engineering#84](https://github.com/dornglut/engineering/issues/84)
owns successor repository bootstrap/profile reconciliation, and
[runen-input#2](https://github.com/dornglut/runen-input/issues/2) owns the active
successor transfer/public-contract acceptance. The future Runenwerk downstream-cutover
issue will own consumer migration and predecessor deletion when created. Pull requests
in each owning repository retain exact-head and accepted-revision evidence.

This charter links those authorities without copying branch heads, workflow runs,
temporary blockers, or child acceptance matrices.

## Sequencing constraints

- Before successor acceptance, Runenwerk remains sole semantic source authority for the
  reusable input implementation.
- The Runenwerk pre-transfer correction may separate successor-worthy neutral semantics
  from legacy `InputState` projections, but must not create a forwarding namespace,
  second writable reducer, or speculative standalone API inside Runenwerk.
- The successor candidate may be prepared and validated on an unmerged branch while
  Runenwerk remains authority; that branch is staging only and may not become dependency
  authority.
- Successor bootstrap must use the current organization `rust-framework` profile and
  perform an exact ownership/source/test census rather than copying Runenwerk's
  integration-product topology by inertia.
- On accepted successor default-branch publication, that immutable accepted revision
  becomes sole semantic source authority immediately and the Runenwerk predecessor
  implementation freezes under ADR 0008.
- During bounded physical overlap, reusable-contract defects are corrected and accepted
  in `runen-input`; Runenwerk repins the corrected accepted revision. The frozen
  predecessor is not patched as an alternate implementation.
- Runenwerk migrates maintained adapters and consumers to an exact immutable accepted
  successor revision or accepted release and deletes predecessor reusable source
  authority in the same downstream cutover boundary.
- Ordinary successor feature evolution for the transferred boundary waits until
  predecessor deletion is accepted.
- Runenwerk-specific `InputState` projections, `ActionState`, App/ECS scheduling,
  winit/native acquisition, UI adaptation, Draw behavior, and camera policy stay with
  their existing owners.
- No source mirror, forwarding crate/module, compatibility alias, source include,
  submodule, moving branch dependency, duplicate reducer/runtime authority, or private
  implementation reach-through may survive final closure.
- Repository-local issues and pull requests own volatile implementation details,
  validation results, and accepted SHAs; this initiative remains durable coordination
  authority only.

## Linked local issues

- [engineering#82](https://github.com/dornglut/engineering/issues/82) — organization
  boundary and initiative activation
- [runenwerk#771](https://github.com/dornglut/runenwerk/issues/771) — completed I3
  extraction decision
- [runenwerk#774](https://github.com/dornglut/runenwerk/issues/774) — completed
  pre-transfer source-boundary correction and transfer census
- [engineering#84](https://github.com/dornglut/engineering/issues/84) — successor
  repository bootstrap/profile reconciliation
- [runen-input#2](https://github.com/dornglut/runen-input/issues/2) — active successor
  transfer/public-contract acceptance

Add the Runenwerk consumer-cutover issue here when created. Do not invent issue numbers
or duplicate repository-local acceptance criteria in this charter.

## Risks and rollback

Before successor acceptance, reversal is ordinary abandonment of the unmerged successor
candidate; Runenwerk remains semantic source authority and no accepted dependency may
point at the abandoned candidate.

After successor acceptance, `runen-input` remains semantic source authority. Correct
cutover-blocking reusable defects there, accept a corrected successor revision, and
repin the Runenwerk cutover. If the transfer itself must be cancelled after successor
acceptance, use an explicitly accepted ADR 0008 reversal that retires successor
authority before predecessor semantic changes resume. A stalled downstream cutover is
blocked state, not permission for dual writable authority.

Material predecessor-boundary drift before successor acceptance, organization-policy
drift affecting handoff/profile requirements, licensing/provenance ambiguity, or a
discovered need for a materially broader reusable input contract must be reconciled in
the owning authority before dependent work continues.

## Closure record

Open.
