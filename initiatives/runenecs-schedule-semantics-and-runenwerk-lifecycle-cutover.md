# RunenECS schedule semantics and Runenwerk lifecycle cutover

- Status: active
- Owner: Dornglut organization
- Opened: 2026-09-12
- Closed:
- Owning issue: engineering#67
- Decision authority: governance/authority-and-work.md; runen-ecs ADR 0001; runenwerk ADR 0022

## Outcome

Coordinate the RunenECS schedule-semantics transition and the paired Runenwerk consumer and publication-lifecycle migrations while preserving repository-local semantic, implementation, validation, and acceptance authority.

The initiative owns only cross-repository sequencing, immutable candidate-to-accepted-revision handoff, rollback behavior, and final coordination closure.

## Rationale

The program spans RunenECS and Runenwerk, requires multiple repository-local delivery phases, has ordering-sensitive dependency cutovers, needs explicit rollback and closure evidence, and cannot be truthfully owned by one repository-local issue.

The completed standalone RunenECS authority-transfer initiative remains historical provenance and is not reused for this later semantic dependency transition.

## Affected repositories

- `dornglut/runen-ecs` owns reusable ECS ordering, schedule diagnostics, deferred visibility, and schedule inspection semantics.
- `dornglut/runenwerk` owns integration policy, maintained ordering-consumer classification, and product/query publication lifecycle semantics.
- `dornglut/engineering` owns only this cross-repository coordination charter.

## Dependency graph

```text
runen-ecs#27 ordering presence
    -> runenwerk#580 candidate compatibility proof
    -> accepted runen-ecs#27 revision
    -> runenwerk#580 accepted-revision repin and cutover

runen-ecs#27 + runen-ecs#52
    -> runen-ecs#33 semantic publication frontiers
    -> runenwerk#591 candidate compatibility proof
    -> accepted runen-ecs#33 revision
    -> runenwerk#591 accepted-revision repin and lifecycle cutover

runen-ecs#33
    -> runen-ecs#28 normalized schedule inspection
```

Repository-local parent `runen-ecs#26` owns the RunenECS-internal slice relationship. This initiative does not duplicate child acceptance criteria.

## Acceptance evidence

Cross-repository acceptance requires, as applicable:

- an executor-validated immutable upstream feature candidate;
- an executor-validated provisional downstream candidate against that exact upstream feature SHA;
- normal upstream exact-head review, CI, guarded squash acceptance, and accepted-main verification;
- reconstruction or repinning of the downstream candidate to the immutable accepted upstream revision through the normal dependency and lockfile path;
- fresh downstream canonical validation, exact-head CI, review, and guarded acceptance;
- repository-local evidence that the intended behavior survives the semantic cutover without compatibility aliases, moving dependencies, fake lifecycle callbacks, or duplicate authority.

The repository-local issues and pull requests retain exact SHAs, validation runs, detailed acceptance matrices, and implementation evidence. This charter does not mirror them.

## Sequencing constraints

A provisional downstream candidate may consume an immutable upstream feature SHA only as compatibility evidence. An unmerged upstream feature SHA is not accepted dependency authority.

Final Runenwerk acceptance must use an immutable accepted RunenECS revision. If upstream squash acceptance changes the commit identity while preserving the reviewed tree, the downstream dependency and lockfile are regenerated for the accepted revision and validation is rerun on the final downstream head.

Runenwerk already consumes RunenECS through an immutable revision. Accepting a new RunenECS revision therefore does not silently mutate the accepted Runenwerk build. The downstream repository may remain on its previous accepted pin until its own migration is ready.

The ordering-presence pair precedes the runtime publication pair. RunenECS inspection follows the normalized ordering/publication model and does not import Runenwerk product lifecycle policy.

## Linked local issues

RunenECS:

- `dornglut/runen-ecs#26` — ADR 0001 implementation parent
- `dornglut/runen-ecs#27` — explicit required and optional ordering references
- `dornglut/runen-ecs#52` — canonical semantic publication-frontier derivation
- `dornglut/runen-ecs#33` — semantic deferred-publication runtime cutover
- `dornglut/runen-ecs#28` — normalized reason-carrying schedule inspection

Runenwerk:

- `dornglut/runenwerk#580` — ordering-reference presence migration
- `dornglut/runenwerk#591` — product/query publication lifecycle cutover

## Risks and rollback

If provisional downstream compatibility fails, neither repository gains permission to weaken the accepted semantic boundary merely to preserve predecessor behavior. Correct the owning candidate or amend the owning accepted authority when the failure proves a real contract defect.

If a final downstream cutover fails after upstream acceptance, keep Runenwerk on its previously accepted immutable RunenECS revision while the owning downstream issue is corrected. Do not use a moving branch dependency, compatibility fork, duplicate scheduler/publication path, fake ECS frontier callback, or long-lived candidate pin.

If repository-local authority changes the semantic contract or dependency graph materially, stop the affected handoff, reconcile this initiative only where the cross-repository contract actually changed, and resume from explicit accepted repository bases.

## Closure record

Open.
