# Provider-neutral repository automation

- Status: cancelled
- Owner: Dornglut organization
- Opened: 2026-07-22
- Closed: 2026-07-24
- Owning issue: [engineering#2](https://github.com/dornglut/engineering/issues/2)
- Decision authority: [ADR 0003](../adrs/0003-retire-provider-neutral-repository-automation.md)
- Original decision: [ADR 0002](../adrs/0002-provider-neutral-repository-automation.md)
- Superseding decision: [ADR 0003](../adrs/0003-retire-provider-neutral-repository-automation.md)
- Successor program: [organization normalization issue #4](https://github.com/dornglut/engineering/issues/4)

## Outcome

The initiative proposed a dedicated `dornglut/forgeops` repository containing a provider-neutral work-order, change-bundle, execution, publication, and conformance platform. Product adoption would have been blocked until that platform and a canary were complete.

The detailed original initiative remains available in repository history at commit [`289706d8a4aa498239399b6109da7fada4290e4d`](https://github.com/dornglut/engineering/commit/289706d8a4aa498239399b6109da7fada4290e4d).

## Rationale

ADR 0003 retired the program before implementation or product adoption.

The initiative was cancelled because:

- the proposed platform was disproportionate to current organization scale;
- no `dornglut/forgeops` repository existed;
- no product repository consumed the proposed protocol;
- the program would have delayed RunenSDF, RunenGPU, RunenRender, RunenECS, and organization work;
- ordinary Git branches, pull requests, repository-owned validation, the GitHub connector, checked-out local agents, and the native GitHub interface already provide a workable execution model;
- authoring tools do not need to become organization architecture.

## Resulting operating model

- GitHub issues and pull requests own accepted work and delivery evidence.
- Product and framework repositories own implementation and validation semantics.
- `dornglut/github-workflows` remains read-only CI orchestration.
- Connector-backed edits are used for bounded GitHub operations and suitable text changes.
- Checked-out repository executors are used for broad transformations and local validation.
- Native GitHub settings and Projects are configured through the GitHub interface when no reviewed connector surface exists.
- No product work is blocked on ForgeOps or an equivalent automation-platform canary.

## Preserved safety constraints

Cancellation does not authorize weaker delivery controls. The following remain required:

- validation does not author or publish source;
- implementation is delivered through task branches and pull requests;
- exact-head validation remains independent from the authoring tool;
- direct pushes to protected default branches are not part of the normal workflow;
- issue text or model output does not grant arbitrary command authority;
- temporary source-export or self-authoring workflows are not introduced as tool workarounds.

## Affected repositories

- `dornglut/engineering` retains the historical decision and initiative closure.
- `dornglut/github-workflows` retains read-only reusable CI orchestration.

## Dependency graph

None. The proposed program was cancelled before implementation, repository creation, or
product adoption.

## Acceptance evidence

ADR 0003 superseded ADR 0002, and engineering issue #2 was reclassified as not
planned. The original initiative revision remains in Git history as historical evidence.

## Sequencing constraints

No implementation, migration, or follow-on work is authorized by this cancelled
initiative.

## Linked local issues

- [engineering#2](https://github.com/dornglut/engineering/issues/2)
- [organization normalization issue #4](https://github.com/dornglut/engineering/issues/4)

## Risks and rollback

No repository, consumer, release, credential, package, branch, or runtime asset was
created by the cancelled program, so no migration or rollback is required.

## Closure record

- ADR 0002 is superseded by ADR 0003.
- The active repository-automation architecture is removed; its original content remains in Git history.
- `dornglut/forgeops` was never created.
- There are no consumers, releases, credentials, packages, branches, or runtime assets to migrate or archive.
- Engineering issue #2 is reclassified as not planned rather than completed implementation.
- Subsequent organization work is owned by engineering issue #4.

This initiative is closed and must not be used as an active prerequisite, implementation plan, or product sequencing authority.
