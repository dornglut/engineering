# Dornglut organization normalization audit — 2026-07-26

- Observation date: 2026-07-26
- Owning program: [engineering issue #4](https://github.com/dornglut/engineering/issues/4)
- Governing decision: [ADR 0004](../adrs/0004-organization-work-and-repository-standardization.md)
- Scope: organization governance, GitHub operating surfaces, repository profiles, inherited defaults, reusable validation, and maintained-repository conformance
- Evidence class: dated audit; this report records observed and owner-attested state but does not replace durable standards or repository-local authority

## Executive conclusion

Dornglut's repository and governance normalization is substantially complete. The organization now has:

- separate private idea capture and public accepted-work tracking;
- normalized `.github`, `engineering`, and `github-workflows` authorities;
- active `dornglut/*` identity across maintained repositories;
- complete inherited and repository-local issue intake;
- immutable, read-only reusable validation;
- explicit repository profiles through custom properties;
- owner-attested squash-only merge settings and `Protect main` rulesets;
- repository-local implementation, validation, roadmap, and release authority.

The program must not close yet because this audit process exposed one concrete enforcement anomaly: the connected GitHub App successfully wrote the first revision of this report directly to `engineering/main` at commit `beb515f9b19106e40e05bcf549e6af58c06d9d7c`, despite the owner-attested pull-request requirement and empty bypass list.

That direct write is preserved as historical evidence. It must not be erased through force push or default-branch rewriting. The cause must be resolved or explicitly accepted before engineering issue #4 is closed.

The organization Actions policy and organization security configuration are also deliberately deferred. They are recorded as residual risks with explicit review triggers rather than represented as completed controls.

The Rust framework template is not unfinished normalization work. It is tracked separately in [engineering issue #9](https://github.com/dornglut/engineering/issues/9) and must activate only immediately before external RunenGPU bootstrap.

## Audited repositories

| Repository | Profile | Lifecycle | Contribution | Role |
|---|---|---|---|---|
| `dornglut/.github` | `organization-defaults` | `active` | `owner-only` | Community-health defaults, issue forms, PR guidance, workflow templates |
| `dornglut/engineering` | `engineering` | `active` | `owner-only` | Organization governance, standards, ADRs, shared architecture, initiatives, reports |
| `dornglut/github-workflows` | `workflow-library` | `active` | `owner-only` | Reusable read-only CI orchestration |
| `dornglut/runenwerk` | `integration-product` | `active` | `discussion` | Integration platform and reference engine |
| `dornglut/runen-ui` | `rust-framework` | `active` | `discussion` | Standalone host-neutral UI framework |
| `dornglut/runen-sdf` | `rust-framework` | `active` | `discussion` | Standalone signed-distance-field framework |

All six repositories were connector-verified as public, unarchived, and using `main`. Native GitHub settings that are unavailable through the connected API are recorded as owner-attested rather than falsely described as API-verified.

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
- Projects V2 internals remain owner-attested because the connected API does not expose their visibility, fields, views, workflows, or item values.

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

The repository owner attested that all six maintained repositories now use:

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
- an empty routine bypass list.

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

## Default-branch enforcement anomaly

The first report revision was created through the repository contents API directly on `engineering/main` at commit `beb515f9b19106e40e05bcf549e6af58c06d9d7c` after the `Protect main` ruleset was configured.

The successful write proves that the accepted protection is not yet fully demonstrated for the connected GitHub App. Possible explanations include a nonmatching or inactive ruleset, an app or role bypass, or provider behavior not represented by the visible configuration. This report does not select a cause without native evidence.

Required correction:

1. inspect `engineering` → Settings → Rules → Rulesets → `Protect main`;
2. confirm enforcement is `Active` and target preview includes `main`;
3. inspect the bypass list and rule insights for commit `beb515f9b19106e40e05bcf549e6af58c06d9d7c`;
4. remove any routine administrator, role, integration, or GitHub App bypass that is not explicitly required;
5. prove the rule with a harmless direct update that GitHub rejects;
6. deliver the accepted report correction through a normal PR that passes `validate / validate`.

The direct commit remains historical evidence and must not be removed through history rewriting.

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

Residual risk: organization-wide Dependabot alert/security-update coverage, CodeQL default setup, secret scanning, push protection, and private vulnerability reporting were not standardized and attested across all maintained repositories.

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
| Default-branch PR enforcement rejects direct App writes | **Fail: direct write succeeded** |
| Shared workflows are read-only and immutable | Pass, repository and CI evidence |
| Active identity uses `dornglut/*` outside explicit history | Pass |
| Maintained repositories have canonical validation and truthful entrypoints | Pass |
| Organization Actions policy standardized | Deferred residual risk |
| Organization security configuration standardized | Deferred residual risk |
| Dated audit records revisions, settings, exceptions, and triggers | Pass after reviewed correction PR |

## Closure recommendation

Do not close engineering issue #4 until the default-branch enforcement anomaly is corrected or explicitly accepted and this report correction is validated through a normal pull request.

After that proof, close #4. Do not keep it open for the future Rust framework template; issue #9 owns that triggered work.

The next active product path remains Runenwerk's RunenGPU sequence. Revisit organization governance only when a recorded review trigger becomes true or material drift is detected.
