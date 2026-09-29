# Maintained-repository GitHub protection normalization

- Status: completed
- Owner: Dornglut organization
- Opened: 2026-09-29
- Closed: 2026-09-29
- Owning issue: [engineering#94](https://github.com/dornglut/engineering/issues/94)
- Decision authority: [Authority and work](../governance/authority-and-work.md), [GitHub standard](../standards/github.md), [Validation standard](../standards/validation.md)

## Outcome

Coordinate the bounded native GitHub-settings normalization needed to bring maintained Dornglut repositories back to the accepted protection target without replacing repository-local issue authority or creating overlapping settings writers.

The initiative owns only cross-repository sequencing, mutable-settings writer ownership, rollback discipline, and final coordination closure. Each linked delivery issue owns its exact native settings delta and verification.

## Rationale

The normalization spans multiple repositories and multiple local admin deliveries. Some settings changes touch the same live ruleset or repository configuration and therefore require serialization. Closure also requires a final cross-repository native-state audit. One merge-method issue cannot truthfully own validation enforcement, review resolution, repository classification, private-repository capability, and merge-method reconciliation across all affected repositories.

## Affected repositories

- `dornglut/engineering` owns the organization GitHub standard, this initiative, and merge-method reconciliation.
- `dornglut/runen-net` owns its protected-main strict-status and review-resolution correction.
- `dornglut/runen-spatial` owns its protected-main strict-status correction.
- `dornglut/runen-lab` owns its complete local repository-settings normalization.
- `dornglut/runen-online` owns its protected-main validation and review-resolution correction.
- `dornglut/werkstatt` owns its protected-main validation and accepted repository classification.
- `dornglut/chimera-signal` owns the private-repository protection capability and visibility decision.

Other maintained repositories participate only where Engineering #53 identifies merge-method drift; they do not gain new repository-local protection work merely because this initiative exists.

## Dependency graph

```text
accepted GitHub protection semantics
    -> repository-local protection deliveries

runen-spatial#42
    -> runen-spatial merge-method step in engineering#53

runen-net#218
    -> runen-net merge-method step in engineering#53

runen-online#52
    -> runen-online merge-method step in engineering#53

werkstatt#21
    -> Werkstatt merge-method/ruleset step in engineering#53

runen-lab#3
    -> final audit
    (engineering#53 does not perform an overlapping Runen Lab settings write)

chimera-signal#21
    -> accepted visibility/plan disposition
    -> any separately authorized Chimera protection or merge-policy action

all completed local/admin work
    -> final cross-repository native-state audit
    -> initiative closure
```

Completed Engineering investigations and policy decisions remain historical inputs; they are not reopened or duplicated by this charter.

## Acceptance evidence

Cross-repository completion requires repository-local evidence for every authorized native mutation or accepted exception, including a fresh pre-change read, the exact bounded setting change, and a post-change read proving the resulting state.

The final Engineering audit confirms that maintained repositories satisfy the accepted GitHub protection target or identify an explicit durable exception, that merge-method ownership is reconciled, that required validation and review protections are enforced where supported, and that Chimera Signal has a truthful terminal capability or visibility disposition.

Native admin changes must not move repository source revisions merely to establish settings compliance. Detailed live payloads, run identifiers, and per-repository acceptance evidence remain in the linked issues rather than this charter.

## Sequencing constraints

Each linked delivery issue remains the sole authority for its exact native settings mutation. Repository-local issues own their listed protection or classification fields; Engineering #53 owns only its separately scoped merge-method fields.

Do not write the same live ruleset from two issues concurrently. For repositories that also need Engineering #53 merge-method normalization, complete and verify the repository-local protection delivery first, then re-read live state before the #53 step.

Werkstatt #21 precedes the Werkstatt-specific #53 ruleset merge-method update because both touch the active pull-request ruleset.

Runen Lab #3 remains the sole writer for its complete local normalization. Engineering #53 must not perform a separate overlapping Runen Lab settings mutation.

Chimera Signal must resolve its private-repository capability or visibility boundary before any protected-main or merge-policy mutation is attempted.

Independent repositories may proceed in parallel only when their live mutable settings surfaces and writer ownership do not overlap.

Every native action re-resolves the target repository and ruleset immediately before mutation and verifies the resulting live state afterward. Repository source revisions must not move merely because an admin setting changed.

## Risks and rollback

Repository-local delivery evidence records the pre-change native state needed to identify an unintended mutation.

If a native settings action produces a materially different result from its authorized delta, stop further dependent settings work in that repository, restore the previously verified setting where the available native surface permits a safe exact rollback, and independently re-read the resulting state before continuing.

Do not use source commits, validation workflows, compatibility settings, or duplicate rulesets as rollback substitutes for an admin-setting error.

If the Chimera capability or visibility decision changes, stop dependent Chimera settings work and reconcile the owning local issue before resuming.

## Linked local issues

Engineering:

- [engineering#53](https://github.com/dornglut/engineering/issues/53) — maintained-repository merge-method normalization

RunenNet:

- [runen-net#218](https://github.com/dornglut/runen-net/issues/218) — strict canonical status and review-thread resolution

RunenSpatial:

- [runen-spatial#42](https://github.com/dornglut/runen-spatial/issues/42) — strict canonical status enforcement

Runen Lab:

- [runen-lab#3](https://github.com/dornglut/runen-lab/issues/3) — complete local repository-settings normalization

RunenOnline:

- [runen-online#52](https://github.com/dornglut/runen-online/issues/52) — canonical validation and review-thread enforcement

Werkstatt:

- [werkstatt#21](https://github.com/dornglut/werkstatt/issues/21) — canonical validation and accepted repository classification

Chimera Signal:

- [chimera-signal#21](https://github.com/dornglut/chimera-signal/issues/21) — private-repository protection capability and visibility decision

## Closure record

Completed 2026-09-29.

All linked repository-local deliveries completed, and Engineering #53 completed the maintained-repository merge-method reconciliation.

The final native-state audit confirmed:

- every maintained repository uses squash-only repository merge settings and automatic merged-head deletion;
- all public maintained repositories retain active default-branch rulesets with required canonical validation, conversation resolution, deletion and non-fast-forward protection, linear history, zero meaningless approval requirements, and empty bypass;
- non-queue public repositories require strict/up-to-date canonical status checks;
- Runenwerk retains its accepted merge-queue exception, where exact merge-group integration evidence provides the latest-base gate instead of strict feature-branch status checking;
- Chimera Signal remains private under the accepted temporary exception in [chimera-signal#21](https://github.com/dornglut/chimera-signal/issues/21): canonical CI remains evidence but is not represented as native protected-main enforcement until the repository plan or visibility changes.

No overlapping settings writer or undocumented merge-method drift remains. Any future capability, plan, visibility, or policy change is new work under the normal authority process rather than continuation of this initiative.
