# GitHub standard

This standard defines Dornglut's use of GitHub as the current forge without making
GitHub the owner of product behavior, repository classification, work semantics,
validation semantics, or durable architecture.

## Organization defaults

`dornglut/.github` supplies defaults only when a repository does not override the
corresponding file.

The default suite should remain small:

- conservative contribution guidance;
- code of conduct;
- security and support routing;
- one pull-request template;
- `defect.yml`;
- `proposal.yml`;
- `config.yml`;
- workflow templates for thin CI callers.

A repository with any valid local `.github/ISSUE_TEMPLATE` templates or configuration
must provide its complete accepted suite because GitHub does not merge that local suite
with the organization default issue-template directory.

Repository-specific issue forms are justified only by a real local work model.

## Contribution modes

The canonical contribution identifiers are defined by the
[Repository standard](repositories.md). Their GitHub contribution meaning is:

| Mode | Meaning |
|---|---|
| owner-only | Maintainers own changes; public issues may still be available |
| discussion | External discussion and proposals are welcome; code starts only after explicit maintainer authorization |
| open | Normal external issue and pull-request contributions are accepted |

The inherited default is conservative: do not begin a code contribution unless the
repository explicitly accepts it or a maintainer authorizes the work.

## Issue intake

### Defect

Use when observed behavior violates an existing contract.

Capture:

- repository and revision;
- observed and expected behavior;
- reproduction steps when available, otherwise the smallest bounded evidence of
  occurrence, including triggering conditions, frequency, or known nondeterminism;
- relevant environment;
- evidence and practical impact;
- confirmation that ordinary issue content does not disclose a vulnerability,
  credential, or private data.

Security vulnerabilities and other private disclosures use the security reporting
route rather than an ordinary defect issue.

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

Maintainer delivery issues may use a structured body without appearing as a public
issue-form choice.

## Pull requests

A pull request identifies:

- owning issue or decision;
- accepted base when relevant;
- reviewed feature head;
- exact-head validation run or status;
- outcome;
- included and excluded scope;
- API, security, migration, and documentation impact.

When recording completed delivery, it also identifies the accepted squash merge and
accepted-main push evidence when that repository requires it. An ordinary pull-request
merge ref is reported only when intentionally describing synthetic merge-result
validation; it must not be called the reviewed feature head. A merge-queue integration
revision is reported as `merge_group` evidence and likewise must not be called the
reviewed feature head. Moving the feature head invalidates prior exact-head evidence.

Pull requests remain bounded. Merge uses exact-head evidence.

## Agent-mediated repository changes

Agent-mediated changes use one exact accepted base, one complete isolated candidate,
exact-head validation, and guarded acceptance. The publication parent is the accepted
base for initial work and the exact previous feature head for a correction.

1. Read current repository authority and record the exact accepted default-branch
   commit and tree.
2. Select an executor capable of the required inspection and of establishing the
   evidence that the applicable executor procedure requires before publication. Do not
   infer a pre-publication execution requirement merely because compilation, tests, or
   runtime execution are eventually required for acceptance. The executor-specific
   procedure defines when execution may first occur after publication. If required
   inspection or pre-publication evidence cannot be established through that procedure,
   use a suitable checked-out executor. GPT Web work follows the
   [GPT Web GitHub procedure](../tooling/gpt-web-github.md).
3. Treat exact revision-bound repository inventory and file contents as authoritative
   state. Search may aid discovery but does not prove absence or dependency closure.
4. Read every modified existing file completely from the exact publication parent.
5. Audit material dependency closure before editing. Do not modify unauthorized paths;
   amend the owning authority first when additional scope is proven necessary.
6. Construct the complete candidate off-ref. Initial work parents the accepted base;
   corrections parent the exact previous feature head. Keep the lineage linear.
7. Before publication, verify publication-parent-to-candidate and
   accepted-base-to-candidate diffs against authorized scope.
8. Re-resolve default and feature refs immediately before publication. Material
   default-branch drift requires a new accepted base and new publication lineage.
   Unexpected feature-head movement is a stop condition.
9. Publish new work by creating an isolated branch directly at the complete candidate.
   Update an existing lineage only by guarded non-force fast-forward. Never expose
   partial candidate state or force-overwrite unexpected branch state.
10. Use a draft pull request and repository-owned exact-head validation. CI may falsify
    a candidate but does not expand scope.
