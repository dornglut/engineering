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

Repository-specific issue forms are justified only by a real local work model, such as RunenUI roadmap-milestone slices.

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
- accepted base when relevant;
- reviewed feature head;
- exact-head validation run or status;
- outcome;
- included and excluded scope;
- API, security, migration, and documentation impact.

When recording completed delivery, it also identifies the accepted squash merge and accepted-main push evidence when that repository requires it. A merge ref is reported only when intentionally describing merge-result validation; it must not be called the reviewed feature head. Moving the feature head invalidates prior exact-head evidence.

Pull requests remain bounded. Merge uses exact-head evidence.

## Projects

The private Inbox and public Engineering Portfolio follow the semantic contract in [Authority and work](../governance/authority-and-work.md).

Projects own live operational state. They do not replace ADRs, repository issues, roadmaps, or source.

## Parent issues and child links

A parent issue is the optional repository-local operational representation of one accepted roadmap milestone or multi-phase outcome. Use it only when:

- the same repository owns the current behavior or migration boundary;
- at least two accepted child issues or delivery slices are required;
- sequencing or an explicit final gate matters;
- one ordinary issue would either become unbounded or duplicate multiple child scopes.

Create the parent when the first child slice is accepted, not merely to reserve a future framework or extraction name. Planned work with no accepted child slice remains in the roadmap or private Inbox.

The parent body maintains one concise linked slice index. Each child issue links back to the parent. The agent or tool that creates a child issue must update the parent index in the same workflow so the owner is not left with recurring manual setup.

GitHub's native parent/sub-issue relationship is optional. Use it when the active tool can create and maintain it directly without extra owner work. Do not make a manual native-linking operation a prerequisite for accepted work, and do not treat native relationship metadata as more authoritative than the linked parent and child issue bodies.

The parent issue owns:

- the roadmap milestone or program outcome and repository boundary;
- the concise linked slice index;
- durable links to the roadmap and accepted decisions;
- sequencing constraints and major gates;
- explicit non-goals;
- the final closure condition.

Child issues own exact investigation or implementation scope, acceptance criteria, validation, migration evidence, and closeout. The parent must not copy child acceptance criteria, current priority or status, pull-request inventories, workflow runs, temporary blockers, or exact-head evidence.

Close the parent only after its final accepted gate. Do not close it merely because one early slice completes.

## GitHub milestones

GitHub Milestone objects are repository-local groupings of issues and pull requests with a description, optional due date, and automatic completion percentage.

Dornglut reserves them for a real repository-local release or shipping target, for example:

```text
runen-ui v0.2
runen-sdf v0.1
application beta
website launch
```

Do not create a GitHub milestone for:

- an internal architecture phase;
- a roadmap milestone already represented by a parent issue and linked child issues;
- extraction readiness;
- an indefinite backlog or topic;
- a cross-repository program.

A milestone description states the release or shipping outcome and exit criteria. GitHub owns its associated issue and pull-request inventory and completion percentage. Do not repeat that inventory in the description or durable Markdown.

Use a due date only when a genuine dated commitment exists. Do not copy milestone membership or completion into Project custom fields or repository custom properties.

Completed historical work does not receive retrospective parent issues or milestones unless an unresolved operational need requires them.

## Cross-repository programs

A repository-local parent may begin before an extraction crosses repository boundaries. Once work requires coordinated delivery in two or more repositories, apply the initiative criteria in [Authority and work](../governance/authority-and-work.md).

A qualifying engineering initiative provides the durable cross-repository charter, sequencing, rollback, and closure evidence. It links repository-local parent and child issues; it does not replace their roadmaps, implementation scope, Projects, or pull requests.

Native cross-repository sub-issue links may support navigation when tooling can maintain them without extra owner work, but they do not remove the requirement for an initiative when the accepted initiative criteria are met.

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
