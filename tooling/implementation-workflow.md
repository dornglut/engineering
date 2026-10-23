# Implementation and delivery workflow

Reusable, executor-neutral **method guidance** for carrying a bounded, authorized
Dornglut change from current behavior to reviewed implementation and truthful
acceptance evidence. It applies to code, tests, documents and tooling in proportion
to their risks. It is **not** additional work authorization, a prescribed development
process, an implementation design, or a new merge/review gate.

Use the owning repository's `AGENTS.md`, accepted issue/contract and source as
applicable. [Authority and work](../governance/authority-and-work.md) owns scope,
work selection and finding routing; [software design](../standards/software-design.md)
owns design requirements; [GitHub](../standards/github.md) and
[validation](../standards/validation.md) own publication, review and verification.
The [GPT Web procedure](gpt-web-github.md) describes connector mechanics; the
[autonomous repository goal](autonomous-repository-goal.md) is for broader
work selection and delegated continuation, not a prerequisite for a single issue.
Use the [investigation workflow](investigation-workflow.md) when the question is
not yet decision-complete.

## Establish the real task

- Start with the accepted **owning issue**, its outcome, exclusions, acceptance
  conditions and current status. Resume an existing PR only after checking its
  actual base, head, diffs, feedback, dependencies and writers. An investigation,
  old handoff, roadmap or unmerged design is evidence, not implementation rights.
- Establish the exact accepted repository revision, current source behavior,
  executable tests, consumer usage, relevant ADR/design/conformance obligations,
  semantic owners and cross-repository pins. Read the full files to be changed
  from the exact candidate parent. Expand inspection only where a real dependency,
  invariant, integration path or uncertainty demands it.
- Describe the **behavioral difference** to deliver, not only a list of files
  to edit. Identify what must remain unchanged, including failure and lifecycle
  behavior, compatibility, performance and resource limits, and independently
  owned contracts. A green test against an obsolete expectation is not authority.
- If the requested result conflicts with accepted architecture, needs a new
  contract/owner decision, or relies on missing feasibility evidence, stop that
  transition and route the question to its owner or a bounded
  [investigation](investigation-workflow.md). Continue independent authorized
  work only when safe.

## Design for the actual obligation

Compare reasonable approaches, including retaining existing structure or
correcting only a verified defect. Evaluate the applicable contract, invariants,
state ownership, dependency direction, public usability, failure handling,
evolution, measured costs and testability. Prefer **long-term conceptual
simplicity**, not the fewest edits, files or abstractions. Justify added layers by
the responsibilities or coupled changes they actually remove; do not build
speculative machinery for hypothetical consumers.

For a meaningful design choice, identify what would falsify it: difficult
counterexamples, rejected and negative cases, concurrency or temporal ordering,
source/consumer incompatibility, platform differences, scalability or resource
ceilings. Distinguish observed behavior, proven properties, measured costs,
modeled estimates and unsupported assumptions. If the evidence cannot support a
choice, do not disguise experimental exploration as completed production work.

## Match proof to claims

Determine what evidence would establish the accepted outcome **before claiming
completion**. Use proportionate checks rather than the same test matrix for all
changes. Examples include:

- representative public behavior plus relevant edge, error, lifetime, cancellation
  and regression paths; invariants may need property, structural or negative tests;
- real consuming APIs, fixtures, conformance IDs, integration behavior and
  backends/platforms when the accepted outcome depends on them;
- representative workloads and complete resource/performance accounting when
  a cost or scale claim is material; a passing narrow example is not universal
  capability or mathematical feasibility;
- precise links and source truth for a documentation-only correction, followed
  by the repository's applicable documentation and canonical checks.

Protect existing accepted positive and negative obligations. Do not silence,
skip, quarantine, weaken or silently reinterpret a failing test to make a
candidate pass. A blocked proof remains blocked until corrected or separately
dispositioned by its owning authority. A tool or physical environment that was
not run must not be described as passing.

## Implement and critically challenge the candidate

- Implement within the accepted write set and actual semantic owner. Keep a
  coherent change whose interfaces, error paths, consumers and tests agree;
  preserve unrelated behavior and accepted production algorithms. Make scope
  expansion or new shared contracts explicit in their owning authority **before**
  introducing them, rather than concealing them as incidental refactoring.
- Iterate using relevant focused checks, source review and concrete falsifiers.
  Use the repository's normal checked-out executor when required by the work;
  follow the supported execution/publication procedure for the active
  environment. Do not substitute static inspection for execution or assume
  GitHub search proves a dependency is absent.
- Critically re-read the **complete accepted-base to candidate-head change**
  with the issue and unchanged owning contracts in view. Challenge semantic
  correctness, hidden state, error/recovery, ordering, unintended consumers,
  speculative complexity, test strength, evidence gaps, migration and
  compatibility. Seek a counterexample rather than merely explaining why the
  patch looks plausible.
- Record material review findings by stable ID, exact reviewed head, evidence,
  impact and the disposition required by
  [material review reconciliation](../governance/authority-and-work.md#material-review-reconciliation).
  Correct current-scope failures in the current lineage. Route independent,
  nonblocking work separately and keep explicit holds binding. Reviewer
  independence, required approvals and protected acceptance remain governed
  by **current accepted** standards and the owning repository; this method
  neither waives nor adds a reviewer requirement.

## Validate, accept or stop truthfully

Use focused tests and the owning repository's complete canonical validation;
prove the **unchanged exact reviewed head** in hosted CI and any additional
mandated conformance or physical evidence. A head change invalidates prior
head-specific review and validation for acceptance. Distinguish local, hosted,
modeled, simulated and unavailable evidence. Candidate construction, branch
publication, safe updates and merge follow the [GitHub standard](../standards/github.md#agent-mediated-repository-changes),
not this document.

Before protected acceptance, reconcile the actual final diff, current accepted
base, dependencies, writer conflicts, findings, required checks, review state and
mergeability. **Passing CI does not prove the issue is complete.** Do not merge a
partially implemented accepted outcome, silently narrow conformance, or treat a
typed rejection as successful positive support unless the owning contract permits
that outcome. A genuine blocker may leave an accurate draft PR; a falsified
design may require a fresh investigation or an owner decision.

After acceptance, verify the required accepted-main evidence; update only the
affected durable contracts, issue/PR and Project state through their existing
owners. Avoid new status ledgers, historical proof copies or ritual closeout
documents. Report what changed, which requirement it satisfies, evidence
actually executed, remaining limitations and the next justified action.

For a small, well-bounded editorial or defect correction, this can amount to
source verification, one coherent edit, focused review and canonical CI. A
cross-owner migration or numerical algorithm needs deeper dependency, design,
falsification and qualification. Neither case requires filling out a new form.

### Example cold start

`Continue <owning delivery issue URL> from current live repository state.
Follow the owning AGENTS.md and Engineering implementation workflow.
Critically review the current design and complete the authorized outcome,
with evidence-bound validation and protected acceptance only where permitted.`

Environments that do not automatically load repository instructions must
retrieve the applicable entrypoints explicitly. A prompt cannot replace
verifying actual authority.
