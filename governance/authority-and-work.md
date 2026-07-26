# Authority and work

Dornglut uses explicit authorities so ideas, plans, GitHub state, automation, and implementation do not compete as parallel sources of truth.

## Authority by question

| Question | Authority |
|---|---|
| What does the software currently do? | Code and tests in the owning repository |
| What must pass before merge? | The owning repository's canonical validation command |
| Where does an undeveloped idea go? | A draft item in the private Dornglut Inbox |
| What investigation or implementation work is accepted? | An issue in the repository that owns the behavior |
| What coordinates a roadmap milestone or multi-phase outcome within one repository? | An optional parent issue with linked child issues |
| What is currently prioritized or active? | The public Dornglut Engineering Portfolio |
| What is the durable long-term sequence? | The owning repository's roadmap |
| What is the current product maturity? | The owning repository's status document |
| What local architecture is durable? | An accepted repository ADR |
| What cross-repository decision is durable? | An accepted ADR in this repository |
| What large outcome genuinely spans repositories? | An optional initiative in this repository with linked local issues |
| What changed in a delivery? | The pull request and its exact-head validation evidence |
| What defaults apply when a repository is silent? | `dornglut/.github` |
| How is shared CI orchestrated? | `dornglut/github-workflows` |
| What happened historically? | Git history, provenance, or a dated report |

## Work lifecycle

```text
raw thought
    -> private Dornglut Inbox draft item
    -> review
        -> drop
        -> retain as an idea
        -> repository investigation issue
        -> repository delivery issue

accepted issue
    -> public Engineering Portfolio
    -> bounded pull request
    -> exact-head validation
    -> review and merge
    -> closed issue and completed Project item
```

A raw idea requires only a useful title, a short statement of the possibility or problem, and an optional area or link. It must not require acceptance criteria, implementation scope, architecture, estimates, or priority.

An idea becomes a repository issue only when it needs investigation, affects an accepted roadmap, blocks a decision, has a plausible delivery horizon, or requires durable discussion and evidence.

## Parent issues and roadmap milestones

A repository-local parent issue is the optional operational representation of one accepted roadmap milestone or multi-phase outcome in the repository that owns the current behavior or migration boundary.

The parent body maintains one concise linked slice index, and each child issue links back to the parent. Native GitHub parent/sub-issue relationships may be added when the active tool can maintain them directly without extra owner work, but they are not required authority. The creator of a child issue must also update the parent index through the available tool.

The parent issue owns the outcome, boundary, sequencing constraints, major gates, and final closure condition. Child issues own exact investigation or implementation scope. The repository roadmap owns durable sequence, and the Engineering Portfolio owns live priority and status.

Do not create a parent issue merely to reserve a future name. Activate it when the first child slice is accepted. Do not copy child acceptance criteria, Project fields, pull-request state, or validation evidence into the parent body.

The parent closes only after its final accepted gate. GitHub Milestone objects are not a second hierarchy for internal technical phases; Dornglut reserves them for real repository-local release or shipping targets. Work that crosses repositories may require an engineering initiative under the criteria below; the initiative links repository-local issues rather than replacing them.

## Projects

### Dornglut Inbox

The Inbox is private and contains undeveloped ideas as Project draft items.

Its semantic fields are:

- `State`: Captured, Reviewing, Promoted, Dropped;
- `Area`: Unassigned, Runenwerk, RunenUI, RunenSDF, GPU, Render, ECS, Organization.

Raw ideas have no priority. The Inbox must not become a second implementation tracker.

### Dornglut Engineering Portfolio

The Portfolio is public and contains accepted issues and pull requests.

Its semantic fields are:

- `Status`: Ready, In progress, Blocked, Done;
- `Priority`: P0, P1, P2, P3, or blank;
- `Kind`: Decision, Investigation, Delivery, Maintenance.

A `Target` field may be added only when real release or dated delivery targets exist.

Do not duplicate GitHub's repository, assignee, milestone, issue state, subissue, dependency, or relationship data through custom fields.

Project configuration is operational state. It may change without rewriting architecture, but it must remain consistent with this semantic contract.

## Priority

| Priority | Meaning |
|---|---|
| P0 | Immediate security, data-loss, published-contract, or default-branch integrity failure |
| P1 | Current critical path or blocker for accepted work |
| P2 | Accepted and queued work |
| P3 | Accepted work deliberately deferred |
| blank | Not prioritized or still under triage |

When priorities are equal, prefer work that:

1. unblocks more accepted work;
2. removes correctness, security, or ownership risk;
3. removes duplicate authority or transitional infrastructure;
4. delivers a usable capability;
5. has the smaller coherent delivery boundary.

Do not introduce weighted scoring, story points, confidence percentages, or impact formulas without repeated evidence that the simpler model is insufficient.

For the current single-maintainer operating mode, keep no more than two product or framework tracks and one organization-maintenance track active. Reassess this limit when contributor capacity changes.

## Initiatives

An initiative is optional. Use one only when all of these conditions hold:

- at least two repositories are affected;
- multiple local issues or delivery phases are required;
- sequencing or migration order matters;
- rollback or closure evidence matters;
- one engineering issue cannot represent the outcome clearly.

An initiative does not replace repository issues, ADRs, the Portfolio, or pull requests.

## Precedence

More specific accepted authority overrides a broader default. Implementation cannot be overruled by a stale plan, and live Project state cannot silently change a durable architectural decision.

When authorities disagree:

1. stop work that depends on the conflict;
2. identify whether behavior, validation, local architecture, or organization policy is disputed;
3. correct the authority that owns that question;
4. record migration consequences;
5. resume implementation from an explicit accepted base.

## Durable versus operational state

Durable Markdown must not mirror:

- current branches or head SHAs;
- open pull-request inventories;
- workflow-run identifiers;
- current assignees;
- live priority order;
- temporary blockers;
- copied Project fields.

Old owner paths, superseded decisions, and completed work may remain in provenance, ADRs, initiatives, and reports when clearly historical. They must not be used as active implementation authority.
