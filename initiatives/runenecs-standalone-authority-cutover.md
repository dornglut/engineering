# RunenECS standalone authority cutover

- Status: active
- Owner: Dornglut organization
- Opened: 2026-09-10
- Owning issue: [engineering#60](https://github.com/dornglut/engineering/issues/60)
- Decision authority: [ADR 0008](../adrs/0008-adopt-bounded-source-authority-handoffs.md), [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)

## Outcome

Move RunenECS semantic source authority from the corrected Runenwerk predecessor into the standalone `dornglut/runen-ecs` framework, then cut Runenwerk over to one immutable accepted successor revision and delete the predecessor implementation without mirrors, forwarding compatibility, moving dependencies, or duplicate writable authority.

This initiative owns only cross-repository sequencing, rollback/reversal, authority handoff, and final coordination closure. Repository-local issues retain implementation, validation, public-contract, repository-profile, release, consumer-migration, and deletion authority.

## Rationale

The post-C9 transfer satisfies the organization initiative criteria: it spans `runen-ecs` and Runenwerk, requires multiple repository-local delivery phases, has an order-sensitive semantic authority switch, and needs explicit reversal and final closure evidence. No repository-local issue can truthfully own both successor acceptance and predecessor cutover. This charter therefore coordinates the lifecycle without duplicating local implementation contracts or live operational state.

## Affected repositories

- `dornglut/engineering` owns this initiative and organization-level handoff policy.
- `dornglut/runen-ecs` owns successor repository reconciliation, transferred reusable RunenECS implementation/public contract, standalone validation, provenance, and successor acceptance.
- `dornglut/runenwerk` owns the corrected predecessor boundary before the switch, downstream consumer migration, integration adaptation, predecessor deletion, and Runenwerk-side closure.

The current organization repository standards and reusable workflows inform repository-profile reconciliation but do not become RunenECS implementation authority or ongoing synchronization authority.

## Dependency graph

```text
accepted corrected Runenwerk C9
    ↓
active RunenECS initiative
    ↓
runen-ecs repository-profile reconciliation + transfer census
    ↓
runen-ecs repository-local successor transfer authority
    ↓
unmerged standalone successor candidate
    ↓
exact-head standalone validation and successor acceptance
    ↓
accepted runen-ecs revision becomes sole RunenECS semantic source authority
    ↓
Runenwerk predecessor freezes
    ↓
Runenwerk exact-pin consumer migration + predecessor deletion
    ↓
final no-mirror/no-forwarder/no-moving-dependency proof
    ↓
post-extraction runen-ecs audit may activate
    ↓
initiative closure
```

## Acceptance evidence

[runenwerk#530](https://github.com/dornglut/runenwerk/issues/530) owns and records accepted C9 and its corrective closeout evidence. [runen-ecs#2](https://github.com/dornglut/runen-ecs/issues/2) owns successor transfer, repository reconciliation, standalone validation, and accepted successor-revision evidence. [runenwerk#551](https://github.com/dornglut/runenwerk/issues/551) owns the exact-pin downstream cutover, predecessor deletion, and Runenwerk post-merge validation. Pull requests in each owning repository retain exact-head and accepted-revision evidence. This charter links those authorities without copying volatile SHAs, workflow runs, branch state, or child acceptance matrices.

## Sequencing constraints

- Corrected accepted Runenwerk C9 is the predecessor input boundary; do not reopen completed C0-C9 repair work merely to facilitate physical transfer.
- While the successor candidate is unmerged, Runenwerk remains the sole semantic RunenECS source authority. The candidate is staging only and is not accepted dependency authority.
- Successor preparation must reconcile the existing `runen-ecs` namespace shell to the current `rust-framework` repository profile and perform a file-by-file ownership census; it must not copy Runenwerk's integration-product topology by inertia.
- On accepted successor default-branch publication, that accepted revision becomes sole semantic source authority immediately and the Runenwerk predecessor implementation freezes under ADR 0008.
- During bounded physical overlap after the authority switch, reusable-contract defects are corrected and accepted in `runen-ecs`; Runenwerk repins the corrected accepted revision. The frozen predecessor is not patched as an alternate implementation.
- Runenwerk migrates maintained consumers to an exact immutable accepted successor revision or accepted release and deletes predecessor source/package authority in the same downstream cutover boundary.
- Ordinary successor feature evolution for the transferred boundary waits until predecessor deletion is accepted.
- No source mirror, forwarding crate/module, compatibility alias, source include, submodule, moving branch dependency, duplicate runtime, or private implementation reach-through may survive final closure.
- Repository-local issues and pull requests own volatile implementation details, branch heads, validation commands/results, and accepted SHAs; this initiative remains durable coordination authority only.

## Linked local issues

- [engineering#60](https://github.com/dornglut/engineering/issues/60) — initiative delivery and cross-repository coordination
- [runenwerk#197](https://github.com/dornglut/runenwerk/issues/197) — RunenECS repository-local program parent
- [runenwerk#530](https://github.com/dornglut/runenwerk/issues/530) — completed corrected C9 predecessor/conformance boundary
- [runen-ecs#2](https://github.com/dornglut/runen-ecs/issues/2) — successor repository reconciliation, source transfer, validation, and acceptance
- [runenwerk#551](https://github.com/dornglut/runenwerk/issues/551) — downstream exact-pin consumer cutover and predecessor deletion
- [runen-ecs#1](https://github.com/dornglut/runen-ecs/issues/1) — blocked post-extraction audit; activates only after successor authority and predecessor deletion are both accepted

Do not copy repository-local acceptance criteria into this charter.

## Risks and reversal

Before successor acceptance, reversal is ordinary abandonment of the unmerged successor candidate; Runenwerk remains semantic authority and no dependency may point at the abandoned candidate.

After successor acceptance, `runen-ecs` remains semantic authority. Correct blocking reusable defects there, accept a corrected successor revision, and repin the Runenwerk cutover. If the transfer itself must be cancelled after successor acceptance, use an explicitly accepted ADR-0008 reversal that retires successor authority before predecessor semantic changes resume. A stalled Runenwerk cutover is blocked state, not permission for dual writable authority.

Material predecessor-boundary drift before successor acceptance, organization-policy drift affecting handoff/profile requirements, licensing/provenance ambiguity, or a discovered need for a new public capability must be reconciled in the owning authority before dependent work continues.

## Closure criteria

Close this initiative only after repository-local evidence establishes all of the following:

- an accepted `runen-ecs` default-branch revision is the sole RunenECS semantic source authority;
- Runenwerk consumes an immutable exact accepted successor revision or accepted release through final public package identities;
- Runenwerk predecessor RunenECS implementation/package authority is deleted rather than forwarded;
- no predecessor source mirror, compatibility namespace, include, submodule, moving dependency, duplicate runtime, or private successor reach-through remains;
- current architecture, validation ownership, provenance, licensing, and repository-family references are reconciled where actually affected;
- [runen-ecs#2](https://github.com/dornglut/runen-ecs/issues/2) and [runenwerk#551](https://github.com/dornglut/runenwerk/issues/551) are accepted or explicitly dispositioned consistently with ADR 0008;
- [runen-ecs#1](https://github.com/dornglut/runen-ecs/issues/1) is eligible to activate as the post-extraction audit;
- no active RunenECS transfer/cutover work remains in this initiative.
