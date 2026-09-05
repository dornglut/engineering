# RunenGPU GX standalone authority cutover

- Status: active
- Owner: Dornglut organization
- Opened: 2026-09-06
- Owning issue: [engineering#51](https://github.com/dornglut/engineering/issues/51)
- Decision authority: [ADR 0008](../adrs/0008-adopt-bounded-source-authority-handoffs.md), [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)

## Outcome

Move RunenGPU semantic source authority from the Runenwerk predecessor into the standalone `dornglut/runen-gpu` framework, then cut Runenwerk over to one immutable accepted successor revision and delete the predecessor implementation without mirrors, forwarding compatibility, moving dependencies, or duplicate writable authority.

This initiative owns only cross-repository sequencing, rollback/reversal, authority handoff, and final coordination closure. Repository-local issues retain implementation, validation, public-contract, release, and consumer-migration authority.

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
bootstrap still-empty runen-gpu shell from accepted template baseline
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
- [engineering#9](https://github.com/dornglut/engineering/issues/9) — framework template, canary, and existing-shell bootstrap
- [runenwerk#449](https://github.com/dornglut/runenwerk/issues/449) — predecessor census, Runenwerk cutover, deletion, and GX closure
- [runenwerk#167](https://github.com/dornglut/runenwerk/issues/167) — RunenGPU repository-local program parent

Add the future `runen-gpu` repository-local extraction/delivery issue only when the shell has been bootstrapped and that local work is authorized. Do not copy its acceptance criteria into this charter.

## Risks and rollback

Before successor acceptance, rollback is ordinary abandonment of the unmerged successor candidate; Runenwerk remains semantic authority.

After successor acceptance, `runen-gpu` remains semantic authority. Correct blocking defects there, accept the corrected successor, and repin the downstream cutover. If the transfer itself must be cancelled after successor acceptance, use an explicitly accepted ADR-0008 reversal that retires successor authority before predecessor semantic changes resume. A stalled cutover is blocked state, not permission for dual writable authority.

Material Runenwerk drift that changes the accepted census boundary, or organization-policy drift that changes bootstrap/handoff requirements, must be reconciled in the owning authority before dependent work continues.

## Closure

Complete this initiative only when:

- `dornglut/runen-gpu` is the accepted sole RunenGPU semantic source authority;
- Runenwerk consumes one immutable accepted successor revision or release;
- the Runenwerk predecessor implementation and forwarding namespace are deleted;
- no mirror, include, submodule, moving branch, compatibility authority, duplicate runtime, frozen predecessor copy, or private WGPU reach-through remains;
- bootstrap, licensing, provenance, release, and cross-repository coordination obligations are reconciled in their owning repositories;
- every linked repository-local delivery issue is accepted or explicitly dispositioned.
