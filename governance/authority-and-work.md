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

## Material review reconciliation

A material finding records a stable finding ID, the exact reviewed revision, severity,
owning issue or pull request, and its required correction or accepted disposition. The
finding ID persists across corrected revisions. A moved feature head makes the earlier
approval or rejection stale for acceptance, not historical evidence: record the same
finding ID and disposition on the corrected head, then bind an independent re-review
verdict to that new exact revision.

| Route | Observable trigger | Required record |
|---|---|---|
| Correct inside the current issue | The implementation misses accepted criteria, violates current scope or ownership, needs material acceptance-proof clarification, or remains necessary for the same authorized outcome. | Concisely project the correction into the issue when criteria, proof, or scope materially changes; do not copy the full review. |
| Correct in the current PR only | The correction plainly fits unchanged issue criteria, changes no durable contract or scope interpretation, and creates no independently schedulable work. | Keep the finding ID and reviewed revision visible in review evidence. |
| Create a separate follow-up issue | The finding is outside authorized scope, independently deliverable, owned by a distinguishable component or repository, and not required for truthful acceptance. | Record its relationship or dependency. A blocking correctness, ownership, security, or acceptance defect is never relabelled as follow-up to permit merge. |
| Update ADR or durable design authority | The correction changes a durable architecture decision, public or cross-repository contract, ownership boundary, long-term tradeoff, or accepted invariant. | The current issue or PR still owns the active correction until that authority is accepted. |
| Report-only | The observation needs no current correction, changes no acceptance criterion, creates no accepted follow-up, and exists only as historical or audit evidence. | Keep it historical; reports do not silently authorize work. |

For example: a failed current acceptance criterion is corrected in its issue; a newly
found architecture-boundary conflict also updates the ADR or accepted design; a useful
non-blocking out-of-scope enhancement becomes a related follow-up; a corrected head
keeps the same finding ID and receives a new exact-head verdict; and an observation
with no required action remains report-only. This is routing guidance, not a generated
task database, truth certificate, mandatory closeout report, or duplicate exact-head
ledger.

## Post-merge closure reconciliation

After accepted merge, check whether delivery changed current behavior or capability,
maturity or support status, architecture or ownership, roadmap sequence or dependency,
parent or current-child state, acceptance criteria discovered during review, initiative
lifecycle, repository-family membership, or compatibility and deletion obligations.
Update only affected authority.

Normal closure requires neither a separate closeout pull request, copied exact-head
ledgers in durable Markdown, process-only activation artifacts, generated prompts, nor
a second workflow-state database. A separate authority-reconciliation pull request is
permitted when it contains independently reviewable authority changes.

## Continuation and work selection

When a specific accepted issue has been selected for continuation, re-establish that
issue and any pull request delivering it from current repository state. Continue it
when its ownership, dependencies, assumptions, and acceptance boundary remain valid.
Changes accepted since its recorded base require broader reconsideration only when they
can affect those properties or current mergeability.

When no specific accepted work has been selected and an executor must choose further
nontrivial work, establish that choice from current accepted authority rather than
automatically following a prior plan, report, review conclusion, handoff, or proposed
sequence.

Inspect only as broadly as necessary to establish the accepted implementation state,
relevant accepted work, applicable roadmap or dependency constraints, canonical
ownership and direct dependencies, and relevant implementation, validation,
verification, or accepted-decision evidence. Consult Portfolio priority when choosing
among otherwise eligible accepted work.

A previously proposed next action is a hypothesis until current authority still
demonstrates its need. An unresolved, incomplete, deferred, or potentially useful
concern does not by itself justify immediate work.

When current authority establishes a material question but not a decision-complete
implementation boundary, route it to investigation rather than inventing a delivery
slice.

Work selection may resume existing accepted work, justify bounded new investigation or
delivery work, leave a concern deferred in its existing authority, or establish that no
further work is currently justified. In the latter case, stop autonomous continuation
and report that result.

Broaden the investigation only when necessary because of a phase-boundary question,
ownership conflict, stale authority, migration dependency, or cross-repository
consequence. Parallel work remains governed by the existing parallel-track rules.

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

Dornglut has no organization-wide numeric cap on active product, framework, or maintenance tracks. The Engineering Portfolio owns live priority and status; concurrency is governed by explicit ownership, dependencies, write conflicts, validation, and review capacity.

Parallel tracks are permitted only when each track:

- is owned by an accepted issue with bounded scope and stop conditions;
- has one clear repository, branch, workspace, and writer authority;
- begins from an explicit accepted revision;
- does not treat an unmerged branch as accepted dependency authority;
- does not write the same files or durable authority surfaces as another track without an explicit rebase or serialization plan;
- retains independent repository validation, review, and acceptance;
- does not create duplicate implementation, roadmap, or decision authority.

The following work remains serialized unless an accepted issue defines and proves a safe staged migration:

- writes to the same branch, workspace, file set, or mutable runtime state;
- shared root manifests and lockfiles;
- organization policy and repository-family architecture;
- protected workflow and validation changes;
- source extraction, transfer, deletion, and consumer cutover;
- dependency or public-contract transitions that require coordinated acceptance.

When parallel tracks become difficult to review, repeatedly conflict, or obscure the critical path, reduce concurrency through Portfolio priority and explicit issue status rather than a universal count.

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
