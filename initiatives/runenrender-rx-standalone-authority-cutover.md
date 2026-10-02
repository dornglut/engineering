# RunenRender RX standalone authority cutover

- Status: active
- Owner: Dornglut organization
- Opened: 2026-10-02
- Closed:
- Owning issue: [engineering#105](https://github.com/dornglut/engineering/issues/105)
- Decision authority: [ADR 0008](../adrs/0008-adopt-bounded-source-authority-handoffs.md), [ADR 0009](../adrs/0009-establish-runen-shader-boundary.md), [Runen family architecture](../architecture/runen-family.md), [runenwerk#906](https://github.com/dornglut/runenwerk/issues/906), [runenwerk#1129](https://github.com/dornglut/runenwerk/issues/1129)

## Outcome

Move RunenRender semantic source authority from the Runenwerk predecessor into standalone `dornglut/runen-render`, then cut Runenwerk over to one immutable accepted successor revision and delete the predecessor semantic, maintained-method, WGSL, and private qualification authority without mirrors, forwarding compatibility, moving dependencies, or duplicate writable authority.

This initiative owns only cross-repository sequencing, rollback/reversal, authority handoff, and final coordination closure. Repository-local issues retain successor implementation, validation, package/public-contract, dependency composition, consumer migration, and predecessor-deletion authority.

## Rationale

Runenwerk has completed the bounded R8 extraction qualification required by the accepted Runen-family architecture. The transfer now spans Engineering, Runenwerk, the accepted standalone RunenRender successor, and the accepted RunenGPU/RunenShader sibling boundaries; requires multiple repository-local delivery phases; has an order-sensitive ADR-0008 authority switch; and needs explicit rollback and final no-duplicate-authority evidence.

A Runenwerk-local issue cannot truthfully own successor bootstrap, standalone acceptance, and the later downstream cutover. A successor-local issue cannot own the predecessor deletion. The initiative therefore coordinates only the cross-repository lifecycle.

## Affected repositories

- `dornglut/runenwerk` owns the downstream consumer cutover and predecessor deletion; its transferred predecessor boundary is frozen and deletion-bound after successor acceptance.
- `dornglut/runen-render` is the standalone authority for reusable renderer semantics, maintained renderer method/execution, renderer conformance, and the explicit RunenShader-artifact to RunenGPU-admission bridge.
- `dornglut/runen-gpu` remains the standalone GPU execution authority consumed through an immutable accepted revision.
- `dornglut/runen-shader` remains the standalone shader source/compilation/artifact authority consumed through an immutable accepted revision.
- `dornglut/engineering` owns only this coordination charter and the organization-level handoff rules.

## Dependency graph

```text
accepted Runenwerk R8 extraction boundary
    -> current bootstrap/profile/security reconciliation
    -> create/bootstrap runen-render successor
    -> runen-render-local transfer authority
    -> unmerged standalone successor candidate
    -> standalone validation + package-level conformance
    -> exact maintained RunenShader artifact -> RunenGPU execution proof
    -> successor acceptance / ADR-0008 authority switch
    -> frozen Runenwerk predecessor boundary
    -> Runenwerk exact-revision dependency cutover
    -> real World/UI/frame/Render-Flow/Render-Lab consumer migration
    -> predecessor semantic/method/WGSL/private qualification deletion
    -> final cross-repository residue proof
    -> ordinary standalone RunenRender evolution
```

Runenwerk [#906](https://github.com/dornglut/runenwerk/issues/906) owns the completed extraction-readiness outcome. Runenwerk [#1129](https://github.com/dornglut/runenwerk/issues/1129) owns the frozen predecessor transfer/stay/export/consumer/deletion inputs. Repository-local successor and downstream cutover issues own the implementation phases once created.

## Current phase

The ADR-0008 successor acceptance has occurred. `dornglut/runen-render` is now the sole
RunenRender semantic source authority. The transferred Runenwerk predecessor boundary is
frozen and deletion-bound. Runenwerk
[#1134](https://github.com/dornglut/runenwerk/issues/1134) owns the remaining
exact-revision consumer migration and predecessor deletion; this initiative remains
active through final residue proof and cross-repository closure.

## Sequencing constraints

Before successor acceptance, Runenwerk remains the sole RunenRender semantic source authority. The successor may be built and validated on an unmerged branch, but no accepted Runenwerk dependency may point to that branch or treat it as semantic authority.

The authority switch occurs when an exact successor revision is accepted on the successor default branch under ADR 0008. From that point, the transferred predecessor boundary is frozen. Reusable-contract corrections are made and accepted in `runen-render`, then the Runenwerk cutover repins; the frozen predecessor is not patched as an alternate implementation.

Runenwerk must consume one immutable accepted successor revision or accepted release and delete predecessor semantic/method/WGSL authority in the downstream cutover. Its product/frame/native/World/UI/Editor/Render-Lab integration remains Runenwerk-owned and consumes the successor directly rather than through a forwarding semantic namespace.

The explicit RunenShader/RunenGPU composition is owned by RunenRender. RunenShader compilation/artifact outcomes remain distinct from RunenGPU program admission and execution outcomes. The transfer must not mirror maintained WGSL in both accepted owners.

Ordinary successor feature/maturity evolution waits until predecessor deletion is accepted. During the bounded physical overlap, only ADR-0008-permitted cutover-blocking extraction, correctness, security, validation, provenance, or release corrections may change the transferred boundary.

No source mirror, forwarding crate/module, compatibility alias, source include, submodule, moving branch dependency, duplicate renderer runtime, mirrored WGSL authority, or private backend reach-through may survive closure.

## Acceptance evidence

Cross-repository acceptance requires, as applicable:

- one immutable predecessor extraction record and source/provenance census;
- a repository-profile-compliant standalone successor with repository-owned canonical validation;
- package-level ordinary public conformance against the actual successor package;
- exact sibling dependency revisions and the RunenShader artifact -> RunenGPU execution handoff;
- exact-head successor review and validation before authority transfer;
- downstream Runenwerk migration to the immutable accepted successor;
- deletion of predecessor semantic/method/WGSL and private qualification authority rather than forwarding it;
- final source/dependency/API residue checks proving one semantic owner and one maintained shader authority.

Repository-local issues and pull requests retain exact SHAs, validation run IDs, implementation matrices, and detailed acceptance evidence. This charter does not mirror them.

## Linked local issues

Engineering:

- [engineering#105](https://github.com/dornglut/engineering/issues/105) — RX initiative delivery and cross-repository coordination
- [engineering#107](https://github.com/dornglut/engineering/issues/107) — completed exact-template generation of the standalone destination repository

RunenRender:

- [runen-render#1](https://github.com/dornglut/runen-render/issues/1) — successor repository acceptance and ADR-0008 semantic authority switch
- [runen-render#2](https://github.com/dornglut/runen-render/issues/2) — source-free repository/profile bootstrap before semantic transfer
- [runen-render#4](https://github.com/dornglut/runen-render/issues/4) — completed frozen-R8 semantic/conformance transfer and standalone executable proof

Runenwerk:

- [runenwerk#906](https://github.com/dornglut/runenwerk/issues/906) — completed R8 extraction readiness
- [runenwerk#1129](https://github.com/dornglut/runenwerk/issues/1129) — completed exact transfer/stay/export/consumer/deletion freeze
- [runenwerk#1134](https://github.com/dornglut/runenwerk/issues/1134) — downstream exact-revision consumer cutover and predecessor deletion

## Risks and rollback

Before successor acceptance, reversal is ordinary abandonment of the unmerged successor candidate; Runenwerk remains semantic authority and no accepted dependency may point at the abandoned candidate.

After successor acceptance, `runen-render` remains semantic authority. Correct blocking reusable defects there, accept a corrected successor revision, and repin the Runenwerk cutover. If the transfer itself must be cancelled after authority moved, use an explicitly accepted ADR-0008 reversal that retires successor authority before predecessor semantic changes resume. A stalled downstream cutover is blocked state, not permission for dual writable authority.

Material predecessor-boundary drift before successor acceptance, organization-policy drift affecting repository/handoff requirements, licensing/provenance ambiguity, or discovery of a new public capability needed for clean cutover requires reconciliation in the owning authority before dependent work continues.

## Closure record

Open.
