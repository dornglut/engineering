# Critical review

A clear record of **what was checked, what was found, and whether the change is ready**.
Use it for code, tests, documentation, designs, configuration, or workflows.

Copy the useful parts into a pull-request comment or another review record. Keep
small reviews short. Replace the prompts with real findings, omit irrelevant
questions, and link to evidence instead of copying logs.

> This template documents a review. It does **not** change project rules,
> replace required evidence or approvals, or grant permission to merge.

## 1. Overview

| | Details |
| --- | --- |
| **Change** | [PR, issue, document, or proposal link] |
| **Version reviewed** | [For a PR: full before/after commit IDs (base/head); otherwise: exact version] |
| **Reviewer / session** | [Who or what conducted the review; identify the reviewed session if useful] |
| **Coverage** | [Changes, requirements, affected people/systems, and other context examined] |
| **Not reviewed** | [Anything left out or inaccessible] |

**Goal:** [What is this change meant to achieve?]

**Risk and impact:** [What could go wrong, and is extra review or proof required?]

## 2. Review notes

Explain the important answers. Do not mark a topic as checked without examining it.

- **Does it do the right thing?** Compare the change with its requirements.
  Note missing behavior, unexpected changes, or incorrect claims.
- **Could it fail?** Look for realistic bad inputs, edge cases, errors,
  cancellation, timing, security problems, or data loss where relevant.
- **Could it break something else?** Check affected users, integrations,
  compatibility, dependencies, and existing behavior.
- **Is it a sound long-term solution?** Consider clarity, ownership,
  maintainability, unnecessary complexity, and changes to existing contracts.
- **What evidence supports it?** Check relevant source, tests, examples,
  documentation, and real-world behavior. Identify assumptions or missing proof.

**Most important failure case examined:** [What might go wrong, how you
investigated it, and what you actually found]

**Assessment:** [Brief source- or evidence-based explanation of what is correct,
incorrect, or uncertain]

## 3. Checks and evidence

| Check | Result and evidence |
| --- | --- |
| Change and affected context | [Reviewed scope; link to source/diff] |
| Tests or practical checks | [Passed / Failed / Not run / Not applicable — why; link] |
| Required CI or automated validation | [Status, run link, and exact checked version] |
| Other required proof | [Integration, security, performance, platform, or physical evidence if relevant] |
| Earlier findings and open discussions | [Resolved with evidence / Still open / None] |

Be precise: **not run** is not **passed**. A successful automated check
does not prove that every requirement is met.

## 4. Findings

List meaningful problems, not speculative or cosmetic filler.

| ID / priority | Problem and impact | Status or required action |
| --- | --- | --- |
| [ID if needed] | [Evidence and why it matters] | [Fixed with proof / Open / Valid nonblocking follow-up] |

**Open risks or missing evidence:** [None identified, or specific limitations]

Keep stable IDs for material findings across revisions. An existing
**HOLD** stays open until the problem is fixed and the updated version is
reviewed, or an authorized decision explicitly resolves it. Missing required
proof and known correctness or security defects cannot be waved away.

## 5. Decision

**Review decision: ACCEPT / HOLD**

**Why:** [Short explanation based on inspected evidence]

**What still needs to happen:** [Concrete actions, or none]

For pull requests only:

**Ready to merge: YES / NO / NOT CHECKED**

**Merge blockers:** [Required checks, unresolved findings or conversations,
review evidence, maintainer decisions, and repository protections]

A review **ACCEPT** is not a GitHub approval or permission to merge.
Follow [Engineering critical review and acceptance](../governance/authority-and-work.md#critical-review-and-acceptance).

If the proposed version changes, update the review and rerun required
version-specific checks before acceptance. Verify post-merge results
separately when the project requires them.