11. Any feature-head change invalidates earlier validation, review, and assurance.
12. Before direct merge or queue enqueue, reconcile the exact final feature head with
    authority, dependency closure, complete diff, CI, review state, and current default
    branch. Accept or enqueue only that exact reviewed feature-head SHA.
13. In a merge-queue-enabled repository, require the queue's exact `merge_group`
    integration revision to satisfy the repository's required queue checks before
    merge. Treat feature-head and merge-group results as separate evidence stages even
    if the queue later promotes the validated integration commit directly.
14. After merge, verify the resulting default-branch state where repository acceptance
    rules require it.

Executor-specific procedures define supported mechanics without weakening these
invariants. Canonical and exact-revision evidence remain owned by the
[Validation standard](validation.md).

Blind rebasing of stale candidates, sequential writes that expose partial candidate
state, search results presented as completeness proof, force-overwriting unexpected
feature state, and model assessment presented as executable validation are not
accepted substitutes for this workflow.

## Projects

The private Inbox, Engineering Portfolio, priority semantics, and work lifecycle are
owned by [Authority and work](../governance/authority-and-work.md).

GitHub Projects represent live operational state. They do not replace ADRs, repository
issues, roadmaps, source, or repository-local implementation authority.

## Parent issues and child links

[Authority and work](../governance/authority-and-work.md#parent-issues-and-roadmap-milestones)
owns parent/child eligibility, ownership, sequencing, and closure.

GitHub issue bodies retain the durable parent/child links. Native parent/sub-issue
relationships are optional navigation and must not outrank the owning issue bodies.

## GitHub milestones

[Authority and work](../governance/authority-and-work.md#parent-issues-and-roadmap-milestones)
owns milestone eligibility and purpose.

A milestone description states the release or shipping outcome and exit criteria. Use
a due date only when a genuine dated commitment exists. GitHub owns the associated
issue/PR inventory and automatic completion percentage; do not copy that live inventory
or completion state into durable Markdown or Project custom fields.

Completed historical work does not receive a retrospective milestone unless an
unresolved operational need requires one.

## Cross-repository programs

[Authority and work](../governance/authority-and-work.md#initiatives) owns initiative
criteria, authority, and closure.

Native cross-repository relationships are optional navigation. They do not replace
owning repository issues or a required initiative.

## Repository properties

GitHub repository custom properties mirror the canonical `profile`, `lifecycle`,
and `contribution` classifications owned by the
[Repository standard](repositories.md#repository-profiles). GitHub property values
must use those canonical identifiers rather than introduce a second classification
vocabulary.

Do not copy priority, milestones, current work, validation results, release state, or
other live work-management data into repository custom properties.

## Repository settings target

For maintained repositories:

- default branch `main`;
- squash merge enabled;
- merge commits and rebase merge disabled unless a repository records a specific
  reason;
- merged head branches deleted automatically;
- normal changes require pull requests;
- canonical validation is a required status check;
- repositories may require additional status or evidence checks when their owning
  validation or acceptance authority requires them;
- repositories without a required merge queue use strict/up-to-date required status
  checks so merge eligibility is tested against the current default-branch state;
- a merge-queue repository may disable strict required-status checking only when its
  required `merge_group` checks validate the exact latest-base integration revision
  before merge; the queue does not waive required checks or exact-revision evidence;
- conversations are resolved before merge;
- force pushes and default-branch deletion are blocked;
- linear history is preferred;
- bypass access is minimized; ordinary changes must not use bypass to evade required
  validation, integration, review, or acceptance evidence. Emergency recovery outside
  the ordinary path requires explicit authority and post-action reconciliation.

A solo-maintainer repository should not require meaningless approval counts. Review
quality comes from bounded scope, independent validation, explicit acceptance, and
exact-head merge protection.

Organization-level rulesets may target repository profiles when the GitHub plan
supports them. Otherwise, import the same accepted repository ruleset separately.

## Labels

Do not duplicate Portfolio priority or status through labels.

Add an organization label vocabulary only after repeated usage demonstrates stable
needs. Prefer a small type or decision vocabulary over a large taxonomy.

## Security

The organization security policy provides a default route. A repository keeps a local
`SECURITY.md` when its supported versions, disclosure boundary, or response process
differs materially.

Validation and reusable workflows use least privilege and remain source-read-only.
