# Dornglut organization normalization audit — 2026-07-26

- Observation date: 2026-07-26
- Owning program: [engineering issue #4](https://github.com/dornglut/engineering/issues/4)
- Governing decision: [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)
- Scope: organization governance, GitHub operating surfaces, repository profiles, inherited defaults, reusable validation, and maintained-repository conformance
- Evidence class: dated audit; this report records accepted state and exceptions but does not replace durable standards or repository-local authority

## Executive conclusion

Dornglut's organization-normalization program is complete enough to close as a bounded governance program.

The organization now has:

- distinct private idea capture and public accepted-work tracking;
- normalized organization, engineering, and workflow-library repositories;
- truthful active `dornglut/*` authority across maintained repositories;
- complete inherited and repository-local issue intake;
- immutable, read-only reusable validation workflows;
- squash-only protected default branches with canonical validation requirements;
- explicit repository profiles through organization custom properties;
- repository-local implementation, validation, roadmap, and release authority.

Two organization-wide controls remain deliberately deferred rather than silently treated as complete:

1. restrictive organization GitHub Actions policy;
2. organization security configuration covering Dependabot, CodeQL, secret scanning, push protection, and private vulnerability reporting.

These exceptions do not invalidate the accepted repository and governance model. They remain residual operational risks with explicit review triggers below.

The Rust framework template is not incomplete normalization work. It is a separate just-in-time bootstrap task that must be activated immediately before external RunenGPU repository creation, after the internal RunenGPU boundary is mature enough to define the template's real requirements.

## Audited repositories

| Repository | Accepted profile | Lifecycle | Contribution mode | Role |
|---|---|---|---|---|
| `dornglut/.github` | `organization-defaults` | `active` | `owner-only` | Community-health defaults, issue forms, PR guidance, and workflow templates |
| `dornglut/engineering` | `engineering` | `active` | `owner-only` | Organization governance, standards, ADRs, cross-repository architecture, initiatives, and dated reports |
| `dornglut/github-workflows` | `workflow-library` | `active` | `owner-only` | Reusable read-only CI orchestration |
| `dornglut/runenwerk` | `integration-product` | `active` | `discussion` | Integration platform and reference engine |
| `dornglut/runen-ui` | `rust-framework` | `active` | `discussion` | Standalone host-neutral UI framework |
| `dornglut/runen-sdf` | `rust-framework` | `active` | `discussion` | Standalone signed-distance-field framework |

All six repositories were connector-verified as public, unarchived, and using `main` during the settings audit. Native GitHub settings that are not exposed through the connected API are recorded as owner-attested evidence, not misrepresented as API-verified state.

## Completed controls

### Governance and authority

- PR [#5](https://github.com/dornglut/engineering/pull/5), merge `9ec28f001cab804ffc20a6339f799e2fc956ab96`, retired the abandoned ForgeOps authority.
- ADR 0003 supersedes ADR 0002 and records that no ForgeOps repository, credential, package, runtime asset, or consumer remains.
- PR [#6](https://github.com/dornglut/engineering/pull/6), merge `d3c627adfd7a4a281f7aa7cea987d60486d8d384`, normalized organization governance, repository standards, architecture, ADR indexing, initiative lifecycle, and validation.
- Durable authority is separated from live GitHub state according to [Authority and work](../governance/authority-and-work.md).

### Work intake and prioritization

- Private Project: [Dornglut Inbox](https://github.com/orgs/dornglut/projects/2/views/1).
- Public Project: [Dornglut Engineering Portfolio](https://github.com/orgs/dornglut/projects/1/views/3).
- Raw ideas and incomplete concepts remain private draft items.
- Accepted work remains an issue in the repository that owns the behavior.
- Project fields own live status, priority, and work kind; no Markdown priority mirror or idea backlog was introduced.
- Project internals are owner-attested because Projects V2 field definitions, view filters, workflows, visibility, and item values are outside the connected API surface.

### Organization defaults and intake

- PR [`.github#2`](https://github.com/dornglut/.github/pull/2), merge `0db26bfcff547476c3ead6293389d10dba453888`, normalized community-health defaults and issue intake.
- PR [`.github#3`](https://github.com/dornglut/.github/pull/3), merge `badc25495b0703aa3bff9ec982d1dbec7fe07897`, adopted the hardened reusable workflow revision.
- The default issue chooser contains `defect.yml`, `proposal.yml`, and `config.yml`.
- Blank issues are disabled through the accepted configuration.
- Repository-local issue-template directories own a complete local suite rather than incorrectly expecting inheritance merging.

### Reusable validation

- PR [`github-workflows#5`](https://github.com/dornglut/github-workflows/pull/5), merge `b6caad377102ca73794efaf734a65903b8efa829`, pinned third-party Actions to immutable revisions, added Dependabot for GitHub Actions, and hardened reusable Rust and Python validation.
- PR [`github-workflows#7`](https://github.com/dornglut/github-workflows/pull/7), merge `3cc9ad6c9bde3b970695baefa1cd815ff56111c7`, adopted `actions/checkout` v7.0.1 through reviewed immutable authority.
- PR [`engineering#8`](https://github.com/dornglut/engineering/pull/8), merge `bec90d4e5b64c545029ff94d034758660fd20fe7`, proved the revised workflow through a low-risk canary.
- Reusable workflows retain `contents: read`, do not inherit secrets, do not persist checkout credentials, do not accept arbitrary commands, and do not write source.
- Product repositories retain their own canonical validation semantics.

### Repository conformance

- PR [`runen-ui#24`](https://github.com/dornglut/runen-ui/pull/24), merge `71eef30ee14e60e42052165034e209c4242399bc`, corrected active namespace authority, repository metadata, issue intake, root entrypoints, and deterministic repository-audit enforcement without changing product behavior.
- PR [`runenwerk#158`](https://github.com/dornglut/runenwerk/pull/158), merge `6654da5d0e003208c5243efae2487f26a182f0ed`, adopted the permanent hardened validation caller without changing product architecture.
- PR [`runen-sdf#6`](https://github.com/dornglut/runen-sdf/pull/6), merge `711b2515378d5f85fe53e1083f44bf5adff2b05a`, completed its Rust-framework profile while preserving API, provenance, and standalone validation authority.
- Stale and superseded governance or workflow pull requests were closed instead of being retained as false active work.

### Merge and default-branch controls

The repository owner attested that all six maintained repositories now use:

- squash merge as the only allowed merge method;
- automatic deletion of merged head branches;
- an active repository-level `Protect main` ruleset;
- default-branch targeting;
- pull requests required before merge;
- zero required approvals during the solo-maintainer phase;
- conversation resolution required;
- canonical repository validation required;
- strict up-to-date branch testing;
- linear history;
- force-push protection;
- default-branch deletion protection;
- no routine bypass list.

The required checks are:

| Repository | Required check |
|---|---|
| `runenwerk` | `Runenwerk validation / Repository baseline` |
| `runen-ui` | `RunenUI validation / Repository baseline` |
| `runen-sdf` | `Validate standalone framework / Repository baseline` |
| `engineering` | `validate / validate` |
| `.github` | `validate / validate` |
| `github-workflows` | `validate / validate` |

These check names were derived from successful workflow jobs rather than guessed from workflow filenames.

### Repository custom properties

The repository owner attested that these organization-governed single-select properties exist and are assigned across all six maintained repositories:

- `profile`: `organization-defaults`, `engineering`, `workflow-library`, `rust-framework`, `integration-product`, `template`;
- `lifecycle`: `planned`, `active`, `maintenance`, `archived`;
- `contribution`: `owner-only`, `discussion`, `open`.

Repository actors cannot reclassify the properties. The properties are not globally required and have no misleading default value. Priority, milestone, release, language, validation result, and current-work data were not duplicated into custom properties.

## Deferred controls and residual risks

### Organization Actions policy

Status: deferred by owner decision on 2026-07-26.

Current mitigations:

- reusable workflows explicitly declare read-only permissions;
- third-party Actions are pinned to immutable commit SHAs;
- checkout credentials are not persisted;
- no workflow accepts arbitrary source-writing commands or inherited secrets;
- default-branch rules require the canonical validation result.

Residual risk:

- the organization-level Actions allowlist and default `GITHUB_TOKEN` policy were not independently tightened through native settings;
- a future repository or workflow could be more permissive than the accepted repository standards unless reviewed and validated.

Review trigger:

- before adding a new third-party Action;
- before enabling a deployment, release, publication, or source-writing workflow;
- before accepting routine external pull requests;
- before adding another organization member with write authority;
- during the external RunenGPU repository bootstrap.

### Organization security configuration

Status: deferred by owner decision on 2026-07-26.

Current mitigations:

- public security routing exists through organization defaults and repository-local exceptions;
- dependency and workflow updates remain repository-owned;
- validation uses least privilege and immutable dependencies;
- security-sensitive disclosures are explicitly prohibited from public issue forms.

Residual risk:

- organization-wide Dependabot alert/security-update coverage was not attested;
- CodeQL default setup was not standardized;
- secret scanning and push protection were not standardized;
- private vulnerability reporting was not standardized across every maintained repository.

Review trigger:

- before a public release or package publication;
- before processing external credentials, user data, network services, or untrusted files;
- before accepting routine external contributions;
- after the first externally consumed Runen framework release;
- during the external RunenGPU repository bootstrap.

### Labels and unused repository features

Status: optional cleanup, not a normalization blocker.

Dornglut deliberately does not duplicate Portfolio status, priority, or kind through labels. Unused GitHub default labels and unused repository features may be removed when they create real ambiguity or maintenance cost. Their presence alone does not contradict the authority model.

## Template disposition

The planned `dornglut/rust-framework-template` is a bootstrap mechanism, not a permanent synchronization authority.

It must be created immediately before external RunenGPU repository bootstrap, after internal RunenGPU G1–G8 work has established real workspace, validation, documentation, provenance, and conformance requirements.

The future task must:

1. create the minimal template repository;
2. mark it as a GitHub repository template;
3. prove it through a disposable canary repository;
4. verify inherited community-health and workflow-template behavior;
5. create external RunenGPU from the accepted template;
6. retire the canary;
7. record any repository-specific deviations in RunenGPU rather than overgeneralizing the template.

This task is intentionally separate from the completed organization-normalization program.

## Acceptance assessment

| Acceptance condition | Result |
|---|---|
| No active authority requires ForgeOps | Pass |
| Ideas and accepted work have separate Project surfaces | Pass, owner-attested Project configuration |
| Organization defaults and local template overrides are explicit | Pass |
| Repository profiles are defined and applied | Pass, owner-attested native properties |
| GitHub merge and default-branch settings are consistent | Pass, owner-attested native settings |
| Shared workflows are read-only and immutable | Pass, repository and CI evidence |
| Active repository identity uses `dornglut/*` outside explicit history | Pass |
| Every maintained repository has canonical validation and truthful entrypoints | Pass |
| Actions organization policy standardized | Deferred residual risk |
| Organization security configuration standardized | Deferred residual risk |
| Dated audit records accepted revisions, settings, exceptions, and triggers | Pass on merge of this report |

## Closure recommendation

Close engineering issue #4 after this report is validated, reviewed, and merged.

Do not keep the completed normalization program open solely for the future Rust framework template. Track that template as a separate triggered issue and keep it `planned` until external RunenGPU bootstrap is authorized.

The next active product action remains Runenwerk's RunenGPU sequence. Organization governance should be revisited only when a recorded review trigger becomes true or material drift is detected.
