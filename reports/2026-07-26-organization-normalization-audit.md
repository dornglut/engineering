# Dornglut organization normalization audit — 2026-07-26

- Observation date: 2026-07-26
- Closure date: 2026-07-26
- Owning program: [engineering issue #4](https://github.com/dornglut/engineering/issues/4)
- Governing decision: [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)
- Scope: organization governance, GitHub operating surfaces, repository profiles, inherited defaults, reusable validation, and maintained-repository conformance
- Evidence class: dated audit; this report records repository evidence and owner-attested native GitHub settings without replacing durable standards or repository-local authority

## Executive conclusion

Dornglut's organization-normalization program is complete as a bounded governance program.

The organization now has:

- separate private idea capture and public accepted-work tracking;
- normalized `.github`, `engineering`, and `github-workflows` authorities;
- active `dornglut/*` identity across maintained repositories;
- complete inherited and repository-local issue intake;
- immutable, read-only reusable validation;
- explicit repository profiles through custom properties;
- owner-attested squash-only merge settings and active `Protect main` rulesets;
- repository-local implementation, validation, roadmap, and release authority.

The connected GitHub App previously wrote the first report revision directly to `engineering/main` at commit `beb515f9b19106e40e05bcf549e6af58c06d9d7c`. The event remains preserved as evidence. On 2026-07-26 the repository owner corrected the protection configuration and attested that the unintended direct-write path is no longer available.

The organization Actions policy and organization security configuration remain deliberately deferred residual risks. Their review triggers are recorded below.

The Rust framework template is separate future work owned by [engineering issue #9](https://github.com/dornglut/engineering/issues/9). It activates only immediately before external RunenGPU bootstrap.

## Audited repositories

| Repository | Profile | Lifecycle | Contribution | Role |
|---|---|---|---|---|
| `dornglut/.github` | `organization-defaults` | `active` | `owner-only` | Community-health defaults, issue forms, PR guidance, workflow templates |
| `dornglut/engineering` | `engineering` | `active` | `owner-only` | Organization governance, standards, ADRs, shared architecture, initiatives, reports |
| `dornglut/github-workflows` | `workflow-library` | `active` | `owner-only` | Reusable read-only CI orchestration |
| `dornglut/runenwerk` | `integration-product` | `active` | `discussion` | Integration platform and reference engine |
| `dornglut/runen-ui` | `rust-framework` | `active` | `discussion` | Standalone host-neutral UI framework |
| `dornglut/runen-sdf` | `rust-framework` | `active` | `discussion` | Standalone signed-distance-field framework |

All six repositories were connector-verified as public, unarchived, and using `main`. Native GitHub settings unavailable through the connected API are classified as owner-attested rather than API-verified.

## Completed controls

### Governance and authority

- Engineering PR [#5](https://github.com/dornglut/engineering/pull/5), merge `9ec28f001cab804ffc20a6339f799e2fc956ab96`, retired ForgeOps authority.
- ADR 0003 supersedes ADR 0002 and records that no ForgeOps repository, credential, package, runtime asset, or consumer remains.
- Engineering PR [#6](https://github.com/dornglut/engineering/pull/6), merge `d3c627adfd7a4a281f7aa7cea987d60486d8d384`, normalized governance, standards, shared architecture, ADR indexing, initiative lifecycle, and validation.
- Durable authority is separated from live GitHub state according to [Authority and work](../governance/authority-and-work.md).

### Work intake and prioritization

- Private Project: [Dornglut Inbox](https://github.com/orgs/dornglut/projects/2/views/1).
- Public Project: [Dornglut Engineering Portfolio](https://github.com/orgs/dornglut/projects/1/views/3).
- Raw ideas remain private Project draft items.
- Accepted work remains an issue in the repository that owns the behavior.
- Project fields own live status, priority, and kind; no Markdown priority or idea mirror was introduced.
- Projects V2 internals are owner-attested because the connected API does not expose their visibility, fields, views, workflows, or item values.

### Organization defaults and intake

- `.github` PR [#2](https://github.com/dornglut/.github/pull/2), merge `0db26bfcff547476c3ead6293389d10dba453888`, normalized community-health defaults and issue intake.
- `.github` PR [#3](https://github.com/dornglut/.github/pull/3), merge `badc25495b0703aa3bff9ec982d1dbec7fe07897`, adopted hardened reusable validation.
- The generic issue chooser contains `defect.yml`, `proposal.yml`, and `config.yml`.
- Repository-local issue-template directories own a complete local suite instead of relying on nonexistent directory merging.

### Reusable validation

- `github-workflows` PR [#5](https://github.com/dornglut/github-workflows/pull/5), merge `b6caad377102ca73794efaf734a65903b8efa829`, pinned third-party Actions to immutable revisions, added Dependabot for Actions, and hardened reusable Rust and Python validation.
- `github-workflows` PR [#7](https://github.com/dornglut/github-workflows/pull/7), merge `3cc9ad6c9bde3b970695baefa1cd815ff56111c7`, adopted reviewed `actions/checkout` v7.0.1 authority.
- Engineering PR [#8](https://github.com/dornglut/engineering/pull/8), merge `bec90d4e5b64c545029ff94d034758660fd20fe7`, proved the revised workflow through a canary.
- Reusable workflows retain `contents: read`, do not inherit secrets, do not persist checkout credentials, do not accept arbitrary commands, and do not write source.
- Each product or framework repository retains its canonical validation semantics.

### Repository conformance

- `runen-ui` PR [#24](https://github.com/dornglut/runen-ui/pull/24), merge `71eef30ee14e60e42052165034e209c4242399bc`, corrected active namespace authority, metadata, issue intake, root entrypoints, and repository-audit enforcement without product changes.
- `runenwerk` PR [#158](https://github.com/dornglut/runenwerk/pull/158), merge `6654da5d0e003208c5243efae2487f26a182f0ed`, adopted permanent hardened validation without architecture changes.
- `runen-sdf` PR [#6](https://github.com/dornglut/runen-sdf/pull/6), merge `711b2515378d5f85fe53e1083f44bf5adff2b05a`, completed the Rust-framework profile while preserving API, provenance, and standalone validation authority.

### Owner-attested merge and branch settings

All six maintained repositories use:

- squash as the only merge method;
- automatic deletion of merged head branches;
- an active repository-level `Protect main` ruleset targeting the default branch;
- pull requests before merge;
- zero required approvals during the solo-maintainer phase;
- conversation resolution;
- canonical validation;
- strict up-to-date branch testing;
- linear history;
- blocked force pushes and default-branch deletion;
- no routine bypass list.

Required checks:

| Repository | Required check |
|---|---|
| `runenwerk` | `Runenwerk validation / Repository baseline` |
| `runen-ui` | `RunenUI validation / Repository baseline` |
| `runen-sdf` | `Validate standalone framework / Repository baseline` |
| `engineering` | `validate / validate` |
| `.github` | `validate / validate` |
| `github-workflows` | `validate / validate` |

### Owner-attested custom properties

The organization-governed single-select properties are:

- `profile`: `organization-defaults`, `engineering`, `workflow-library`, `rust-framework`, `integration-product`, `template`;
- `lifecycle`: `planned`, `active`, `maintenance`, `archived`;
- `contribution`: `owner-only`, `discussion`, `open`.

Repository actors cannot reclassify these properties. They are not globally required and have no misleading default. Priority, milestones, releases, language, validation output, and current work were not duplicated into properties.

## Resolved default-branch enforcement anomaly

The first audit revision was created through the repository contents API directly on `engineering/main` at commit `beb515f9b19106e40e05bcf549e6af58c06d9d7c` after the initial ruleset setup.

The direct commit remains historical evidence and was not removed through history rewriting. The repository owner subsequently corrected the protection configuration and attested on 2026-07-26 that the unintended direct-write path was fixed.

The final audit correction and this closure revision were delivered through normal pull requests with exact-head `validate / validate` evidence. Future unexpected default-branch writes reopen the settings audit immediately.

## Deferred controls and residual risks

### Organization Actions policy

Status: deferred by owner decision on 2026-07-26.

Mitigations already present:

- reusable workflows explicitly declare read-only permissions;
- third-party Actions are pinned to immutable SHAs;
- checkout credentials are not persisted;
- no shared workflow accepts arbitrary commands, inherited secrets, or source-writing authority.

Residual risk: organization-wide allowlisting and default `GITHUB_TOKEN` restrictions are not independently standardized. A future workflow could be more permissive than current standards unless reviewed.

Review before:

- adding a new third-party Action;
- enabling deployment, release, publication, or source-writing workflows;
- accepting routine external pull requests;
- adding another organization member with write authority;
- external RunenGPU bootstrap.

### Organization security configuration

Status: deferred by owner decision on 2026-07-26.

Residual risk: organization-wide Dependabot alert and security-update coverage, CodeQL default setup, secret scanning, push protection, and private vulnerability reporting were not standardized and attested across all maintained repositories.

Review before:

- a public release or package publication;
- processing credentials, user data, network services, or untrusted files;
- accepting routine external contributions;
- the first externally consumed Runen framework release;
- external RunenGPU bootstrap.

### Labels and unused repository features

Status: optional cleanup, not a normalization blocker.

Dornglut deliberately does not duplicate Portfolio status, priority, or kind through labels. Unused default labels and repository features may be removed when they create actual ambiguity or maintenance cost.

## Template disposition

The future Rust framework template is a bootstrap mechanism, not ongoing synchronization authority.

Its activation and acceptance criteria are owned by [engineering issue #9](https://github.com/dornglut/engineering/issues/9). It remains `planned` until internal RunenGPU G1–G8 is closed and external RunenGPU extraction is explicitly authorized.

## Acceptance assessment

| Acceptance condition | Result |
|---|---|
| No active authority requires ForgeOps | Pass |
| Ideas and accepted work have separate Project surfaces | Pass, owner-attested Project configuration |
| Organization defaults and local template overrides are explicit | Pass |
| Repository profiles are defined and assigned | Pass, owner-attested native properties |
| Squash-only merge settings are consistent | Pass, owner-attested native settings |
| Default-branch protection is corrected | Pass, owner-attested resolution on 2026-07-26 |
| Shared workflows are read-only and immutable | Pass, repository and CI evidence |
| Active identity uses `dornglut/*` outside explicit history | Pass |
| Maintained repositories have canonical validation and truthful entrypoints | Pass |
| Organization Actions policy standardized | Deferred residual risk |
| Organization security configuration standardized | Deferred residual risk |
| Dated audit records revisions, settings, exceptions, and triggers | Pass |

## Closure

Close engineering issue #4 after this revision passes exact-head validation and merges.

Do not keep the completed normalization program open for the future Rust framework template; issue #9 owns that triggered work.

The next active product path is Runenwerk's RunenGPU sequence. Revisit organization governance only when a recorded review trigger becomes true or material drift is detected.
