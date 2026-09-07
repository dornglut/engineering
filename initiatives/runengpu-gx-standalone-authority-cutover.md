# RunenGPU GX standalone authority cutover

- Status: completed
- Owner: Dornglut organization
- Opened: 2026-09-06
- Closed: 2026-09-07
- Owning issue: [engineering#51](https://github.com/dornglut/engineering/issues/51)
- Decision authority: [ADR 0008](../adrs/0008-adopt-bounded-source-authority-handoffs.md), [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)

## Outcome

Move RunenGPU semantic source authority from the Runenwerk predecessor into the standalone `dornglut/runen-gpu` framework, then cut Runenwerk over to one immutable accepted successor revision and delete the predecessor implementation without mirrors, forwarding compatibility, moving dependencies, or duplicate writable authority.

This initiative owns only cross-repository sequencing, rollback/reversal, authority handoff, and final coordination closure. Repository-local issues retain implementation, validation, public-contract, release, and consumer-migration authority.

## Rationale

GX now satisfies the organization initiative criteria: it spans multiple repositories, requires multiple repository-local delivery phases, has order-sensitive source-authority transitions, and needs explicit rollback/reversal and final closure evidence. A Runenwerk-local issue cannot truthfully own successor bootstrap, successor acceptance, and cross-repository authority handoff, while a broader implementation tracker here would duplicate repository-local authority. This charter therefore coordinates only the cross-repository lifecycle.

## Affected repositories

- `dornglut/engineering` owns this initiative, organization policy, and Engineering #9 bootstrap coordination.
- `dornglut/rust-framework-template` is the one-time framework bootstrap mechanism created and proved under Engineering #9 immediately before RunenGPU bootstrap.
- `dornglut/runen-gpu` becomes the standalone RunenGPU implementation and semantic source authority after repository-local acceptance.
- `dornglut/runenwerk` owns the predecessor boundary, downstream consumer migration, integration adaptation, predecessor deletion, and Runenwerk-side closure.

The disposable template canary is proof infrastructure under Engineering #9, not an ongoing participant in the framework dependency graph.

## Dependency graph

```text
accepted Runenwerk #449 mechanical census
    ↓
active GX initiative
    ↓
then-current organization bootstrap-input re-audit
    ↓
Engineering #9 activation
    ↓
rust-framework-template + disposable canary proof
    ↓
accepted runen-gpu repository bootstrap
    ↓
runen-gpu repository-local extraction authority
    ↓
unmerged successor extraction candidate
    ↓
standalone successor acceptance
    ↓
accepted runen-gpu revision becomes sole semantic source authority
    ↓
Runenwerk predecessor freezes
    ↓
Runenwerk exact-pin migration + predecessor deletion
    ↓
final cross-repository proof and closure
```

The bootstrap-input re-audit is an activation prerequisite for Engineering #9. The template is one-time bootstrap authority only and never becomes synchronization authority for `runen-gpu`.

## Acceptance evidence

Runenwerk #449 owns and records the accepted predecessor census that activated this cross-repository phase. Engineering #9 owns the accepted template/canary/bootstrap boundary; [runen-gpu#2](https://github.com/dornglut/runen-gpu/issues/2) owns successor extraction, implementation, and standalone validation; Runenwerk #449 owns downstream cutover/deletion acceptance. Pull requests in each owning repository retain exact-head and accepted-revision evidence. This charter links those authorities without copying volatile SHAs, workflow runs, branch state, or child acceptance criteria.

## Sequencing constraints

- Do not transfer RunenGPU implementation source or create successor implementation authority before Engineering #9 completes the accepted template/canary/bootstrap boundary.
- While the successor candidate is unmerged, Runenwerk remains the sole semantic RunenGPU source authority.
- On accepted successor default-branch publication, that accepted revision becomes sole semantic source authority immediately and the Runenwerk copy becomes frozen and deletion-bound under ADR 0008.
- During the bounded publication overlap, reusable-contract defects are corrected and accepted in `runen-gpu`; the frozen predecessor is not patched as an alternate implementation.
- Runenwerk migrates consumers to an exact accepted successor revision or exact accepted release and deletes the predecessor source/namespace in the same downstream cutover boundary.
- Ordinary successor feature evolution for the transferred boundary waits until predecessor deletion is accepted.
- No mirror, forwarding package/module, alias, source include, submodule, moving branch dependency, duplicate runtime, or private-backend reach-through may survive final closure.

## Linked local issues

- [engineering#51](https://github.com/dornglut/engineering/issues/51) — initiative delivery and coordination ownership
- [engineering#9](https://github.com/dornglut/engineering/issues/9) — framework template, canary, and repository bootstrap
- [runen-gpu#2](https://github.com/dornglut/runen-gpu/issues/2) — successor extraction, implementation, and standalone acceptance
- [runenwerk#449](https://github.com/dornglut/runenwerk/issues/449) — predecessor census, Runenwerk cutover, deletion, and GX closure
- [runenwerk#167](https://github.com/dornglut/runenwerk/issues/167) — RunenGPU repository-local program parent

Do not copy repository-local acceptance criteria into this charter.

## Risks and rollback

Before successor acceptance, rollback is ordinary abandonment of the unmerged successor candidate; Runenwerk remains semantic authority.

After successor acceptance, `runen-gpu` remains semantic authority. Correct blocking defects there, accept the corrected successor, and repin the downstream cutover. If the transfer itself must be cancelled after successor acceptance, use an explicitly accepted ADR-0008 reversal that retires successor authority before predecessor semantic changes resume. A stalled cutover is blocked state, not permission for dual writable authority.

Material Runenwerk drift that changes the accepted census boundary, or organization-policy drift that changes bootstrap/handoff requirements, must be reconciled in the owning authority before dependent work continues.

## Closure record

The RunenGPU GX authority cutover completed after standalone successor acceptance and the accepted Runenwerk exact-revision consumer migration and predecessor deletion. `dornglut/runen-gpu` is the sole RunenGPU semantic source authority; Runenwerk retains only its downstream integration boundary and no predecessor, forwarding, mirror, moving-dependency, duplicate-runtime, or private-backend compatibility authority remains. Repository-local delivery and validation evidence remains in the linked issues and pull requests; no active GX migration work remains in this initiative.
