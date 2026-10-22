# [Investigation/Audit] Decision question or audit outcome

## Question and motivation

What question or observed problem requires an evidence-backed answer? Why now?

## Authority and boundaries

Owning repository/issue, relevant accepted contracts or decisions, and known
dependencies. Identify included scope, non-goals, and authority boundaries.
Re-resolve exact repository revisions when the work begins.

## Evidence and comparison

What source, contracts, consumers, tests, reproductions, measurements, alternatives,
and counterexamples matter? Specify a decision-relevant proof threshold without
preselecting the recommended solution.

## Required result and decision gate

Describe the answer or audit findings needed for closure, acceptable negative or
inconclusive outcomes, and any explicit stop/owner-decision condition. This
investigation does not authorize implementation or a contract change by itself.

## Results and disposition (populate from actual evidence)

Current conclusion, links to fixed-revision evidence, material finding IDs and
owners, remaining uncertainty, and decision/closure status. Keep this section
short; put substantial inventories and logs in linked issue comments or
existing evidence artifacts.

## Audit coverage (include only for an audit)

Exact revision(s), complete target universe/inventory method, inspection depth,
uninspected paths or behavior, tools/checks actually executed, and evidence limits.
Classify findings by stable IDs, evidence strength, material impact, and owner/
disposition. An inventory or text scan is not proof of semantic correctness.

---

Procedure: [Engineering investigation and audit workflow](https://github.com/dornglut/engineering/blob/main/tooling/investigation-workflow.md).
Omit irrelevant sections rather than supplying invented evidence or decisions.
