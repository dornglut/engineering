# Verified-head validation adoption

- Status: completed
- Owner: Dornglut organization
- Opened: 2026-07-28
- Closed: 2026-07-29
- Owning issue: [engineering#20](https://github.com/dornglut/engineering/issues/20)
- Decision authority: [Validation standard](../standards/validation.md)

## Outcome

Dornglut repositories validate reviewed feature heads selected and proven explicitly, retain repository-owned canonical commands, present compact success output and bounded failure diagnostics, and call shared workflows through immutable accepted revisions.

## Rationale

GitHub's generated pull-request merge revision is useful merge-result evidence when intentionally validated, but it is not the reviewed feature head. The organization needs one truthful model that preserves reviewable repository content, read-only shared orchestration, and each repository's validation authority.

## Affected repositories

- `dornglut/github-workflows` owns the reusable read-only verification contract.
- `dornglut/engineering` owns organization standards, the first Python caller adoption, and this initiative.
- `dornglut/runen-sdf` is the Rust canary after Engineering acceptance and accepted-main proof.
- `dornglut/runenwerk` owns later Rust and documentation adoption for the integration product.
- `dornglut/.github` owns remaining default and template adoption.
- `dornglut/runen-ui` owns its remaining caller adoption.

## Dependency graph

```text
github-workflows contract
    ↓
Engineering standards and Python adoption
    ↓
RunenSDF Rust canary
    ↓
Runenwerk Rust and documentation adoption
    ↓
.github and RunenUI remaining adoption
    ↓
enforcement and closure
```

The accepted shared dependency is `dornglut/github-workflows@624cb41adeed21a6461eb838bc7330bd0a5079fd`. It is an immutable accepted dependency, not volatile branch state.

## Acceptance evidence

Each adoption records its accepted base, reviewed feature head, exact-head pull-request validation, accepted squash merge, accepted-main push validation, and stable required status context. The evidence proves the relevant repository revision without copying live branch, pull-request, queue, or workflow-run state into this charter.

## Sequencing constraints

Adoption proceeds in the dependency-graph order. The RunenSDF canary begins only after Engineering's slice is accepted, squash-merged, and proven through accepted-main push evidence. Later local issues are added as they are authorized.

## Linked local issues

- [engineering#20](https://github.com/dornglut/engineering/issues/20)
- [engineering#21](https://github.com/dornglut/engineering/issues/21)
- [github-workflows#8](https://github.com/dornglut/github-workflows/issues/8)

## Risks and rollback

Callers pin immutable revisions and remain on their prior accepted pin until an adoption pull request merges. A defective shared revision is corrected through a new immutable revision; existing accepted revisions are never moved or rewritten. The workflow library does not centralize product validation semantics.

## Closure record

Verified-head validation adoption completed after accepted delivery across the affected
callers and reusable-workflow contract. The immutable shared revision and accepted
delivery records above remain historical evidence; no active adoption work remains in
this initiative.
