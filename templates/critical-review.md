# Critical pull-request review — reusable outline

Use this outline in a pull-request review comment when it helps make a substantive
review reproducible. Adapt it to the risk and scope; omit irrelevant prompts rather
than filling them with boilerplate. A trivial editorial change may need only a brief,
source-grounded verdict. Do not duplicate the PR description, issue, test logs, or
a permanent status ledger.

This is **optional reporting guidance**, not a review policy, additional approval
gate, or grant of merge authority. Follow the currently accepted
[Engineering review governance](https://github.com/dornglut/engineering/blob/main/governance/authority-and-work.md),
[GitHub standard](https://github.com/dornglut/engineering/blob/main/standards/github.md),
and any stronger accepted repository-local requirements. In particular, a
documented author-side review does **not** satisfy an independently required
reviewer merely by using this template. Do not apply an unmerged policy proposal.

## Review identity and coverage

- **Repository / PR / owning issue:** [links]
- **Accepted base → exact reviewed feature head:** [full commit SHAs]
- **Reviewer and provenance:** [actual person or agent; author-side AI-assisted /
  genuinely non-authoring human / genuinely non-authoring AI]
- **Inspected:** [complete base-to-head diff, modified source, owning contracts,
  relevant consumers/tests and their exact revisions]
- **Not inspected / visibility limits:** [explicit gaps, including inaccessible paths]
- **Applicable review rules:** [current accepted sources, including any required
  separate reviewer, platform qualification, or maintainer authorization]

A new chat or account label is not proof of genuine independence. State what
was actually reviewed; a file list, search result, or green check is not a full
semantic inspection. Re-review the new complete diff when the feature head changes.

## Risk and obligations

- **Classification and reason:** [routine / heightened, by applicable authority]
- **Affected boundaries:** [accepted semantics/architecture and owner; public API
  or compatibility; security/trust; persistent data or irreversible migration;
  concurrency/ordering/resource lifetime; cross-repository contracts;
  governance/CI/protection; native/hardware/conformance; other actual risks]
- **Required additional assurance:** [named owner decision, distinct reviewer if
  required, executable proof, hardware/platform evidence, or none with rationale]

A risk category not affected is not the same as a category not investigated.
The template never relaxes a stronger accepted review or evidence requirement.

## Adversarial source review

Record **specific answers and source/evidence links**, not merely checked boxes.
Challenge the author's claims against the current accepted contracts:

1. **Outcome and scope:** Which issue criteria are demonstrably satisfied or
   missed? Does the complete diff include unauthorized behavior or hidden scope?
2. **Ownership and design:** Are the correct semantic owners, dependency
   directions, invariants, compatibility boundaries, and long-term maintenance
   costs preserved? Are any abstractions or dual authorities unjustified?
3. **Correctness and failure:** What concrete counterexample could break the
   design? Examine applicable empty/invalid/boundary inputs, error/recovery,
   cancellation, stale state, concurrency/ordering, and resource lifetimes.
4. **Integration and regressions:** Which existing/public consumers, negative
   contracts, migrations, platforms, or cross-repository pins are affected?
5. **Proof strength:** Do tests cover real observable behavior and relevant
   negative paths? What remains unproven by tests, static inspection, mocks,
   simulations, or unsupported performance/physical claims?

**Counterexamples actually investigated:** [scenario → source/test or reproduction
→ observed result; distinguish an unexecuted hypothesis from a verified test]

**Source-grounded assessment:** [material facts and reasoning, including why
the implementation does or does not satisfy the owning issue]

## Validation and evidence

| Check / proof | Actual result and link |
| --- | --- |
| Exact base-to-head diff and relevant consumers | [coverage / gaps] |
| Focused positive, boundary, negative, regression checks | [PASS / FAIL / NOT RUN] |
| Repository-owned canonical exact-head CI | [run URL, actual checkout SHA, PASS / FAIL / PENDING / NOT RUN] |
| Required integration, public conformance or physical qualification | [evidence / unavailable / not applicable with rationale] |
| Prior review findings, holds, and review threads | [IDs, exact-head dispositions, unresolved items] |

Do not describe planned, unavailable, static, or simulated evidence as executed
qualification. A passing CI result alone does not prove acceptance criteria.

## Material findings and disposition

| Stable ID / severity | Exact revision, source and observed impact | Required disposition and supporting evidence |
| --- | --- | --- |
| [F-... / P1 etc.] | [location, falsifier and consequence] | [corrected / unresolved HOLD / authorized nonblocking follow-up] |

Keep existing finding IDs across corrections; identify any old review HOLD
and the current-head evidence that explicitly supersedes it. Do not relabel
an unresolved correctness/security defect or missing mandatory evidence as
accepted risk merely to clear a PR. If no material findings were identified,
say so with actual coverage and limitations, not an assertion of defect-free code.

## Technical verdict

**ACCEPT / HOLD:** [one; bind it to the exact reviewed head]

**Rationale and residual risk:** [source-grounded conclusion, limits, any
correlated author-side review risk, and exact corrective work if HOLD]

An **ACCEPT** requires a supported positive assessment of the applicable review
criteria; an unresolved material HOLD cannot count as accepting. Technical
ACCEPT is **not** a GitHub approval event or authorization to merge.

## Separate merge-eligibility reconciliation

**ELIGIBLE / HOLD / NOT ASSESSED:** [one; not a substitute for the authorized
acceptance actor]

- [Current base, exact head, dependency closure, required hosted CI and
  integration/merge-group/accepted-main proof as applicable]
- [Unresolved material findings or holds; required review threads]
- [Any required genuinely independent review, risk-specific human-maintainer
  decision, security/conformance/physical evidence and repository protections]

**Evidence or blockers:** [links and remaining gates]

A template-complete record does not override missing evidence, repository
protections, current accepted authority, or an explicit hold. A new feature
head requires a new exact-head review and validation before acceptance.
