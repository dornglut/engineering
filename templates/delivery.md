# [Delivery] Outcome

Use this optional issue-body outline for **accepted, bounded implementation work**.
Replace prompts with real information; omit irrelevant material. This is not a
public GitHub issue form, a project plan, or permission to implement by itself.
Existing [Engineering authority and work](https://github.com/dornglut/engineering/blob/main/governance/authority-and-work.md)
and the [implementation workflow](https://github.com/dornglut/engineering/blob/main/tooling/implementation-workflow.md)
govern selection, acceptance, and proof.

## Why and desired outcome

What currently fails, is missing, or needs changing? What observable result must
be true when this issue is complete? Link the current source/consumer evidence.

## Owner, authority, and boundaries

Name the owning repository/component and current accepted contracts or ADRs.
Describe what is **included** and explicitly **not included**. Identify actual
dependent issues, consumers, and cross-repository acceptance/pinning constraints.
Re-resolve exact repository revisions when work begins.

## Acceptance and proof

Describe concrete positive and negative acceptance cases and what evidence can
falsify the proposed change. State relevant test/CI, compatibility, security,
performance, physical-platform, or migration proof only when the outcome needs it.
Do not pre-label unexecuted work as passing.

## Stop or owner-decision conditions

What would require a new decision rather than silently expanding this issue?
Include new semantic/public contracts, different owners, missing feasibility
evidence, unsafe migrations, and unresolved required review/validation as applicable.

## Result and disposition (after work)

Summarize the verified outcome and link the actual PR and exact-revision evidence.
Record material finding IDs, unresolved blockers, and justified follow-ups with
their own owner. Do not duplicate detailed CI logs or create a second status ledger.

---

This outline does not replace issue-specific acceptance criteria, the canonical
validation command, critical review, or protected GitHub acceptance.
