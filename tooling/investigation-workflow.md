# Investigation and audit workflow

Reusable **method guidance** for a bounded, accepted Dornglut investigation or audit.
It does not authorize work, establish a new review gate, amend a contract, or replace
repository-local instructions. [Authority and work](../governance/authority-and-work.md)
owns work and finding disposition;
[software design](../standards/software-design.md) owns project-neutral design defaults;
[GitHub](../standards/github.md) and [validation](../standards/validation.md) own
delivery and evidence rules. Use the [issue outline](../templates/investigation.md)
when a fresh issue benefits from a structured body; existing issues need not be reformatted.

## Discover authority before reasoning from history

1. Identify the decision or observable outcome the owning issue must enable. If no
   accepted issue exists, follow the existing idea/intake and work-selection authority;
   a roadmap entry, report, prior prompt, or finding alone does not authorize work.
2. Establish the owning repository and current accepted revision. Inspect its
   `AGENTS.md`, issue and related PR, then the **relevant** architecture/ADR/contracts,
   implementation, tests, and Engineering standards. Resolve cross-repository owners
   only where the investigated boundary requires it. Read widely when the scope is
   wide; do not load unrelated documents merely to complete a ritual.
3. Distinguish accepted `main`, an exact candidate/PR head, and historical revisions.
   Recheck mutable state before deciding or proposing a correction. Search helps locate
   evidence but cannot prove an exhaustive inventory or the absence of a dependency.

## Frame a falsifiable inquiry

State the question, why it matters, system/owner boundaries, excluded changes, and
what a decision-ready result must show. Identify competing hypotheses and practical
alternatives, including retaining the existing design or making no change. Decide
which observations, reproductions, measurements, negative cases, or counterexamples
could change the recommendation. Choose relevant criteria such as correctness,
semantic ownership, maintainability, usability, performance, portability, cost, and
evolution without treating one metric (file count, brevity, or an existing design)
as a predetermined winner.

An **investigation** seeks a supported answer to a bounded question.
An **audit** additionally states an explicit coverage universe and inspection method:
exact revision(s), included/excluded paths or behaviors, inventory completeness,
inspection depth, tools/checks actually used, uninspected areas, and limitations.
A file counted or text-screened is not thereby semantically reviewed, validated,
or proven correct. A feature branch is separate candidate evidence, not accepted
repository state.

## Gather and challenge evidence

- Inspect actual source, tests, contracts, consumers, and failure paths relevant to
  the question. Follow dependencies as far as needed to substantiate conclusions.
- Separate **source-observed behavior/structure**, **executed reproduction or
  measurement**, **inference**, **unverified hypothesis**, and **unavailable evidence**.
  Name exact commit and, where material, test inputs, platform, command, or CI run.
  Do not claim local execution from hosted CI or generalize one passing workload
  into universal support.
- Seek counterexamples and positive counterfindings. Challenge both new proposals
  and accepted designs; absence of a demonstrated defect can justify retaining
  current structure. Do not modify tests or contracts solely to make evidence green.
- Compare viable options using the same stated criteria and realistic workloads.
  Where feasibility depends on quality, resource, platform, or scaling bounds,
  demand evidence of those bounds rather than an algorithm name or speculative
  benchmark. A negative or inconclusive result is a valid outcome.

## Record findings and route outcomes

Use stable, issue-scoped IDs (for example, `F01`) for material findings. For each,
capture as relevant:

| Field | Record |
|---|---|
| Claim | Specific defect, risk, contradiction, or positive counterfinding |
| Provenance | Owning repository, immutable revision, source/test/evidence links |
| Evidence level | Observed, reproduced/measured, inferred, hypothesized, or unavailable |
| Impact | Concrete consequence and severity **where justified** |
| Recommendation | Correction, independent proof, retention, deferral, or no action |
| Disposition/owner | Owning issue/PR or accepted decision; unresolved if still gated |

Keep the same ID when the evidence or disposition is revised, and identify what
revision the re-review covers. Do not fabricate numerical confidence scores or
label every maintainability preference a defect. Route material findings using
the existing [review reconciliation](../governance/authority-and-work.md#material-review-reconciliation):
correct in current scope, amend accepted design/ADR for durable contract changes,
open a justified separately owned issue, or retain report-only evidence.
An audit finding does **not** automatically authorize source changes or a merge.

Keep the **issue body navigable**: question/outcome, applicable authority, current
decision or gate, material findings/dispositions, acceptance boundary, and links.
Detailed fixed-revision inventories, reproduction logs, and completed investigation
evidence may live in linked issue comments or existing CI/artifacts. Preserve
historical results without appending successive status ledgers to the main body.
Promote a research artifact into versioned source only if its reproducibility or
ongoing technical value independently justifies maintenance. Do not duplicate
current Project state, PR/head status, or permanent contracts in durable Markdown.

## Decide and finish

Report what was established, viable alternatives and their tradeoffs, what was
falsified, what remains unknown, and a justified recommendation. Explicitly say
whether the original question is answered, blocked by unavailable evidence, or
requires an owner decision. Close only when the owning issue's criteria are
satisfied or an accepted disposition permits closure. Success may mean retaining
the current design, deferring with a concrete revisit condition, or declining
implementation.

An accepted investigation conclusion is **not** production implementation
authority by default. Implementation, contract change, validation, independent
review, and protected acceptance follow their existing owning authorities.
For authorized delivery, see the [implementation workflow](implementation-workflow.md).

### Example cold start

`Investigate <owning issue URL> from current accepted authority. Read the owning
repository AGENTS.md and apply the Engineering investigation workflow. Return a
decision-ready, evidence-linked disposition without assuming implementation authority.`

This example is an invocation convenience, not a substitute for an agent actually
fetching the applicable documents. Environments without automatic repository
instruction discovery must retrieve the entrypoint explicitly.
