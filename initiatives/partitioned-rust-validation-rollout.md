# Partitioned Rust validation rollout

- Status: active
- Owner: Dornglut organization
- Opened: 2026-10-06
- Closed:
- Owning issue: [engineering#118](https://github.com/dornglut/engineering/issues/118)
- Decision authority: [Validation standard](../standards/validation.md)

## Outcome

Roll out the accepted partition-aware canonical validation model through the shared Rust
workflow, prove it with a measured RunenUI pilot, and only then make that accepted
generation the default for new Dornglut Rust repositories.

## Rationale

Engineering now permits a repository-owned canonical validation command to expose
bounded execution partitions without transferring validation semantics to shared CI.
RunenUI provides measured pressure for parallel execution, but changing a shared
workflow used across Dornglut requires ordered adoption, immutable rollback points, and
a pilot before defaults change.

## Affected repositories

- `dornglut/engineering` owns the validation standard and this rollout coordination.
- `dornglut/github-workflows` owns the reusable Rust execution contract and
  implementation.
- `dornglut/runen-ui` owns the first partitioned caller implementation and measured
  acceptance decision.
- `dornglut/.github` owns the organization Rust workflow template after successful
  pilot evidence.
- `dornglut/rust-framework-template` owns the standalone-framework bootstrap default
  after successful pilot evidence.

Other existing callers remain on immutable accepted revisions until repository-local
migration is independently justified.

## Dependency graph

```text
accepted Engineering partition-validation standard
    -> shared Rust workflow implementation
    -> accepted immutable github-workflows revision
    -> RunenUI partitioned pilot
    -> measured accept/reject decision
        -> reject: retain prior RunenUI pin and close with evidence
        -> accept: update organization/framework defaults
    -> optional later caller migrations
    -> initiative closure
```

## Acceptance evidence

Each repository-local delivery retains its own exact accepted base, reviewed feature
head, repository-owned exact-head validation, accepted merge, and accepted-main
evidence. RunenUI additionally records cold/new-key and controlled same-head warm
measurements against its accepted serial baseline before the partitioned model is
accepted as beneficial.

This charter records sequencing and closure only; it does not copy mutable workflow-run
or branch state.

## Sequencing constraints

The shared workflow implementation begins only from accepted
`github-workflows/main`. RunenUI must not reference an unmerged or moving shared
workflow revision. The RunenUI pilot begins only after one exact shared revision is
accepted on `github-workflows/main`.

Organization and framework defaults change only after the RunenUI pilot proves semantic
equivalence and material hosted-latency benefit. Linker, runner, workspace-target cache,
and other independent optimization work is outside this rollout.

## Linked local issues

- [engineering#118](https://github.com/dornglut/engineering/issues/118)
- [github-workflows#31](https://github.com/dornglut/github-workflows/issues/31)

The RunenUI pilot issue is added only after the shared workflow revision is accepted.

## Risks and rollback

Existing callers pin immutable workflow revisions and therefore do not change when the
workflow library advances. A defective shared candidate is corrected before caller
adoption. A failed RunenUI pilot returns to its prior accepted immutable workflow pin
and complete serial canonical validation. Default/template adoption does not occur
unless the pilot is accepted.

Partitioning must never become a reason to omit validation, alter package or feature
semantics, accept arbitrary execution inputs, or depend on mutable cross-job build
artifacts for correctness.

## Closure record

Open until the shared workflow is accepted, the RunenUI pilot is accepted or rejected
with evidence, successful-pilot defaults are reconciled when applicable, and remaining
caller migrations are explicitly dispositioned.
