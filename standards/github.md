# GitHub standard

This standard defines Dornglut's use of GitHub as the current forge without making GitHub the owner of product behavior or durable architecture.

## Organization defaults

`dornglut/.github` supplies defaults only when a repository does not override the corresponding file.

The default suite should remain small:

- conservative contribution guidance;
- code of conduct;
- security and support routing;
- one pull-request template;
- `defect.yml`;
- `proposal.yml`;
- `config.yml`;
- workflow templates for thin CI callers.

A repository with any local `.github/ISSUE_TEMPLATE` files must provide its complete accepted suite because GitHub does not merge local and organization issue-template directories.

Repository-specific issue forms are justified only by a real local work model, such as RunenUI milestone slices.

## Contribution modes

Every maintained repository uses one of these modes:

| Mode | Meaning |
|---|---|
| owner-only | Maintainers own changes; public issues may still be available |
| discussion | External discussion and proposals are welcome; code starts only after explicit maintainer authorization |
| open | Normal external issue and pull-request contributions are accepted |

The inherited default is conservative: do not begin a code contribution unless the repository explicitly accepts it or a maintainer authorizes the work.

## Issue intake

### Defect

Use when observed behavior violates an existing contract.

Capture:

- repository and revision;
- observed and expected behavior;
- deterministic reproduction;
- environment;
- evidence and impact;
- security confirmation.

### Proposal

Use for capability, architecture, documentation, tooling, or research proposals.

Capture:

- proposal type;
- concrete problem;
- desired observable outcome;
- evidence or motivation;
- scope and non-goals;
- owning repository or affected repositories.

Undeveloped ideas belong in the private Dornglut Inbox, not repository issue trackers.

Maintainer delivery issues may use a structured body without appearing as a public issue-form choice.

## Pull requests

A pull request identifies:

- owning issue or decision;
- implementation base when relevant;
- reviewed head or merge ref;
- outcome;
- included and excluded scope;
- validation evidence;
- API, security, migration, and documentation impact.

Pull requests remain bounded. Merge uses exact-head evidence.

## Projects

The private Inbox and public Engineering Portfolio follow the semantic contract in [Authority and work](../governance/authority-and-work.md).

Projects own live operational state. They do not replace ADRs, repository issues, roadmaps, or source.

## Repository properties

When GitHub custom properties are available, use only:

- `profile`: organization-defaults, engineering, workflow-library, rust-framework, integration-product, template;
- `lifecycle`: planned, active, maintenance, archived;
- `contribution`: owner-only, discussion, open.

Do not copy priority, milestones, current work, validation results, or release state into custom properties.

## Repository settings target

For maintained repositories:

- default branch `main`;
- squash merge enabled;
- merge commits and rebase merge disabled unless a repository records a specific reason;
- merged head branches deleted automatically;
- normal changes require pull requests;
- canonical validation is required;
- conversations are resolved before merge;
- force pushes and default-branch deletion are blocked;
- linear history is preferred;
- bypass is narrowly restricted.

A solo-maintainer repository should not require meaningless approval counts. Review quality comes from bounded scope, independent validation, explicit acceptance, and exact-head merge protection.

Organization-level rulesets may target repository profiles when the GitHub plan supports them. Otherwise, import the same accepted repository ruleset separately.

## Labels

Do not duplicate Portfolio priority or status through labels.

Add an organization label vocabulary only after repeated usage demonstrates stable needs. Prefer a small type or decision vocabulary over a large taxonomy.

## Security

The organization security policy provides a default route. A repository keeps a local `SECURITY.md` when its supported versions, disclosure boundary, or response process differs materially.

Validation and reusable workflows use least privilege and remain source-read-only.
