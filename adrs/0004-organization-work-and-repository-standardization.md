# ADR 0004: Organization work and repository standardization

- Status: accepted
- Date: 2026-07-24
- Owner: Dornglut organization
- Scope: organization-wide work intake, priority, repository profiles, and documentation authority

## Context

Dornglut now contains organization repositories, an integration platform, standalone frameworks, and planned extractions. The initial governance bootstrap correctly separated `.github`, `engineering`, `github-workflows`, and product authority, but several operational questions remained underspecified.

Raw ideas, accepted work, priorities, roadmaps, status documents, initiatives, and pull requests risked becoming overlapping trackers. Repository roots and documentation used similar concepts with inconsistent paths. Organization defaults could also conflict with local contribution policies or be silently disabled by local issue-template directories.

A scalable model must make idea capture inexpensive, keep accepted work reviewable, centralize only genuinely shared policy, and avoid a synchronization platform or duplicated live-state documents.

## Decision

Dornglut adopts the following work model:

- undeveloped ideas live as draft items in a private organization Project named `Dornglut Inbox`;
- accepted investigation and delivery work live as issues in the repository that owns the behavior;
- accepted cross-repository priority and execution state live in a public Project named `Dornglut Engineering Portfolio`;
- durable long-term sequence lives in repository roadmaps;
- product maturity lives in repository status documents;
- durable local decisions live in repository ADRs;
- durable cross-repository decisions live in `dornglut/engineering` ADRs;
- initiatives are optional and used only for large multi-repository programs that need sequencing, rollback, and closure evidence;
- pull requests and exact-head CI own implementation evidence.

Dornglut adopts repository profiles for organization defaults, engineering policy, workflow libraries, Rust frameworks, integration products, and templates. Profiles normalize ownership and entrypoint semantics without requiring identical internal directory trees.

Organization centralization is limited to:

- community-health defaults and workflow templates in `.github`;
- governance, standards, shared architecture, ADRs, and qualifying initiatives in `engineering`;
- reusable read-only CI orchestration in `github-workflows`.

Product and framework repositories retain code, tests, public contracts, validation semantics, releases, local architecture, roadmaps, status, and issues.

Current GitHub custom properties, when configured, are limited to `profile`, `lifecycle`, and `contribution`. Dornglut will not introduce a parallel checked-in repository manifest unless a future concrete validation need cannot be met through repository-local authority and GitHub settings.

The default public issue chooser contains only generic defect and proposal forms. Maintainer delivery issues may use a structured body without adding another public form. A repository with a local issue-template directory owns a complete accepted local suite.

Changing GitHub priority, branch, PR, assignee, or workflow-run state is not copied into durable Markdown.

## Alternatives considered

### One public backlog for ideas and accepted work

Rejected. It would expose incomplete thoughts, pollute accepted delivery state, and encourage premature issue creation.

### Markdown priority and idea documents

Rejected. They would duplicate live GitHub state and become stale.

### One identical repository tree

Rejected. Consistent authority and entrypoints are valuable; identical physical layouts would distort different products and documentation systems.

### A checked-in organization repository manifest

Deferred. It adds synchronization cost before a demonstrated machine-validation need exists. GitHub custom properties and repository-local validation are sufficient for the current scale.

### Remove initiatives entirely

Rejected. Most work does not need an initiative, but genuine multi-repository migrations may need a durable program charter beyond an ADR and individual issues.

### Elaborate scoring and planning fields

Rejected. RICE, WSJF, story points, confidence, effort, and date fields create administration without current decision value.

## Consequences

- ideas can be captured without polluting issue trackers;
- public priority contains accepted work only;
- roadmaps and status documents remain durable rather than operational mirrors;
- repository differences become explicit profile choices instead of accidental drift;
- local issue-template overrides must be complete and validated;
- organization standards remain small enough to audit;
- Project configuration still requires native GitHub administration when no reviewed API surface is available;
- future growth can add fields or profiles through evidence-backed changes rather than speculative structure.

## Affected repositories

- `dornglut/.github`
- `dornglut/engineering`
- `dornglut/github-workflows`
- `dornglut/runenwerk`
- `dornglut/runen-ui`
- `dornglut/runen-sdf`
- planned RunenGPU, RunenRender, and RunenECS repositories

## Adoption or migration

1. Normalize `dornglut/engineering` and establish the Project semantic contract.
2. Configure the private Inbox and public Engineering Portfolio through the native GitHub interface and record the evidence.
3. Normalize `.github` defaults and issue intake.
4. Harden `github-workflows`.
5. Audit GitHub settings and apply repository properties.
6. Correct active namespace and issue-template authority in RunenUI.
7. Conform Runenwerk and RunenSDF without homogenizing their product documentation.
8. Create a Rust framework template immediately before RunenGPU bootstrap.
9. Publish a dated organization-normalization audit.

Implementation is owned by [engineering issue #4](https://github.com/dornglut/engineering/issues/4).

## Supersedes

None.

## Superseded by

None.
